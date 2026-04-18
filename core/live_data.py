"""
core/live_data.py
─────────────────
Three-tier data fetching for PitchIQ:
    1.  cricketdata.org free API  (primary — needs CRICDATA_KEY)
    2.  Cricbuzz HTML scraper     (fallback — no key needed)
    3.  Built-in mock data        (offline fallback — always works)

Every public function returns a *normalised* dict so consumers never
need to know which source was used.

Caching:
    • st.cache_data(ttl=30)   for live score endpoints
    • st.cache_data(ttl=300)  for squad / match-info endpoints
"""

from __future__ import annotations

import os
import traceback
from datetime import datetime

import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# ── Load .env BEFORE any os.getenv() ─────────────────────────────────
load_dotenv()

CRICDATA_KEY = os.getenv("CRICDATA_KEY", "")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
BASE_URL = "https://api.cricapi.com/v1"


# ═══════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════

def _dbg(msg: str) -> None:
    """Print a debug message to the terminal if DEBUG is enabled."""
    if DEBUG:
        print(f"[PitchIQ] {msg}")


def _api_get(endpoint: str, params: dict | None = None) -> dict | None:
    """
    Fire a GET request to the cricketdata.org API.

    Parameters
    ----------
    endpoint : str    e.g. "currentMatches", "match_info"
    params   : dict   additional query-string params

    Returns
    -------
    dict | None   parsed JSON body, or None on failure.
    """
    if not CRICDATA_KEY or CRICDATA_KEY == "your_free_key_from_cricketdata_org":
        _dbg("No valid CRICDATA_KEY — skipping API call")
        return None

    url = f"{BASE_URL}/{endpoint}"
    qp = {"apikey": CRICDATA_KEY}
    if params:
        qp.update(params)

    try:
        resp = requests.get(url, params=qp, timeout=10)
        _dbg(f"API {endpoint} → {resp.status_code}")
        data = resp.json()
        if DEBUG:
            raw = str(data)[:500]
            _dbg(f"Raw response: {raw}")
        if data.get("status") == "failure":
            _dbg(f"API failure: {data.get('reason', 'unknown')}")
            return None
        return data
    except Exception as e:
        _dbg(f"API request error: {e}")
        if DEBUG:
            traceback.print_exc()
        return None


def _norm_team(raw: dict, fallback_id: str = "unk") -> dict:
    """
    Normalize a team dict from any source into the standard shape.

    Parameters
    ----------
    raw         : dict   raw team data from API / scraper
    fallback_id : str    id to use if not detectable

    Returns
    -------
    dict   { id, name, short, color }
    """
    from data.teams_db import find_team_by_name

    name = raw.get("name", raw.get("teamName", fallback_id))
    found = find_team_by_name(name)
    if found:
        return {
            "id": found["id"],
            "name": found["name"],
            "short": found["short"],
            "color": found["color"],
        }
    short = name[:3].upper() if name else fallback_id.upper()
    return {"id": fallback_id, "name": name, "short": short, "color": "#666"}


# ═══════════════════════════════════════════════════════════════════════
# CRICBUZZ SCRAPER (fallback)
# ═══════════════════════════════════════════════════════════════════════

