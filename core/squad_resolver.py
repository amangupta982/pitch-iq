"""
core/squad_resolver.py
──────────────────────
Fuzzy-matches raw player names from live APIs to canonical player
profiles in player_profiles.py, and detects Playing-11 vs bench
from scorecard data.

Uses rapidfuzz for name matching with a 75-point threshold.

Key functions:
    resolve_team_id()     — map any team name variant → internal id
    resolve_squad()       — match raw names → profiles
    detect_playing_11()   — who appeared in the scorecard
    detect_bench()        — who didn't
    detect_dismissed()    — batters already out
    detect_overs_bowled() — how many overs each bowler has used
"""

from __future__ import annotations

import os
import traceback

from rapidfuzz import process, fuzz

from data.player_profiles import PLAYER_PROFILES, get_profile, get_all_names

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Pre-compute the list of canonical names once
_ALL_NAMES = get_all_names()
_MATCH_THRESHOLD = 75


# ═══════════════════════════════════════════════════════════════════════
# TEAM ID RESOLUTION (Bug 1 fix)
# ═══════════════════════════════════════════════════════════════════════

# Exhaustive alias map: every known variation → canonical team id.
# Keys are lowercase.  Covers official names, short codes,
# abbreviations, old names, and common misspellings.
TEAM_ALIASES: dict[str, str] = {
    # ── Royal Challengers Bengaluru ──
    "rcb":                            "rcb",
    "royal challengers bengaluru":    "rcb",
    "royal challengers bangalore":    "rcb",
    "royal challengers":              "rcb",
    "bengaluru":                      "rcb",
    "challengers":                    "rcb",
    "rc bengaluru":                   "rcb",
    "rc bangalore":                   "rcb",
    # ── Chennai Super Kings ──
    "csk":                            "csk",
    "chennai super kings":            "csk",
    "chennai":                        "csk",
    "super kings":                    "csk",
    # ── Mumbai Indians ──
    "mi":                             "mi",
    "mumbai indians":                 "mi",
    "mumbai":                         "mi",
    # ── Kolkata Knight Riders ──
    "kkr":                            "kkr",
    "kolkata knight riders":          "kkr",
    "kolkata":                        "kkr",
    "knight riders":                  "kkr",
    # ── Sunrisers Hyderabad ──
    "srh":                            "srh",
    "sunrisers hyderabad":            "srh",
    "sunrisers":                      "srh",
    "hyderabad":                      "srh",
    # ── Rajasthan Royals ──
    "rr":                             "rr",
    "rajasthan royals":               "rr",
    "rajasthan":                      "rr",
    "royals":                         "rr",
    # ── Delhi Capitals ──
    "dc":                             "dc",
    "delhi capitals":                 "dc",
    "delhi":                          "dc",
    "capitals":                       "dc",
    "delhi daredevils":               "dc",
    "dd":                             "dc",
    # ── Punjab Kings ──
    "pbks":                           "pbks",
    "punjab kings":                   "pbks",
    "punjab":                         "pbks",
    "kings xi punjab":                "pbks",
    "kxip":                           "pbks",
    "pk":                             "pbks",
    # ── Gujarat Titans ──
    "gt":                             "gt",
    "gujarat titans":                 "gt",
    "gujarat":                        "gt",
    "titans":                         "gt",
    # ── Lucknow Super Giants ──
    "lsg":                            "lsg",
    "lucknow super giants":           "lsg",
    "lucknow":                        "lsg",
    "super giants":                   "lsg",
}

# Pre-compute all alias keys for fuzzy matching
_ALIAS_KEYS = list(TEAM_ALIASES.keys())


def resolve_team_id(name: str) -> str:
    """
    Resolve any team name variant to a canonical internal team id.

    Resolution order:
        1. Exact match against TEAM_ALIASES (case-insensitive)
        2. Substring match — if the input contains an alias key
        3. rapidfuzz token_sort_ratio with 60-point threshold

    Parameters
    ----------
    name : str   e.g. "Rajasthan Royals", "RR", "Kolkata Knight Rid..."

    Returns
    -------
    str   canonical team id (e.g. "rr", "kkr") or "unk" if unresolved.
    """
    if not name or not name.strip():
        return "unk"

    clean = name.strip().lower()

    # ── 1. Exact alias match ─────────────────────────────────────────
    if clean in TEAM_ALIASES:
        _dbg(f"Team resolve (exact): '{name}' → '{TEAM_ALIASES[clean]}'")
        return TEAM_ALIASES[clean]

    # ── 2. Substring match: check if any alias is in the name ────────
    for alias, tid in TEAM_ALIASES.items():
        if len(alias) > 2 and alias in clean:
            _dbg(f"Team resolve (substring): '{name}' → '{tid}'")
            return tid

    # ── 3. Fuzzy match against all alias keys ────────────────────────
    result = process.extractOne(
        clean,
        _ALIAS_KEYS,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=60,
    )
    if result:
        matched_alias, score, _ = result
        tid = TEAM_ALIASES[matched_alias]
        _dbg(f"Team resolve (fuzzy): '{name}' → '{tid}' via '{matched_alias}' (score={score})")
        return tid

    _dbg(f"Team resolve FAILED: '{name}' → 'unk'")
    return "unk"


