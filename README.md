# 🏏 PitchIQ v2 — IPL Coaching Intelligence System

PitchIQ is a **real-time coaching dashboard** designed for IPL team coaches sitting in the dugout during a live match. It auto-detects the current match, pulls the Playing 15 for both teams, tracks every ball, and delivers instant intelligent suggestions — from who should bat next, to which bowler for this over, to when to use the Impact Substitution. The coach never types anything manually; everything is automatically derived from live match data.

---

## ⚡ Features

| Module | What it does |
|--------|-------------|
| **📊 War Room** | Live match overview: win probability, pressure index, run rate chart, batters at crease, last 6 balls, plain-English analysis |
| **🏏 Batting Order** | Ranked "who bats next" list with phase-weighted scoring, form/SR charts, and "SEND IN NOW" hero card |
| **🎯 Bowling Plan** | Over-by-over strategy for next 6 overs, quota tracker per bowler, economy charts, field placement hints |
| **🔥 Matchup Matrix** | Batter × Bowler heatmap showing danger zones, bowler advantages, and field suggestions |
| **🔀 Impact Sub** | Bench player scoring with timing recommendation (e.g., "Bring in at over 14") and impact chart |
| **📝 Session Notes** | Coach's private notepad with quick-insert, auto-generated summaries, and .txt export |

---

## 🔌 Live Data — Three-Tier Fallback

```
┌─────────────────────────────────────────────────┐
│                  DATA PIPELINE                   │
├─────────────────────────────────────────────────┤
│                                                  │
│   Tier 1: cricketdata.org API  (CRICDATA_KEY)    │
│       ├── /currentMatches                        │
│       ├── /match_info                            │
│       ├── /match_squad                           │
│       └── /match_scorecard                       │
│                     │                            │
│                     ▼ (if fails / no key)         │
│   Tier 2: Cricbuzz Scraper  (BeautifulSoup)      │
│       └── /cricket-match/live-scores             │
│                     │                            │
│                     ▼ (if fails / no internet)    │
│   Tier 3: Built-in Mock Data  (always works)     │
│       └── RCB vs CSK demo match                  │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 🚀 Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/your-username/pitch-iq.git
cd pitch-iq

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment
cp .env.example .env
# Edit .env and add your free API key from cricketdata.org

# 4. Run locally
streamlit run app.py
```

The app opens at `http://localhost:8501`. If no API key is set, it will automatically fall back to **demo mode** with a realistic RCB vs CSK match.

---

## 🔑 Environment Setup

Create a `.env` file (or copy from `.env.example`):

```env
CRICDATA_KEY=your_free_key_from_cricketdata_org
DEBUG=false
```

| Variable | Description |
|----------|-------------|
| `CRICDATA_KEY` | Free API key from [cricketdata.org](https://cricketdata.org) |
| `DEBUG` | Set to `true` to see API responses and fuzzy-match logs in terminal |

---

## 📁 Project Structure

```
pitch-iq/
├── app.py                         ← entry point
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── .streamlit/
│   └── config.toml                ← dark theme config
│
├── core/
│   ├── __init__.py
│   ├── live_data.py               ← three-tier data fetching
│   ├── squad_resolver.py          ← fuzzy name matching + squad detection
│   ├── engine.py                  ← all analytical/coaching logic
│   └── state.py                   ← central session state manager
│
├── data/
│   ├── __init__.py
│   ├── teams_db.py                ← IPL 2026 all 10 team profiles
│   ├── player_profiles.py         ← ~150 player stats (all 10 teams)
│   └── mock_data.py               ← offline demo match data
│
├── components/
│   ├── __init__.py
│   ├── sidebar.py                 ← match selector, nav, debug panel
│   ├── styles.py                  ← global CSS dark theme
│   └── cards.py                   ← reusable HTML card components
│
└── pages/
    ├── __init__.py
    ├── war_room.py                ← live match overview
    ├── batting_order.py           ← who bats next
    ├── bowling_plan.py            ← over-by-over bowling strategy
    ├── matchup_matrix.py          ← batter vs bowler heatmap
    ├── impact_sub.py              ← bench player recommendation
    └── session_notes.py           ← coach notepad with export
```

---

## ☁️ Deploy to Streamlit Community Cloud

1. **Push to GitHub** — Ensure `requirements.txt` is in the repo root.

2. **Connect on Streamlit Cloud** — Go to [share.streamlit.io](https://share.streamlit.io), click "New app", select your repo, branch, and set `app.py` as the main file.

3. **Add Secrets** — In the Streamlit Cloud dashboard, go to **App Settings → Secrets** and add:
   ```toml
   CRICDATA_KEY = "your_key_here"
   DEBUG = "false"
   ```

That's it — your app will be live at `https://your-app.streamlit.app`.

---

## 📊 Data Sources

- **[CricketData.org](https://cricketdata.org)** — Free tier: 100 requests/day. Provides live scores, squads, and scorecards.
- **Cricbuzz** — Public HTML scraping as a fallback (no API key needed).
- **Built-in Mock Data** — A complete RCB vs CSK match (over 14, chasing 182, score 98/3) for offline development and demos.

---

## 🧠 Analytics Engine

The coaching intelligence is powered by `core/engine.py`:

- **Win Probability** — DLS-inspired formula considering required rate, wickets, phase, and balls remaining
- **Pressure Index** — 0-100 composite score with "Controlled / Elevated / Critical" labels
- **Batting Order** — Phase-weighted scoring (PP → SR, Death → Death SR, chase → Chase SR)
- **Bowling Plan** — Optimal bowler selection per over with line/length and matchup analysis
- **Matchup Matrix** — Hand-vs-spin-type advantages, form differentials, strike rate analysis
- **Impact Sub** — Situation-aware bench scoring: chase acceleration, death bowling, batting depth

---

## 📜 License

MIT License. Built for cricket, by cricket fans. 🏏
