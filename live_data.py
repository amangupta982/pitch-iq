"""
core/live_data.py
-----------------
Live cricket data layer.

Priority:
  1. cricketdata.org API  (free tier: 100 req/day — set CRICDATA_KEY in .env)
  2. Cricbuzz scraper     (unofficial, no key needed, fallback)
  3. Demo/mock data       (if both fail or in offline mode)

Usage:
  from core.live_data import get_live_match, get_scorecard
"""

import os
import time
import requests
import streamlit as st
from bs4 import BeautifulSoup
from data.mock_data import MOCK_SCORECARD

# ── Config ─────────────────────────────────────────────────────────────────────
CRICDATA_KEY   = os.getenv("CRICDATA_KEY", "")
CRICDATA_BASE  = "https://api.cricapi.com/v1"
SCRAPER_BASE   = "https://m.cricbuzz.com"
CACHE_TTL      = 30   # seconds between live refreshes

# ── Helpers ────────────────────────────────────────────────────────────────────
def _headers():
    return {"User-Agent": "Mozilla/5.0 (compatible; PitchIQ/1.0)"}

@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def get_live_matches():
    """Return list of live/recent matches. Tries API first, then scraper."""
    if CRICDATA_KEY:
        try:
            r = requests.get(
                f"{CRICDATA_BASE}/currentMatches",
                params={"apikey": CRICDATA_KEY, "offset": 0},
                timeout=5,
            )
            data = r.json()
            if data.get("status") == "success":
                return _parse_cricdata_list(data["data"])
        except Exception:
            pass

    # Fallback: scrape Cricbuzz
    try:
        return _scrape_live_matches()
    except Exception:
        return _mock_match_list()

@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def get_scorecard(match_id: str, source: str = "auto"):
    """Return full scorecard dict for a match_id."""
    if source == "api" or (source == "auto" and CRICDATA_KEY):
        try:
            r = requests.get(
                f"{CRICDATA_BASE}/match_scorecard",
                params={"apikey": CRICDATA_KEY, "id": match_id},
                timeout=5,
            )
            data = r.json()
            if data.get("status") == "success":
                return _parse_cricdata_scorecard(data["data"])
        except Exception:
            pass

    if source == "scraper" or source == "auto":
        try:
            return _scrape_scorecard(match_id)
        except Exception:
            pass

    return MOCK_SCORECARD

# ── cricketdata.org parsers ────────────────────────────────────────────────────
def _parse_cricdata_list(matches: list) -> list:
    out = []
    for m in matches:
        if "IPL" not in m.get("series", "") and "Indian Premier" not in m.get("series", ""):
            continue
        out.append({
            "id":     m.get("id", ""),
            "label":  m.get("name", "Unknown match"),
            "status": m.get("status", ""),
            "source": "api",
        })
    return out or _mock_match_list()

def _parse_cricdata_scorecard(data: dict) -> dict:
    """Normalise API scorecard into PitchIQ internal format."""
    innings_list = data.get("scorecard", [])
    parsed = []
    for inn in innings_list:
        batters = []
        for b in inn.get("batting", []):
            batters.append({
                "name":        b.get("batsmanName", ""),
                "runs":        int(b.get("r", 0)),
                "balls":       int(b.get("b", 0)),
                "fours":       int(b.get("4s", 0)),
                "sixes":       int(b.get("6s", 0)),
                "sr":          float(b.get("sr", 0)),
                "dismissal":   b.get("dismissal", "batting"),
                "out":         b.get("dismissal", "") not in ("", "batting", "not out"),
            })
        bowlers = []
        for bw in inn.get("bowling", []):
            bowlers.append({
                "name":    bw.get("bowlerName", ""),
                "overs":   float(bw.get("o", 0)),
                "maidens": int(bw.get("m", 0)),
                "runs":    int(bw.get("r", 0)),
                "wickets": int(bw.get("w", 0)),
                "economy": float(bw.get("eco", 0)),
                "wides":   int(bw.get("wd", 0)),
                "noballs": int(bw.get("nb", 0)),
            })
        parsed.append({
            "team":    inn.get("batTeamName", ""),
            "total":   inn.get("score", "0/0"),
            "overs":   inn.get("overs", "0.0"),
            "batters": batters,
            "bowlers": bowlers,
        })

    return {
        "match_id":  data.get("id", ""),
        "title":     data.get("name", ""),
        "status":    data.get("status", ""),
        "toss":      data.get("tossWinner", "") + " won the toss",
        "venue":     data.get("venue", ""),
        "innings":   parsed,
        "source":    "api",
    }

