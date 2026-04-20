"""
core/engine.py
──────────────
PitchIQ analytical engine — all coaching intelligence lives here.

Every function accepts live player dicts (from squad_resolver), never
hardcoded data.  The MatchState dataclass is the single source of truth
for the current match situation.

Functions:
    win_probability()              — DLS-inspired bat/bowl win %
    pressure_index()               — 0-100 pressure gauge
    batting_order_recommendation() — who bats next, ranked
    bowling_plan()                 — next 6 overs plan
    matchup_matrix()               — batter × bowler heatmap
    impact_sub_recommendation()    — bench player timing
    field_placement_hints()        — 3 field placement strings
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════════════════
# MATCH STATE
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class MatchState:
    """
    Immutable snapshot of the current match situation.

    Auto-computed fields: phase, balls_left, crr, rrr, proj_score,
    is_chasing.
    """
    batting_team: dict = field(default_factory=dict)
    bowling_team: dict = field(default_factory=dict)
    runs: int = 0
    wickets: int = 0
    overs: float = 0.0
    target: int | None = None
    venue_name: str = ""
    innings_number: int = 1

    # ── Auto-computed ────────────────────────────────────────────────
    @property
    def phase(self) -> str:
        """Return the current phase: 'powerplay', 'middle', or 'death'."""
        if self.overs < 6:
            return "powerplay"
        elif self.overs < 16:
            return "middle"
        return "death"

    @property
    def balls_bowled(self) -> int:
        """Convert overs (e.g. 13.2) to total balls."""
        full_overs = int(self.overs)
        balls = int(round((self.overs - full_overs) * 10))
        return full_overs * 6 + balls

    @property
    def balls_left(self) -> int:
        """Balls remaining in the innings (max 120)."""
        return max(0, 120 - self.balls_bowled)

    @property
    def crr(self) -> float:
        """Current run rate."""
        if self.overs <= 0:
            return 0.0
        return round(self.runs / self.overs, 2)

    @property
    def rrr(self) -> float | None:
        """Required run rate (only when chasing)."""
        if not self.is_chasing or self.balls_left <= 0:
            return None
        overs_left = self.balls_left / 6.0
        runs_needed = (self.target or 0) - self.runs
        if overs_left <= 0:
            return 99.99
        return round(runs_needed / overs_left, 2)

    @property
    def proj_score(self) -> int:
        """Projected total at current run rate (for 1st innings)."""
        if self.overs <= 0:
            return self.runs
        return int(self.crr * 20)

    @property
    def is_chasing(self) -> bool:
        """True if batting team is chasing a target."""
        return self.target is not None and self.target > 0

    @property
    def runs_needed(self) -> int:
        """Runs still required (0 if not chasing)."""
        if not self.is_chasing:
            return 0
        return max(0, (self.target or 0) - self.runs)


# ═══════════════════════════════════════════════════════════════════════
# WIN PROBABILITY
# ═══════════════════════════════════════════════════════════════════════

def win_probability(ms: MatchState) -> tuple[float, float]:
    """
    Duckworth-Lewis-inspired win probability.

    Considers: required rate vs 8.0 baseline, wickets in hand,
    venue average, dew factor, phase, powerplay score.

    Parameters
    ----------
    ms : MatchState

    Returns
    -------
    (bat_prob, bowl_prob)   both floats 0.0-1.0 summing to 1.0.
    """
    if not ms.is_chasing:
        # 1st innings — estimate a rough probability based on projected score
        par = 170  # average IPL 1st innings score
        diff = ms.proj_score - par
        bat_prob = 0.5 + (diff / 200) * 0.3
        bat_prob = max(0.15, min(0.85, bat_prob))
        return round(bat_prob, 3), round(1 - bat_prob, 3)

    # ── 2nd innings (chasing) ────────────────────────────────────────
    base = 0.50

    # RRR factor: easier chase → bat advantage
    rrr_val = ms.rrr or 8.0
    rrr_factor = (8.0 - rrr_val) / 8.0 * 0.25
    base += rrr_factor

    # Wickets in hand: more wickets = bat advantage
    wkts_in_hand = 10 - ms.wickets
    wkt_factor = (wkts_in_hand - 5) / 10.0 * 0.20
    base += wkt_factor

    # Phase factor: death overs with high RRR = bowl advantage
    if ms.phase == "death" and rrr_val > 10:
        base -= 0.10
    elif ms.phase == "powerplay" and ms.crr > 8:
        base += 0.05

    # Balls left: more balls = bat advantage
    balls_factor = (ms.balls_left - 60) / 120.0 * 0.10
    base += balls_factor

    # Clamp
    bat_prob = max(0.02, min(0.98, base))
    return round(bat_prob, 3), round(1 - bat_prob, 3)


# ═══════════════════════════════════════════════════════════════════════
# PRESSURE INDEX
# ═══════════════════════════════════════════════════════════════════════

def pressure_index(ms: MatchState) -> dict:
    """
    Compute a 0-100 pressure score for the batting team.

    Parameters
    ----------
    ms : MatchState

    Returns
    -------
    dict   {"score": int, "label": str, "color": str}
    """
    pressure = 40  # neutral baseline

    # RRR pressure
    if ms.is_chasing and ms.rrr:
        if ms.rrr > 12:
            pressure += 30
        elif ms.rrr > 10:
            pressure += 20
        elif ms.rrr > 8:
            pressure += 10
        elif ms.rrr < 6:
            pressure -= 15

    # Wickets lost
    if ms.wickets >= 7:
        pressure += 25
    elif ms.wickets >= 5:
        pressure += 15
    elif ms.wickets >= 3:
        pressure += 5
    elif ms.wickets == 0:
        pressure -= 10

    # Phase
    if ms.phase == "death":
        pressure += 10
    elif ms.phase == "powerplay":
        pressure -= 5

    # Balls left
    if ms.balls_left < 18:
        pressure += 15
    elif ms.balls_left < 36:
        pressure += 8

    pressure = max(0, min(100, pressure))

    if pressure < 35:
        label, color = "Controlled", "#22c55e"
    elif pressure < 65:
        label, color = "Elevated", "#f59e0b"
    else:
        label, color = "Critical", "#ef4444"

    return {"score": pressure, "label": label, "color": color}


# ═══════════════════════════════════════════════════════════════════════
# BATTING ORDER RECOMMENDATION
# ═══════════════════════════════════════════════════════════════════════

def batting_order_recommendation(
    ms: MatchState,
    available_batters: list[dict],
) -> list[dict]:
    """
    Rank available batters by who should come in next.

    Scoring considers: phase-appropriate SR, vs_pace/vs_spin,
    form, chase context, and wickets context.

    Parameters
    ----------
    ms                : MatchState
    available_batters : list[dict]   Playing 11 minus dismissed

    Returns
    -------
    list[dict]   ranked list with keys:
        name, role, score, rationale, profile
    """
    if not available_batters:
        return []

    scored = []
    for player in available_batters:
        prof = player.get("profile", {})
        score = 0.0
        reasons = []

        # ── Phase weight ─────────────────────────────────────────────
        if ms.phase == "powerplay":
            pp_sr = prof.get("powerplay_sr", 130)
            score += pp_sr * 0.35
            if pp_sr > 145:
                reasons.append(f"Strong PP striker (SR {pp_sr})")
        elif ms.phase == "death":
            d_sr = prof.get("death_sr", 140)
            score += d_sr * 0.40
            if d_sr > 170:
                reasons.append(f"Death-overs specialist (SR {d_sr})")
        else:
            sr = prof.get("sr", 130)
            score += sr * 0.30
            avg = prof.get("avg", 25)
            score += avg * 0.15
            if avg > 35:
                reasons.append(f"High average ({avg})")

        # ── vs Pace / Spin ───────────────────────────────────────────
        # Approximate: early overs = more pace, late = more spin
        if ms.phase in ("powerplay", "death"):
            vp = prof.get("vs_pace", 50)
            score += vp * 0.10
            if vp > 75:
                reasons.append(f"Handles pace well ({vp}/100)")
        else:
            vs = prof.get("vs_spin", 50)
            score += vs * 0.10
            if vs > 75:
                reasons.append(f"Strong vs spin ({vs}/100)")

        # ── Form ─────────────────────────────────────────────────────
        form = prof.get("form", 65)
        score += form * 0.15
        if form > 85:
            reasons.append(f"Red-hot form ({form}/100)")

        # ── Chase context ────────────────────────────────────────────
        if ms.is_chasing:
            rrr_val = ms.rrr or 8.0
            chase_sr = prof.get("chase_sr", 130)
            if rrr_val > 9:
                score += chase_sr * 0.15
                if chase_sr > 155:
                    reasons.append(f"Chase specialist (SR {chase_sr})")
            else:
                score += prof.get("avg", 25) * 0.10
                if prof.get("avg", 25) > 35:
                    reasons.append("Can anchor the chase")

        # ── Wickets context ──────────────────────────────────────────
        if ms.wickets >= 7:
            avg = prof.get("avg", 25)
            score += avg * 0.20
            reasons.append("Need to protect the tail")
        if ms.wickets <= 1:
            sr = prof.get("sr", 130)
            score += sr * 0.05

        # ── Role bonus ───────────────────────────────────────────────
        role = player.get("role", "bat")
        if role == "bat":
            score += 5
        elif role == "wk-bat":
            score += 3

        if not reasons:
            reasons.append("Solid all-round option")

        scored.append({
            "name": player["name"],
            "role": player.get("role", "bat"),
            "score": round(score, 1),
            "rationale": ". ".join(reasons),
            "profile": prof,
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored


# ═══════════════════════════════════════════════════════════════════════
# BOWLING PLAN
# ═══════════════════════════════════════════════════════════════════════

_LINE_LENGTH = {
    "powerplay": [
        ("Full outside off", "Swing the new ball, target edges"),
        ("Short of a length, angling in", "Dry up runs, induce false shots"),
        ("Yorker at the stumps", "Surprise yorker for early wicket"),
    ],
    "middle": [
        ("Line on middle/off", "Control the run rate, vary pace"),
        ("Wide outside off with slip", "Tempt the drive on a turning pitch"),
        ("Short ball, target body", "Upset the rhythm with bouncers"),
    ],
    "death": [
        ("Wide yorker outside off", "Hardest to hit for six"),
        ("Slower ball back of length", "Deceive with pace changes"),
        ("Blockhole delivery", "Target the base of the stumps"),
    ],
}


def bowling_plan(
    ms: MatchState,
    available_bowlers: list[dict],
    batters_at_crease: list[dict],
) -> list[dict]:
    """
    Generate an over-by-over bowling plan for the next 6 overs.

    Parameters
    ----------
    ms                 : MatchState
    available_bowlers  : list[dict]   bowlers with < 4 overs
    batters_at_crease  : list[dict]   current 2 batters

    Returns
    -------
    list[dict]   each with: over, phase, bowler, line, reasoning
    """
    if not available_bowlers:
        return []

    plan = []
    current_over = int(ms.overs) + 1
    used_overs: dict[str, float] = {}
    for b in available_bowlers:
        used_overs[b["name"]] = b.get("overs_bowled", 0.0)

    for i in range(6):
        over_num = current_over + i
        if over_num > 20:
            break

        # Determine phase
        if over_num <= 6:
            phase = "powerplay"
        elif over_num <= 16:
            phase = "middle"
        else:
            phase = "death"

        # Score each bowler
        best_bowler = None
        best_score = -1

        for bowler in available_bowlers:
            prof = bowler.get("profile", {})
            bname = bowler["name"]
            overs_used = used_overs.get(bname, 0.0)

            # Skip if quota exhausted
            if overs_used >= 4.0:
                continue

            score = 0.0

            # Economy rating
            if phase == "death":
                econ = prof.get("death_econ", 9.0)
                score += (12.0 - econ) * 10
            else:
                econ = prof.get("econ", 8.0)
                score += (10.0 - econ) * 8

            # Wicket-taking
            wkts = prof.get("wkts", 5)
            score += wkts * 2

            # Form
            form = prof.get("form", 65)
            score += form * 0.3

            # Phase specialist bonus
            bowling_type = prof.get("bowling_type", "")
            if phase == "powerplay" and bowling_type == "pace":
                score += 15
            elif phase == "middle" and bowling_type in ("offspin", "legspin", "left-arm-spin"):
                score += 15
            elif phase == "death" and bowling_type == "pace":
                score += 10

            # Matchup bonus vs batters at crease
            for bat in batters_at_crease:
                bat_prof = bat.get("profile", {})
                bat_hand = bat_prof.get("hand", "R")
                if bowling_type in ("offspin",) and bat_hand == "R":
                    score += 5  # offspin into right-hander
                elif bowling_type in ("legspin",) and bat_hand == "L":
                    score += 5
                elif bowling_type in ("left-arm-spin",) and bat_hand == "R":
                    score += 5

            # Overs remaining bonus (use bowlers who have overs left)
            quota_left = 4.0 - overs_used
            if quota_left <= 1:
                score -= 10  # save for later if possible
            elif quota_left >= 3:
                score += 5

            if score > best_score:
                best_score = score
                best_bowler = bowler

        if not best_bowler:
            break

        # Pick line & length
        lines = _LINE_LENGTH.get(phase, _LINE_LENGTH["middle"])
        line_idx = i % len(lines)
        line, reason = lines[line_idx]

        # Update used overs
        used_overs[best_bowler["name"]] = used_overs.get(best_bowler["name"], 0) + 1.0

        plan.append({
            "over": over_num,
            "phase": phase,
            "bowler": best_bowler["name"],
            "line": line,
            "reasoning": reason,
            "profile": best_bowler.get("profile", {}),
            "overs_used": used_overs[best_bowler["name"]],
        })

    return plan


# ═══════════════════════════════════════════════════════════════════════
# MATCHUP MATRIX
# ═══════════════════════════════════════════════════════════════════════

def matchup_matrix(
    batters: list[dict],
    bowlers: list[dict],
) -> list[dict]:
    """
    Compute advantage scores for every batter × bowler pair.

    Positive = batter advantage, Negative = bowler advantage.

    Parameters
    ----------
    batters : list[dict]   Playing 11 batters
    bowlers : list[dict]   Playing 11 bowlers

    Returns
    -------
    list[dict]   flat list sorted by threat level, each with:
        batter, bowler, score, label, bat_hand, bowl_type
    """
    results = []
    for bat in batters:
        bp = bat.get("profile", {})
        for bowl in bowlers:
            bwp = bowl.get("profile", {})

            score = 0.0

            # SR advantage
            bat_sr = bp.get("sr", 130)
            bowl_econ = bwp.get("econ", 8.0) or 8.0
            score += (bat_sr - 130) * 0.15
            score -= (8.0 - bowl_econ) * 3

            # vs_pace / vs_spin
            bowling_type = bwp.get("bowling_type", "")
            if bowling_type in ("pace", "medium"):
                vs = bp.get("vs_pace", 50)
            else:
                vs = bp.get("vs_spin", 50)
            score += (vs - 50) * 0.3

            # Hand vs spin type
            bat_hand = bp.get("hand", "R")
            if bowling_type == "offspin" and bat_hand == "R":
                score -= 5  # off-spin into RHB
            elif bowling_type == "legspin" and bat_hand == "R":
                score += 3  # legspin away from RHB — batter can free arms
            elif bowling_type == "left-arm-spin" and bat_hand == "R":
                score -= 4  # turning in

            # Form differential
            bat_form = bp.get("form", 65)
            bowl_form = bwp.get("form", 65)
            score += (bat_form - bowl_form) * 0.15

            # Wickets factor
            wkts = bwp.get("wkts", 5)
            if wkts and wkts > 12:
                score -= 5

            # Label
            if score > 8:
                label = "🔴 Batter danger"
            elif score > 3:
                label = "🟡 Slight batter edge"
            elif score > -3:
                label = "⚪ Even"
            elif score > -8:
                label = "🟢 Slight bowler edge"
            else:
                label = "🟢 Bowler dominates"

            results.append({
                "batter": bat["name"],
                "bowler": bowl["name"],
                "score": round(score, 1),
                "label": label,
                "bat_hand": bat_hand,
                "bowl_type": bowling_type,
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


# ═══════════════════════════════════════════════════════════════════════
# IMPACT SUB RECOMMENDATION
# ═══════════════════════════════════════════════════════════════════════

def impact_sub_recommendation(
    ms: MatchState,
    bench_players: list[dict],
) -> list[dict]:
    """
    Score bench players for current-situation relevance.

    Parameters
    ----------
    ms            : MatchState
    bench_players : list[dict]   typically 4 players

    Returns
    -------
    list[dict]   ranked, each with:
        name, role, score, reason, timing, profile
    """
    if not bench_players:
        return []

    scored = []
    for player in bench_players:
        prof = player.get("profile", {})
        role = player.get("role", prof.get("role", "bat"))
        score = 0.0
        reason = ""
        timing = "Consider for later"

        # ── Chasing with high RRR → aggressive batter ────────────────
        if ms.is_chasing and ms.rrr and ms.rrr > 10:
            if role in ("bat", "wk-bat"):
                chase_sr = prof.get("chase_sr", 130)
                death_sr = prof.get("death_sr", 140)
                score += chase_sr * 0.4 + death_sr * 0.3
                reason = f"Aggressive chaser needed — SR {chase_sr} in chases"
                timing = "Bring in immediately"
            elif role == "allrounder":
                score += prof.get("sr", 130) * 0.3
                reason = "All-round option for chase acceleration"
                timing = "Bring in next wicket fall"

        # ── Death overs defending → death bowler ─────────────────────
        elif not ms.is_chasing and ms.phase == "death":
            if role in ("bowl", "allrounder"):
                death_econ = prof.get("death_econ", 9.0)
                if death_econ:
                    score += (12.0 - death_econ) * 15
                    reason = f"Death specialist — economy {death_econ}"
                    timing = f"Bring in at over {max(17, int(ms.overs) + 1)}"

        # ── Wickets falling → batting depth ──────────────────────────
        elif ms.wickets >= 5:
            if role in ("bat", "wk-bat", "allrounder"):
                avg = prof.get("avg", 25)
                score += avg * 1.5 + prof.get("form", 65) * 0.5
                reason = f"Batting reinforcement needed — avg {avg}"
                timing = "Bring in next over"

        # ── General middle-overs ─────────────────────────────────────
        else:
            form = prof.get("form", 65)
            score += form * 0.5
            if role in ("bowl", "allrounder"):
                econ = prof.get("econ", 8.0)
                if econ:
                    score += (9.0 - econ) * 5
                    reason = f"Spin/pace option — economy {econ}"
            elif role in ("bat", "wk-bat"):
                sr = prof.get("sr", 130)
                score += sr * 0.2
                reason = f"Batting depth — SR {sr}"
            timing = f"Bring in at over {min(14, int(ms.overs) + 2)}"

        if not reason:
            reason = "General squad depth option"

        scored.append({
            "name": player["name"],
            "role": role,
            "score": round(score, 1),
            "reason": reason,
            "timing": timing,
            "profile": prof,
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored


# ═══════════════════════════════════════════════════════════════════════
# FIELD PLACEMENT HINTS
# ═══════════════════════════════════════════════════════════════════════

def field_placement_hints(
    batter: dict,
    bowler: dict,
    phase: str,
) -> list[str]:
    """
    Generate 3 field placement suggestions.

    Parameters
    ----------
    batter : dict   player dict
    bowler : dict   player dict
    phase  : str    "powerplay" | "middle" | "death"

    Returns
    -------
    list[str]   3 suggestion strings
    """
    bp = batter.get("profile", {})
    bwp = bowler.get("profile", {})
    bat_hand = bp.get("hand", "R")
    bowl_type = bwp.get("bowling_type", "pace")
    bat_sr = bp.get("sr", 130)
    death_sr = bp.get("death_sr", 140)

    hints = []

    if phase == "powerplay":
        if bat_sr > 150:
            hints.append("🛡️ Third man back — aggressive opener will target short balls")
        else:
            hints.append("🛡️ Slip + gully — new ball, induce edges early")
        if bowl_type == "pace":
            hints.append("📍 Fine leg up — control singles, protect boundary")
            hints.append("📍 Mid-off straight — target drives, set a trap")
        else:
            hints.append("📍 Short midwicket — spin in powerplay draws pull shots")
            hints.append("📍 Deep square leg — protect the sweep boundary")

    elif phase == "middle":
        if bat_hand == "L" and bowl_type in ("offspin", "legspin"):
            hints.append("🛡️ Backward point deep — left-hander vs spin targets cuts")
        else:
            hints.append("🛡️ Long-on + long-off — protect straight boundaries")
        hints.append("📍 Cow corner — batters target this zone in middle overs")
        if bowler.get("profile", {}).get("wkts", 0) and bowler["profile"]["wkts"] > 10:
            hints.append("📍 Slip in for wicket-taker — back their skill")
        else:
            hints.append("📍 Deep midwicket — save runs, build dot-ball pressure")

    else:  # death
        if death_sr > 180:
            hints.append("🛡️ Sweeper cover + deep point — death hitter targets off side")
            hints.append("📍 Long-on back — slog-sweep protection")
            hints.append("📍 Fine leg back on boundary — yorker plan needs protection")
        else:
            hints.append("🛡️ Third man up — squeeze runs, force risk")
            hints.append("📍 Long-off back — target is stumps, protect miscues")
            hints.append("📍 Deep square leg — protect pull & hook shots")

    return hints[:3]