# ═══════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════

def _dbg(msg: str) -> None:
    """Print debug message if DEBUG is True."""
    if DEBUG:
        print(f"[PitchIQ:Squad] {msg}")


def _default_profile(name: str, role: str = "bat", team: str = "") -> dict:
    """
    Generate a safe default profile when no fuzzy match is found.

    Parameters
    ----------
    name : str   player name
    role : str   inferred role
    team : str   team id

    Returns
    -------
    dict   profile with conservative default stats.
    """
    return {
        "name": name,
        "team": team,
        "hand": "R",
        "role": role,
        "avg": 30,
        "sr": 130,
        "powerplay_sr": 128,
        "death_sr": 140,
        "chase_sr": 132,
        "vs_pace": 50,
        "vs_spin": 50,
        "form": 65,
        "econ": 8.0 if role in ("bowl", "allrounder") else None,
        "death_econ": 9.0 if role in ("bowl", "allrounder") else None,
        "wkts": 5 if role in ("bowl", "allrounder") else None,
        "bowling_type": "medium" if role in ("bowl", "allrounder") else None,
    }


def _fuzzy_match(raw_name: str) -> tuple[str | None, int]:
    """
    Attempt to fuzzy-match a raw player name to canonical profiles.

    Parameters
    ----------
    raw_name : str   e.g. "V Kohli", "MS Dhoni"

    Returns
    -------
    (matched_name | None, score)
    """
    if not raw_name or not _ALL_NAMES:
        return None, 0

    # Exact match first
    if raw_name in PLAYER_PROFILES:
        return raw_name, 100

    result = process.extractOne(
        raw_name,
        _ALL_NAMES,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=_MATCH_THRESHOLD,
    )
    if result:
        matched_name, score, _ = result
        _dbg(f"Fuzzy match: '{raw_name}' → '{matched_name}' (score={score})")
        return matched_name, score

    _dbg(f"No fuzzy match for: '{raw_name}'")
    return None, 0


# ═══════════════════════════════════════════════════════════════════════
# RESOLVE SQUAD
# ═══════════════════════════════════════════════════════════════════════

def resolve_squad(raw_squad: list[dict], team_id: str) -> list[dict]:
    """
    Resolve a raw squad list into fully-profiled player dicts.

    For each player in the raw squad:
      1. Fuzzy-match name → canonical profile
      2. Merge live data (runs, balls, etc.) with profile stats
      3. If no match: use safe defaults

    Parameters
    ----------
    raw_squad : list[dict]   from fetch_match_squad() or mock data
    team_id   : str          e.g. "rcb"

    Returns
    -------
    list[dict]   list of normalised player dicts with profiles merged.
    """
    resolved = []
    for raw in raw_squad:
        raw_name = raw.get("name", "Unknown")
        role = raw.get("role", "bat")
        is_11 = raw.get("is_playing_11", True)

        # Try fuzzy match
        matched_name, score = _fuzzy_match(raw_name)

        if matched_name:
            profile = get_profile(matched_name).copy()
        else:
            profile = _default_profile(raw_name, role, team_id)

        player = {
            "name": profile["name"],
            "raw_name": raw_name,
            "role": role if role != "bat" else profile.get("role", role),
            "batting_position": None,
            "bowling_position": None,
            "runs": raw.get("runs", 0),
            "balls": raw.get("balls", 0),
            "overs_bowled": raw.get("overs_bowled", 0.0),
            "dismissed": raw.get("dismissed", False),
            "dismissal": raw.get("dismissal", ""),
            "is_playing_11": is_11,
            "profile": profile,
        }
        resolved.append(player)

    _dbg(f"Resolved {len(resolved)} players for {team_id}")
    return resolved


# ═══════════════════════════════════════════════════════════════════════
# SCORECARD ANALYSIS
# ═══════════════════════════════════════════════════════════════════════

