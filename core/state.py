"""
core/state.py
─────────────
Central session-state manager for PitchIQ.

All pages read from st.session_state — they never call live_data.py
directly.  state.py is the *single point of data mutation*.

Functions:
    init_state()                 — set defaults, called once on load
    load_match(match_id)         — full fetch + resolve + store
    refresh_live_score()         — re-fetch scorecard only (fast)
    get_batting_team_players()   — Playing 11 of batting side
    get_bowling_team_players()   — Playing 11 of bowling side
    get_bench_players(team)      — 4 bench players for impact sub
    get_selected_team_players()  — Players for the manually selected team
    get_selected_bench()         — Bench for the manually selected team
"""

from __future__ import annotations

import time
from datetime import datetime

import streamlit as st

from core.live_data import (
    fetch_live_matches,
    fetch_match_info,
    fetch_match_squad,
    fetch_scorecard,
)
from core.squad_resolver import (
    resolve_squad,
    resolve_team_id,
    detect_playing_11,
    detect_bench,
    update_squad_from_scorecard,
)
from core.engine import MatchState


# ═══════════════════════════════════════════════════════════════════════
# INIT
# ═══════════════════════════════════════════════════════════════════════

def init_state() -> None:
    """
    Initialise all session-state keys with safe defaults.

    Called once at the top of app.py.  Subsequent calls are no-ops
    for keys that already exist.
    """
    defaults = {
        "match": None,
        "match_id": None,
        "squad_a": [],
        "squad_b": [],
        "playing_11_a": [],
        "playing_11_b": [],
        "bench_a": [],
        "bench_b": [],
        "scorecard": [],
        "match_state": None,
        "last_updated": None,
        "current_page": "war_room",
        "session_notes": "",
        "auto_refresh": True,
        "debug_log": [],
        # Team selector: "batting" or "bowling" — coach picks perspective
        "selected_perspective": "batting",
        # Match mode: "live" or "manual"
        "match_mode": "live",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# ═══════════════════════════════════════════════════════════════════════
# LOAD MATCH
# ═══════════════════════════════════════════════════════════════════════

def load_match(match_id: str) -> None:
    """
    Full load: fetch info + squad + scorecard, resolve players, build
    MatchState, and store everything in session_state.

    Parameters
    ----------
    match_id : str   match identifier (e.g. "demo_rcb_csk_14")
    """
    st.session_state.match_id = match_id

    # ── Fetch all data ───────────────────────────────────────────────
    match_info = fetch_match_info(match_id)
    squad_data = fetch_match_squad(match_id)
    scorecard = fetch_scorecard(match_id)

    # ── Store match info ─────────────────────────────────────────────
    match_info["innings"] = scorecard
    match_info["squad_a"] = squad_data.get("squad_a", [])
    match_info["squad_b"] = squad_data.get("squad_b", [])
    st.session_state.match = match_info

    # ── Resolve squads ───────────────────────────────────────────────
    team_a_id = match_info.get("team_a", {}).get("id", "unk")
    team_b_id = match_info.get("team_b", {}).get("id", "unk")

    squad_a = resolve_squad(squad_data.get("squad_a", []), team_a_id)
    squad_b = resolve_squad(squad_data.get("squad_b", []), team_b_id)

    # Detect playing 11 from scorecard
    squad_a = detect_playing_11(scorecard, squad_a)
    squad_b = detect_playing_11(scorecard, squad_b)

    # Update squads with live scorecard data
    # Determine who is batting in the latest innings
    latest_innings = scorecard[-1] if scorecard else None
    if latest_innings:
        batting_team_id = latest_innings.get("batting_team", "")
        if batting_team_id == team_a_id:
            squad_a = update_squad_from_scorecard(squad_a, scorecard, is_batting=True)
            squad_b = update_squad_from_scorecard(squad_b, scorecard, is_batting=False)
        else:
            squad_b = update_squad_from_scorecard(squad_b, scorecard, is_batting=True)
            squad_a = update_squad_from_scorecard(squad_a, scorecard, is_batting=False)

    # ── Store squads ─────────────────────────────────────────────────
    st.session_state.squad_a = squad_a
    st.session_state.squad_b = squad_b
    st.session_state.playing_11_a = [p for p in squad_a if p.get("is_playing_11")]
    st.session_state.playing_11_b = [p for p in squad_b if p.get("is_playing_11")]
    st.session_state.bench_a = detect_bench(squad_a)
    st.session_state.bench_b = detect_bench(squad_b)
    st.session_state.scorecard = scorecard

    # ── Build MatchState ─────────────────────────────────────────────
    _build_match_state(match_info, scorecard)

    st.session_state.last_updated = time.time()


# ═══════════════════════════════════════════════════════════════════════
# MANUAL MATCH ENTRY (when API tokens exhausted)
# ═══════════════════════════════════════════════════════════════════════

def load_manual_match(
    team_a_id: str,
    team_b_id: str,
    batting_team_id: str,
    runs: int,
    wickets: int,
    overs: float,
    innings: int,
    target: int | None = None,
) -> None:
    """
    Build a full match from manual coach input using our player database.

    This is the offline fallback when API tokens are exhausted.  The coach
    picks two teams, enters the current score, and selects whether batting
    first or chasing — PitchIQ does the rest.

    Parameters
    ----------
    team_a_id      : str         team id (e.g. "rr")
    team_b_id      : str         team id (e.g. "kkr")
    batting_team_id: str         which team is currently batting
    runs           : int         current score
    wickets        : int         wickets fallen
    overs          : float       overs completed (e.g. 13.2)
    innings        : int         1 or 2
    target         : int | None  target score if chasing (innings=2)
    """
    from data.teams_db import get_team
    from data.player_profiles import PLAYER_PROFILES

    team_a = get_team(team_a_id)
    team_b = get_team(team_b_id)

    if not team_a or not team_b:
        return

    # ── Build raw squads from teams_db player lists ───────────────────
    def _build_raw_squad(team: dict) -> list[dict]:
        players = team.get("players", [])
        raw_squad = []
        for i, pname in enumerate(players):
            prof = PLAYER_PROFILES.get(pname, {})
            raw_squad.append({
                "name": pname,
                "role": prof.get("role", "bat"),
                "is_playing_11": i < 11,  # first 11 are playing
            })
        return raw_squad

    raw_squad_a = _build_raw_squad(team_a)
    raw_squad_b = _build_raw_squad(team_b)

    # ── Determine batting / bowling ──────────────────────────────────
    if batting_team_id == team_a_id:
        batting_team = team_a
        bowling_team = team_b
    else:
        batting_team = team_b
        bowling_team = team_a

    # ── Build scorecard ──────────────────────────────────────────────
    scorecard = []
    if innings == 2 and target:
        # First innings (completed) — the bowling team batted first
        scorecard.append({
            "inning_number": 1,
            "batting_team": bowling_team["id"],
            "bowling_team": batting_team["id"],
            "runs": target - 1,
            "wickets": 6,
            "overs": 20.0,
            "target": None,
            "batters": [],
            "bowlers": [],
            "last_6_balls": [],
        })

    # Current innings
    scorecard.append({
        "inning_number": innings,
        "batting_team": batting_team_id,
        "bowling_team": bowling_team["id"],
        "runs": runs,
        "wickets": wickets,
        "overs": overs,
        "target": target,
        "batters": [],
        "bowlers": [],
        "last_6_balls": [],
    })

    # ── Build match info ─────────────────────────────────────────────
    match_id = f"manual_{team_a_id}_{team_b_id}"
    match_info = {
        "id": match_id,
        "title": f"{team_a.get('short', '')} vs {team_b.get('short', '')}, Manual Entry",
        "status": "live",
        "source": "manual",
        "venue": team_a.get("home_venue", ""),
        "toss": "",
        "team_a": {
            "id": team_a["id"],
            "name": team_a["name"],
            "short": team_a["short"],
            "color": team_a["color"],
        },
        "team_b": {
            "id": team_b["id"],
            "name": team_b["name"],
            "short": team_b["short"],
            "color": team_b["color"],
        },
        "innings": scorecard,
        "squad_a": raw_squad_a,
        "squad_b": raw_squad_b,
    }

    # ── Store everything ─────────────────────────────────────────────
    st.session_state.match_id = match_id
    st.session_state.match = match_info

    squad_a = resolve_squad(raw_squad_a, team_a_id)
    squad_b = resolve_squad(raw_squad_b, team_b_id)

    st.session_state.squad_a = squad_a
    st.session_state.squad_b = squad_b
    st.session_state.playing_11_a = [p for p in squad_a if p.get("is_playing_11")]
    st.session_state.playing_11_b = [p for p in squad_b if p.get("is_playing_11")]
    st.session_state.bench_a = detect_bench(squad_a)
    st.session_state.bench_b = detect_bench(squad_b)
    st.session_state.scorecard = scorecard

    _build_match_state(match_info, scorecard)
    st.session_state.last_updated = time.time()


def _build_match_state(match_info: dict, scorecard: list[dict]) -> None:
    """
    Construct a MatchState from the latest innings data.

    Parameters
    ----------
    match_info : dict
    scorecard  : list[dict]
    """
    if not scorecard:
        st.session_state.match_state = MatchState()
        return

    latest = scorecard[-1]
    batting_team_key = latest.get("batting_team", "")
    bowling_team_key = latest.get("bowling_team", "")

    team_a = match_info.get("team_a", {})
    team_b = match_info.get("team_b", {})

    if batting_team_key == team_a.get("id", ""):
        batting_team = team_a
        bowling_team = team_b
    elif batting_team_key == team_b.get("id", ""):
        batting_team = team_b
        bowling_team = team_a
    else:
        # Guess based on innings number
        if len(scorecard) <= 1:
            batting_team = team_a
            bowling_team = team_b
        else:
            batting_team = team_b
            bowling_team = team_a

    ms = MatchState(
        batting_team=batting_team,
        bowling_team=bowling_team,
        runs=latest.get("runs", 0),
        wickets=latest.get("wickets", 0),
        overs=float(latest.get("overs", 0.0)),
        target=latest.get("target"),
        venue_name=match_info.get("venue", ""),
        innings_number=latest.get("inning_number", len(scorecard)),
    )
    st.session_state.match_state = ms


# ═══════════════════════════════════════════════════════════════════════
# REFRESH
# ═══════════════════════════════════════════════════════════════════════

def refresh_live_score() -> None:
    """
    Re-fetch scorecard only (fast, called every ~30 s).

    Updates: dismissed flags, overs_bowled, runs, wickets.
    Recalculates match_state.
    """
    match_id = st.session_state.get("match_id")
    if not match_id:
        return

    scorecard = fetch_scorecard(match_id)
    match_info = st.session_state.get("match", {})

    if scorecard:
        st.session_state.scorecard = scorecard
        if match_info:
            match_info["innings"] = scorecard

        # Re-resolve squad stats from updated scorecard
        team_a_id = match_info.get("team_a", {}).get("id", "")
        latest = scorecard[-1] if scorecard else {}
        batting_team_id = latest.get("batting_team", "")

        if batting_team_id == team_a_id:
            st.session_state.squad_a = update_squad_from_scorecard(
                st.session_state.squad_a, scorecard, is_batting=True)
            st.session_state.squad_b = update_squad_from_scorecard(
                st.session_state.squad_b, scorecard, is_batting=False)
        else:
            st.session_state.squad_b = update_squad_from_scorecard(
                st.session_state.squad_b, scorecard, is_batting=True)
            st.session_state.squad_a = update_squad_from_scorecard(
                st.session_state.squad_a, scorecard, is_batting=False)

        # Update playing 11 lists
        st.session_state.playing_11_a = [
            p for p in st.session_state.squad_a if p.get("is_playing_11")]
        st.session_state.playing_11_b = [
            p for p in st.session_state.squad_b if p.get("is_playing_11")]

        # Rebuild match state
        _build_match_state(match_info, scorecard)

    st.session_state.last_updated = time.time()


# ═══════════════════════════════════════════════════════════════════════
# GETTERS
# ═══════════════════════════════════════════════════════════════════════

def get_batting_team_players() -> list[dict]:
    """
    Return Playing 11 of the currently batting team.

    Dismissed flags are already set from the scorecard.

    Returns
    -------
    list[dict]   player dicts with is_playing_11=True on batting side.
    """
    ms = st.session_state.get("match_state")
    if not ms:
        return []

    batting_id = ms.batting_team.get("id", "")
    match = st.session_state.get("match", {})

    if batting_id == match.get("team_a", {}).get("id", ""):
        return st.session_state.get("playing_11_a", [])
    return st.session_state.get("playing_11_b", [])


def get_bowling_team_players() -> list[dict]:
    """
    Return Playing 11 of the currently bowling team.

    overs_bowled is already set from the scorecard.

    Returns
    -------
    list[dict]
    """
    ms = st.session_state.get("match_state")
    if not ms:
        return []

    bowling_id = ms.bowling_team.get("id", "")
    match = st.session_state.get("match", {})

    if bowling_id == match.get("team_a", {}).get("id", ""):
        return st.session_state.get("playing_11_a", [])
    return st.session_state.get("playing_11_b", [])


def get_bench_players(team: str = "batting") -> list[dict]:
    """
    Return bench players (Playing 15 minus Playing 11) for the
    specified team.

    Parameters
    ----------
    team : str   "batting" or "bowling"

    Returns
    -------
    list[dict]   typically 4 players.
    """
    ms = st.session_state.get("match_state")
    if not ms:
        return []

    match = st.session_state.get("match", {})

    if team == "batting":
        target_id = ms.batting_team.get("id", "")
    else:
        target_id = ms.bowling_team.get("id", "")

    if target_id == match.get("team_a", {}).get("id", ""):
        return st.session_state.get("bench_a", [])
    return st.session_state.get("bench_b", [])


def get_selected_team_players() -> list[dict]:
    """
    Return Playing 11 for whichever team the coach has selected
    in the sidebar (batting or bowling perspective).

    Returns
    -------
    list[dict]
    """
    perspective = st.session_state.get("selected_perspective", "batting")
    if perspective == "batting":
        return get_batting_team_players()
    return get_bowling_team_players()


def get_selected_bench() -> list[dict]:
    """
    Return bench players for whichever team the coach has selected.

    Returns
    -------
    list[dict]
    """
    perspective = st.session_state.get("selected_perspective", "batting")
    return get_bench_players(perspective)