# ── Cricbuzz scraper ───────────────────────────────────────────────────────────
def _scrape_live_matches() -> list:
    """Scrape live match list from Cricbuzz mobile site."""
    url = f"{SCRAPER_BASE}/cricket-match/live-scores"
    r   = requests.get(url, headers=_headers(), timeout=8)
    soup = BeautifulSoup(r.text, "html.parser")
    matches = []
    for card in soup.select("div.cb-mtch-lst"):
        link = card.select_one("a")
        title = card.get_text(strip=True)
        if not link:
            continue
        href = link.get("href", "")
        match_id = href.split("/")[2] if len(href.split("/")) > 2 else ""
        if "IPL" in title or "Indian Premier" in title:
            matches.append({
                "id":     match_id,
                "label":  title[:60],
                "status": "live",
                "source": "scraper",
            })
    return matches or _mock_match_list()

def _scrape_scorecard(match_id: str) -> dict:
    """Scrape full scorecard from Cricbuzz for a given match_id."""
    url  = f"{SCRAPER_BASE}/cricket-scores/{match_id}"
    r    = requests.get(url, headers=_headers(), timeout=8)
    soup = BeautifulSoup(r.text, "html.parser")

    title  = soup.select_one("h1.cb-nav-hdr")
    title  = title.get_text(strip=True) if title else "Live Match"
    status = soup.select_one("div.cb-text-complete")
    status = status.get_text(strip=True) if status else "In Progress"

    innings = []
    for inn_div in soup.select("div.cb-ltst-wgt-hdr"):
        inn_title = inn_div.get_text(strip=True)
        batters, bowlers = [], []

        bat_table = inn_div.find_next("table", class_="cb-bat-lst")
        if bat_table:
            for row in bat_table.select("tr")[1:]:
                cols = [c.get_text(strip=True) for c in row.select("td")]
                if len(cols) >= 8:
                    batters.append({
                        "name":      cols[0],
                        "dismissal": cols[1],
                        "runs":      _int(cols[2]),
                        "balls":     _int(cols[3]),
                        "fours":     _int(cols[5]),
                        "sixes":     _int(cols[6]),
                        "sr":        _float(cols[7]),
                        "out":       cols[1] not in ("batting", "not out", ""),
                    })

        bwl_table = inn_div.find_next("table", class_="cb-bowl-lst")
        if bwl_table:
            for row in bwl_table.select("tr")[1:]:
                cols = [c.get_text(strip=True) for c in row.select("td")]
                if len(cols) >= 7:
                    bowlers.append({
                        "name":    cols[0],
                        "overs":   _float(cols[1]),
                        "maidens": _int(cols[2]),
                        "runs":    _int(cols[3]),
                        "wickets": _int(cols[4]),
                        "economy": _float(cols[5]),
                        "wides":   _int(cols[6]) if len(cols) > 6 else 0,
                        "noballs": _int(cols[7]) if len(cols) > 7 else 0,
                    })

        score_tag = inn_div.find_next("div", class_="cb-scr-wll-chvrn")
        score_txt = score_tag.get_text(strip=True) if score_tag else "0/0 (0)"

        innings.append({
            "team":    inn_title,
            "total":   score_txt,
            "overs":   _extract_overs(score_txt),
            "batters": batters,
            "bowlers": bowlers,
        })

    return {
        "match_id": match_id,
        "title":    title,
        "status":   status,
        "toss":     "",
        "venue":    "",
        "innings":  innings or MOCK_SCORECARD["innings"],
        "source":   "scraper",
    }

# ── Utilities ──────────────────────────────────────────────────────────────────
def _int(v):
    try:    return int(str(v).replace("*", ""))
    except: return 0

def _float(v):
    try:    return float(str(v).replace("*", ""))
    except: return 0.0

def _extract_overs(score_txt: str) -> str:
    import re
    m = re.search(r"\(([0-9.]+)\)", score_txt)
    return m.group(1) if m else "0.0"

def _mock_match_list():
    return [
        {"id": "demo_rcb_csk", "label": "RCB vs CSK — Demo",  "status": "In Progress", "source": "mock"},
        {"id": "demo_mi_kkr",  "label": "MI vs KKR — Demo",   "status": "Upcoming",    "source": "mock"},
        {"id": "demo_srh_lsg", "label": "SRH vs LSG — Demo",  "status": "Upcoming",    "source": "mock"},
    ]