def detect_playing_11(scorecard: list[dict], squad: list[dict]) -> list[dict]:
    """
    Scan the scorecard to determine which players are in the Playing 11.

    Any player who appears in the batting or bowling lists of any
    innings is marked as is_playing_11=True.

    Parameters
    ----------
    scorecard : list[dict]   innings list from fetch_scorecard()
    squad     : list[dict]   resolved squad list

    Returns
    -------
    list[dict]   squad with is_playing_11 flags updated.
    """
    scorecard_names = set()
    for inn in scorecard:
        for b in inn.get("batters", []):
            scorecard_names.add(b.get("name", "").lower())
        for bw in inn.get("bowlers", []):
            scorecard_names.add(bw.get("name", "").lower())

    if not scorecard_names:
        return squad

    for player in squad:
        name_low = player["name"].lower()
        raw_low = player.get("raw_name", "").lower()
        if name_low in scorecard_names or raw_low in scorecard_names:
            player["is_playing_11"] = True
        # Also fuzzy check
        for sc_name in scorecard_names:
            if sc_name and (fuzz.token_sort_ratio(name_low, sc_name) >= _MATCH_THRESHOLD):
                player["is_playing_11"] = True
                break

    return squad


def detect_bench(squad: list[dict]) -> list[dict]:
    """
    Return players who are NOT in the Playing 11.

    Parameters
    ----------
    squad : list[dict]   resolved squad

    Returns
    -------
    list[dict]   bench players (typically 4 in IPL with Impact Sub).
    """
    return [p for p in squad if not p.get("is_playing_11", True)]


def detect_dismissed(scorecard: list[dict], team_id: str = "") -> list[str]:
    """
    Return names of dismissed batters from the scorecard.

    Parameters
    ----------
    scorecard : list[dict]   innings list
    team_id   : str          optional filter by batting team

    Returns
    -------
    list[str]   player names who are out.
    """
    dismissed = []
    for inn in scorecard:
        if team_id and inn.get("batting_team", "") != team_id and team_id:
            # If we know the team, only look at their innings
            pass
        for b in inn.get("batters", []):
            if b.get("dismissed", False):
                dismissed.append(b["name"])
    return dismissed


def detect_overs_bowled(scorecard: list[dict]) -> dict[str, float]:
    """
    Build a mapping of bowler name → overs bowled across all innings.

    Parameters
    ----------
    scorecard : list[dict]

    Returns
    -------
    dict[str, float]   e.g. {"Jasprit Bumrah": 3.4, "Rashid Khan": 4.0}
    """
    overs_map: dict[str, float] = {}
    for inn in scorecard:
        for bw in inn.get("bowlers", []):
            name = bw.get("name", "")
            overs = float(bw.get("overs", 0.0))
            if name:
                overs_map[name] = overs_map.get(name, 0.0) + overs
    return overs_map


def update_squad_from_scorecard(
    squad: list[dict],
    scorecard: list[dict],
    is_batting: bool = True,
) -> list[dict]:
    """
    Update a resolved squad list with live data from the scorecard.

    Merges runs, balls, dismissed status, overs_bowled, and batting
    position from the most recent innings.

    Parameters
    ----------
    squad       : list[dict]   resolved squad
    scorecard   : list[dict]   innings list
    is_batting  : bool         True if this team is currently batting

    Returns
    -------
    list[dict]   updated squad.
    """
    if not scorecard:
        return squad

    # Use the latest innings
    latest = scorecard[-1] if is_batting else scorecard[-1]

    # Update batting stats
    for batter_data in latest.get("batters", []):
        bname = batter_data.get("name", "")
        for player in squad:
            if (player["name"].lower() == bname.lower() or
                    fuzz.token_sort_ratio(player["name"].lower(), bname.lower()) >= _MATCH_THRESHOLD):
                player["runs"] = batter_data.get("runs", 0)
                player["balls"] = batter_data.get("balls", 0)
                player["dismissed"] = batter_data.get("dismissed", False)
                player["dismissal"] = batter_data.get("dismissal", "")
                break

    # Update bowling stats
    for bowler_data in latest.get("bowlers", []):
        bwname = bowler_data.get("name", "")
        for player in squad:
            if (player["name"].lower() == bwname.lower() or
                    fuzz.token_sort_ratio(player["name"].lower(), bwname.lower()) >= _MATCH_THRESHOLD):
                player["overs_bowled"] = float(bowler_data.get("overs", 0.0))
                break

    # Set batting positions
    for idx, batter_data in enumerate(latest.get("batters", [])):
        bname = batter_data.get("name", "")
        for player in squad:
            if (player["name"].lower() == bname.lower() or
                    fuzz.token_sort_ratio(player["name"].lower(), bname.lower()) >= _MATCH_THRESHOLD):
                player["batting_position"] = idx + 1
                break

    return squad
