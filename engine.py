"""
core/engine.py
--------------
All analytical logic for PitchIQ.
No external API calls — pure cricket intelligence.
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Optional
from data.teams_db import TEAMS, VENUES


# ── Data models ────────────────────────────────────────────────────────────────
@dataclass
class MatchState:
    batting_id:   str
    bowling_id:   str
    runs:         int
    wickets:      int
    overs:        float
    target:       int          = 0
    venue_name:   str          = "Wankhede, Mumbai"
    phase:        str          = field(init=False)
    balls_faced:  int          = field(init=False)
    balls_left:   int          = field(init=False)
    crr:          float        = field(init=False)
    rrr:          float        = field(init=False)
    is_chasing:   bool         = field(init=False)
    proj_score:   int          = field(init=False)

    def __post_init__(self):
        self.phase       = _phase(self.overs)
        self.balls_faced = round(self.overs * 6)
        self.balls_left  = max(0, 120 - self.balls_faced)
        self.crr         = round(self.runs / self.overs, 2) if self.overs > 0 else 0.0
        self.is_chasing  = self.target > 0
        needed           = max(0, self.target - self.runs)
        self.rrr         = round(needed / self.balls_left * 6, 2) if self.balls_left > 0 else 0.0
        self.proj_score  = round(self.runs + self.crr * (20 - self.overs))


# ── Win probability ────────────────────────────────────────────────────────────
def win_probability(ms: MatchState) -> tuple[float, float]:
    """Returns (batting_team_prob, bowling_team_prob)."""
    team  = TEAMS[ms.batting_id]
    venue = VENUES[ms.venue_name]

    if ms.is_chasing:
        if ms.runs >= ms.target:   return (0.98, 0.02)
        if ms.wickets >= 10:       return (0.02, 0.98)
        prob = team["chase_win"]
        prob -= (ms.rrr - 8.0) * 0.042
        prob -= ms.wickets * 0.032
        prob += (venue["avg"] - 170) / 220
        # phase adjustment
        if ms.overs <= 6:   prob += 0.02
        elif ms.overs > 15: prob -= 0.04
        if venue["dew"]:    prob += 0.03
    else:
        proj   = ms.proj_score
        prob   = 0.50 + (proj - venue["avg"]) / 280
        prob  -= ms.wickets * 0.038
        if venue["dew"]: prob += 0.03

    prob = round(min(0.95, max(0.05, prob)), 4)
    return prob, round(1 - prob, 4)


# ── Pressure index ─────────────────────────────────────────────────────────────
def pressure_index(ms: MatchState) -> dict:
    """0–100 score with label + colour hint."""
    if ms.is_chasing:
        score = min(100, round(ms.rrr * 9 + ms.wickets * 4.5))
    else:
        score = round((ms.wickets / 3) * 28 + max(0, 8 - ms.crr) * 5)

    score = max(0, min(100, score))
    if score >= 70:
        return {"score": score, "label": "Critical",  "color": "#ef4444"}
    if score >= 40:
        return {"score": score, "label": "Elevated",  "color": "#f59e0b"}
    return     {"score": score, "label": "Controlled","color": "#4caf7d"}


# ── Batting order recommendation ───────────────────────────────────────────────
def batting_order_recommendation(ms: MatchState, available_batters: list[dict]) -> list[dict]:
    """
    Rank available (not yet out) batters for the current situation.
    Returns sorted list with rationale per player.
    """
    scored = []
    for b in available_batters:
        score = _batter_situational_score(b, ms)
        rationale = _batter_rationale(b, ms, score)
        scored.append({**b, "situation_score": score, "rationale": rationale})
    return sorted(scored, key=lambda x: x["situation_score"], reverse=True)

def _batter_situational_score(b: dict, ms: MatchState) -> float:
    score = b.get("form", 70) * 0.30

    # Phase weight: powerplay needs aggressive openers
    if ms.phase == "Powerplay":
        score += b.get("sr", 130) * 0.30 + b.get("avg", 30) * 0.10
    elif ms.phase == "Death overs":
        score += b.get("sr", 130) * 0.40 + b.get("death_sr", b.get("sr", 130)) * 0.20
    else:
        score += b.get("avg", 30) * 0.25 + b.get("sr", 130) * 0.15

    # Chase pressure: prefer experienced chasers
    if ms.is_chasing and ms.rrr > 9:
        score += b.get("chase_sr", b.get("sr", 130)) * 0.20

    # Wickets — protect tail if many wickets down
    if ms.wickets >= 7:
        score += b.get("lower_order_score", 0) * 0.15

    return round(score, 1)

def _batter_rationale(b: dict, ms: MatchState, score: float) -> str:
    parts = []
    if ms.phase == "Powerplay":
        parts.append(f"SR {b.get('sr', 0)} suits powerplay aggression")
    elif ms.phase == "Death overs":
        parts.append(f"Death-over specialist (SR {b.get('death_sr', b.get('sr', 0))})")
    else:
        parts.append(f"Avg {b.get('avg', 0)} builds stability in middle overs")
    if ms.is_chasing and ms.rrr > 9:
        parts.append(f"Can up the ante with RRR at {ms.rrr}")
    if b.get("form", 70) >= 80:
        parts.append("in excellent form this season")
    return "; ".join(parts) + "."


# ── Bowling plan ───────────────────────────────────────────────────────────────
def bowling_plan(ms: MatchState, available_bowlers: list[dict], batters_at_crease: list[dict]) -> list[dict]:
    """
    For each upcoming over, recommend a bowler + line/length.
    Returns list of over-by-over plans.
    """
    plans = []
    overs_remaining = int(20 - ms.overs)
    for i in range(min(overs_remaining, 6)):   # show next 6 overs
        over_num = int(ms.overs) + i + 1
        bowler, reasoning, line = _pick_bowler(available_bowlers, batters_at_crease, over_num, ms)
        plans.append({
            "over":      over_num,
            "bowler":    bowler,
            "line":      line,
            "reasoning": reasoning,
        })
    return plans

def _pick_bowler(bowlers, batters, over_num, ms):
    # Death: pace bowler with lowest economy
    if over_num >= 17:
        pace = [b for b in bowlers if b.get("type") in ("pace", "fast-medium")]
        if pace:
            best = min(pace, key=lambda b: b.get("death_econ", b.get("econ", 9)))
            return best["name"], f"Best death economy ({best.get('death_econ', best.get('econ','?'))}). Yorker-heavy plan.", "Yorker / low full toss"
    # Powerplay: swing/seam
    if over_num <= 6:
        swing = [b for b in bowlers if b.get("type") in ("pace", "swing")]
        if swing:
            best = min(swing, key=lambda b: b.get("econ", 9))
            return best["name"], f"Powerplay pace with economy {best.get('econ','?')}. Use swing & seam.", "Good length / outswinger"
    # Middle: spin if right-hander, or best economy
    righties = [b for b in batters if b.get("hand", "R") == "R"]
    if righties and over_num <= 15:
        spinners = [b for b in bowlers if b.get("type") in ("spin", "leg-spin", "off-spin")]
        if spinners:
            best = min(spinners, key=lambda b: b.get("econ", 9))
            return best["name"], f"Right-handers at crease — {best['name']} exploits off-stump channel.", "Off-stump / slightly shorter"
    # Generic best economy
    if bowlers:
        best = min(bowlers, key=lambda b: b.get("econ", 9))
        return best["name"], f"Best economy bowler available ({best.get('econ','?')}).", "Good length"
    return "TBD", "Evaluate squad options.", "Good length"


# ── Matchup matrix ─────────────────────────────────────────────────────────────
def matchup_matrix(batters: list[dict], bowlers: list[dict]) -> list[dict]:
    """
    For each batter × bowler pair, compute advantage score.
    Returns flat list sorted by threat level (batter advantage first).
    """
    rows = []
    for bat in batters:
        for bwl in bowlers:
            adv = _matchup_score(bat, bwl)
            rows.append({
                "batter":    bat["name"],
                "bowler":    bwl["name"],
                "advantage": adv,           # +ve = batter wins, -ve = bowler wins
                "label":     _matchup_label(adv),
                "tip":       _matchup_tip(bat, bwl, adv),
            })
    return sorted(rows, key=lambda x: x["advantage"], reverse=True)

def _matchup_score(bat, bwl):
    score = 0
    # handedness vs spin type
    if bat.get("hand") == "R" and bwl.get("type") == "off-spin":
        score -= 8   # off-spin into right-hander
    if bat.get("hand") == "L" and bwl.get("type") == "leg-spin":
        score -= 8
    if bat.get("hand") == "R" and bwl.get("type") == "leg-spin":
        score += 6
    # pace vs form
    score += (bat.get("form", 70) - 70) * 0.3
    score -= (bwl.get("form", 70) - 70) * 0.3
    # sr advantage
    score += (bat.get("sr", 130) - 130) * 0.05
    return round(score, 1)

def _matchup_label(adv):
    if adv >  8: return "Batter danger zone"
    if adv >  3: return "Slight batter edge"
    if adv > -3: return "Even contest"
    if adv > -8: return "Bowler has edge"
    return "Bowler dominates"

def _matchup_tip(bat, bwl, adv):
    if adv > 5:
        return f"Consider not bowling {bwl['name']} to {bat['name']} — high risk of boundaries."
    if adv < -5:
        return f"{bwl['name']} should target {bat['name']} aggressively — clear advantage."
    return f"Competitive matchup — field placement is the differentiator."


# ── Impact sub recommendation ──────────────────────────────────────────────────
def impact_sub_recommendation(ms: MatchState, squad: list[dict], players_used: list[str]) -> dict:
    """Recommend best impact substitute player and timing."""
    available = [p for p in squad if p["name"] not in players_used]
    if not available:
        return {"recommendation": "No substitutes remaining.", "player": None, "reason": ""}

    # Score each available sub for the situation
    scored = []
    for p in available:
        s = _impact_sub_score(p, ms)
        scored.append((s, p))
    scored.sort(reverse=True)

    best_score, best = scored[0]
    timing = _impact_sub_timing(ms)

    return {
        "player": best,
        "score":  best_score,
        "reason": _impact_sub_reason(best, ms),
        "timing": timing,
        "alternatives": [p for _, p in scored[1:3]],
    }

def _impact_sub_score(p, ms):
    score = p.get("form", 70)
    role  = p.get("role", "")
    if ms.is_chasing and ms.rrr > 9 and "bat" in role:
        score += 20
    if not ms.is_chasing and ms.phase == "Death overs" and "bowl" in role:
        score += 20
    if ms.wickets >= 6 and "bat" in role:
        score += 15
    return score

def _impact_sub_reason(p, ms):
    role = p.get("role", "player")
    if ms.is_chasing and ms.rrr > 9:
        return f"{p['name']} as batting reinforcement — required rate demands a big hitter."
    if ms.phase == "Death overs" and "bowl" in role:
        return f"{p['name']} as a death bowling specialist — protect the total."
    return f"{p['name']} brings {role} versatility to the current situation."

def _impact_sub_timing(ms):
    if ms.is_chasing and ms.rrr > 10:
        return "Bring in now — every ball counts at this required rate."
    if ms.phase == "Death overs":
        return f"Ideal window: start of over {int(ms.overs)+1}."
    return f"Recommended: over {int(ms.overs)+2} after next strategic break."


# ── Field placement hints ──────────────────────────────────────────────────────
def field_placement_hints(batter: dict, bowler: dict, phase: str) -> list[str]:
    hints = []
    hand = batter.get("hand", "R")
    btype = bowler.get("type", "pace")

    if btype in ("pace", "fast-medium"):
        if hand == "R":
            hints.append("Third slip + gully for early movement")
            hints.append("Fine leg up for the pull shot")
        else:
            hints.append("Gully + cover point for outside edge")
    elif btype in ("spin", "off-spin"):
        if hand == "R":
            hints.append("Slip + short leg — turn into right-hander")
            hints.append("Sweeper cover for the slog-sweep")
        else:
            hints.append("Cow corner + mid-wicket — left-hander's preferred arc")

    if phase == "Death overs":
        hints = ["Fine leg + deep square leg (slog protection)",
                 "Long-on + long-off (straight hit protection)",
                 "Third man up (ramp/upper-cut threat)"]
    return hints


# ── Utility ────────────────────────────────────────────────────────────────────
def _phase(overs: float) -> str:
    if overs <= 6:  return "Powerplay"
    if overs <= 15: return "Middle overs"
    return "Death overs"