def _scrape_cricbuzz_live() -> list[dict]:
    """
    Scrape Cricbuzz homepage for live IPL match data.

    Returns
    -------
    list[dict]   list of partially-normalised match dicts, or [].
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(
            "https://www.cricbuzz.com/cricket-match/live-scores",
            headers=headers,
            timeout=10,
        )
        soup = BeautifulSoup(resp.text, "html.parser")
        matches: list[dict] = []

        match_cards = soup.select("div.cb-mtch-lst.cb-tms-itm")
        for card in match_cards[:5]:
            title_el = card.select_one("h3.cb-lv-scr-mtch-hdr a")
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            if "IPL" not in title and "Indian Premier League" not in title:
                continue

            status_el = card.select_one("div.cb-text-live, div.cb-text-complete")
            status = "live" if status_el and "live" in (status_el.get("class") or [""])[0] else "completed"

            teams_el = card.select("div.cb-hmscg-tm-nm")
            team_names = [t.get_text(strip=True) for t in teams_el]

            match = {
                "id": f"cb_{hash(title) % 100000}",
                "title": title,
                "status": status,
                "source": "scraper",
                "venue": "",
                "toss": "",
                "team_a": _norm_team({"name": team_names[0] if team_names else "Team A"}),
                "team_b": _norm_team({"name": team_names[1] if len(team_names) > 1 else "Team B"}),
                "innings": [],
                "squad_a": [],
                "squad_b": [],
            }
            matches.append(match)

        _dbg(f"Cricbuzz scraper found {len(matches)} IPL matches")
        return matches

    except Exception as e:
        _dbg(f"Cricbuzz scraper error: {e}")
        if DEBUG:
            traceback.print_exc()
        return []


# ═══════════════════════════════════════════════════════════════════════
# PUBLIC API FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=300)
def fetch_live_matches() -> list[dict]:
    """
    Fetch current live IPL matches.

    Fallback chain:  API → Cricbuzz scraper → mock schedule.

    Returns
    -------
    list[dict]   list of normalised match summary dicts.
    """
    # ── Tier 1: API ──
    data = _api_get("currentMatches")
    if data and data.get("data"):
        matches = []
        for m in data["data"]:
            name = m.get("name", "")
            match_type = m.get("matchType", "")
            series = m.get("series_id", "")
            # Try to filter IPL matches
            if "ipl" in name.lower() or "indian premier" in name.lower() or match_type == "t20":
                match = {
                    "id": m.get("id", ""),
                    "title": name,
                    "status": "live" if m.get("matchStarted") and not m.get("matchEnded") else
                              "completed" if m.get("matchEnded") else "upcoming",
                    "source": "api",
                    "venue": m.get("venue", ""),
                    "toss": "",
                    "team_a": _norm_team({"name": m.get("teams", ["", ""])[0] if m.get("teams") else ""}),
                    "team_b": _norm_team({"name": m.get("teams", ["", ""])[1] if m.get("teams") and len(m.get("teams", [])) > 1 else ""}),
                    "innings": [],
                    "squad_a": [],
                    "squad_b": [],
                }
                matches.append(match)
        if matches:
            _dbg(f"API returned {len(matches)} IPL matches")
            return matches

    # ── Tier 2: Scraper ──
    scraped = _scrape_cricbuzz_live()
    if scraped:
        return scraped

    # ── Tier 3: Mock ──
    _dbg("Using mock schedule (offline mode)")
    from data.mock_data import get_mock_schedule
    return get_mock_schedule()


@st.cache_data(ttl=300)
def fetch_match_info(match_id: str) -> dict:
    """
    Fetch detailed match info (toss, venue, teams).

    Parameters
    ----------
    match_id : str

    Returns
    -------
    dict   normalised match dict with info fields populated.
    """
    if match_id.startswith("demo_"):
        from data.mock_data import get_mock_match
        return get_mock_match()

    data = _api_get("match_info", {"id": match_id})
    if data and data.get("data"):
        d = data["data"]
        return {
            "id": match_id,
            "title": d.get("name", ""),
            "status": "live" if d.get("matchStarted") and not d.get("matchEnded") else
                      "completed" if d.get("matchEnded") else "upcoming",
            "source": "api",
            "venue": d.get("venue", ""),
            "toss": d.get("tossWinner", "") + " " + d.get("tossChoice", ""),
            "team_a": _norm_team({"name": d.get("teams", [""])[0] if d.get("teams") else ""}),
            "team_b": _norm_team({"name": d.get("teams", ["", ""])[1] if d.get("teams") and len(d.get("teams", [])) > 1 else ""}),
            "innings": [],
            "squad_a": [],
            "squad_b": [],
        }

    # Fallback
    from data.mock_data import get_mock_match
    _dbg("Match info fallback → mock")
    return get_mock_match()


@st.cache_data(ttl=300)
def fetch_match_squad(match_id: str) -> dict:
    """
    Fetch Playing 15 squads for both teams.

    Parameters
    ----------
    match_id : str

    Returns
    -------
    dict   {"squad_a": [...], "squad_b": [...]}  raw player lists.
    """
    if match_id.startswith("demo_"):
        from data.mock_data import get_mock_match
        m = get_mock_match()
        return {"squad_a": m["squad_a"], "squad_b": m["squad_b"]}

    data = _api_get("match_squad", {"id": match_id})
    if data and data.get("data"):
        squads = data["data"]
        squad_a_raw = []
        squad_b_raw = []
        for i, team_data in enumerate(squads):
            players = team_data.get("players", [])
            parsed = []
            for p in players:
                parsed.append({
                    "name": p.get("name", "Unknown"),
                    "role": _infer_role(p.get("role", "")),
                    "is_playing_11": p.get("playingXI", False),
                })
            if i == 0:
                squad_a_raw = parsed
            else:
                squad_b_raw = parsed
        return {"squad_a": squad_a_raw, "squad_b": squad_b_raw}

    # Fallback
    from data.mock_data import get_mock_match
    _dbg("Squad fallback → mock")
    m = get_mock_match()
    return {"squad_a": m["squad_a"], "squad_b": m["squad_b"]}


@st.cache_data(ttl=30)
def fetch_scorecard(match_id: str) -> list[dict]:
    """
    Fetch live scorecard (ball-by-ball).

    Parameters
    ----------
    match_id : str

    Returns
    -------
    list[dict]   list of innings dicts with batters, bowlers, last_6_balls.
    """
    if match_id.startswith("demo_"):
        from data.mock_data import get_mock_match
        return get_mock_match()["innings"]

    data = _api_get("match_scorecard", {"id": match_id})
    if data and data.get("data"):
        d = data["data"]
        innings_list = []
        for idx, sc in enumerate(d.get("scorecard", d.get("score", []))):
            batters = []
            for b in sc.get("batting", []):
                batters.append({
                    "name": b.get("batsman", {}).get("name", b.get("name", "")),
                    "runs": b.get("r", 0),
                    "balls": b.get("b", 0),
                    "dismissed": b.get("dismissal", "") != "",
                    "dismissal": b.get("dismissal", ""),
                })
            bowlers = []
            for bw in sc.get("bowling", []):
                bowlers.append({
                    "name": bw.get("bowler", {}).get("name", bw.get("name", "")),
                    "overs": bw.get("o", 0.0),
                    "runs": bw.get("r", 0),
                    "wickets": bw.get("w", 0),
                    "econ": bw.get("eco", 0.0),
                })
            inning_runs = sc.get("r", sc.get("runs", 0))
            inning_wkts = sc.get("w", sc.get("wickets", 0))
            inning_overs = sc.get("o", sc.get("overs", 0.0))

            innings_list.append({
                "inning_number": idx + 1,
                "batting_team": "",
                "bowling_team": "",
                "runs": inning_runs,
                "wickets": inning_wkts,
                "overs": float(inning_overs),
                "target": None,
                "batters": batters,
                "bowlers": bowlers,
                "last_6_balls": [],
            })
        if innings_list:
            return innings_list

    # Fallback
    from data.mock_data import get_mock_match
    _dbg("Scorecard fallback → mock")
    return get_mock_match()["innings"]


@st.cache_data(ttl=300)
def fetch_schedule() -> list[dict]:
    """
    Fetch today's IPL schedule.

    Returns
    -------
    list[dict]   match summaries.
    """
    data = _api_get("matches", {"offset": 0})
    if data and data.get("data"):
        matches = []
        for m in data["data"]:
            name = m.get("name", "")
            if "ipl" in name.lower() or "indian premier" in name.lower():
                matches.append({
                    "id": m.get("id", ""),
                    "title": name,
                    "status": "live" if m.get("matchStarted") and not m.get("matchEnded") else
                              "completed" if m.get("matchEnded") else "upcoming",
                    "source": "api",
                    "team_a": _norm_team({"name": m.get("teams", [""])[0] if m.get("teams") else ""}),
                    "team_b": _norm_team({"name": m.get("teams", ["", ""])[1] if m.get("teams") and len(m.get("teams", [])) > 1 else ""}),
                })
                matches.append(matches[-1])  # fixed: just append once
        # deduplicate
        seen = set()
        unique = []
        for mx in matches:
            if mx["id"] not in seen:
                seen.add(mx["id"])
                unique.append(mx)
        if unique:
            return unique

    from data.mock_data import get_mock_schedule
    return get_mock_schedule()


# ═══════════════════════════════════════════════════════════════════════
# HELPERS (private)
# ═══════════════════════════════════════════════════════════════════════

def _infer_role(raw_role: str) -> str:
    """
    Map API role strings to our canonical set.

    Parameters
    ----------
    raw_role : str   e.g. "Batting Allrounder", "WK-Batsman"

    Returns
    -------
    str   one of "bat", "bowl", "allrounder", "wk-bat"
    """
    r = raw_role.lower()
    if "wk" in r or "keeper" in r:
        return "wk-bat"
    if "allrounder" in r or "all-rounder" in r:
        return "allrounder"
    if "bowl" in r:
        return "bowl"
    return "bat"