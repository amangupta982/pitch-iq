<p align="center">
  <img src="https://img.shields.io/badge/🏏-PitchIQ-blue?style=for-the-badge&labelColor=0e1117&color=3b82f6" alt="PitchIQ" height="40"/>
</p>

<h1 align="center">PitchIQ — IPL Coaching Intelligence</h1>

<p align="center">
  <em>Real-time AI-powered coaching dashboard for IPL cricket — built for the dugout.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/streamlit-1.32+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/plotly-5.20+-3F4F75?style=flat-square&logo=plotly&logoColor=white" alt="Plotly"/>
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License"/>
  <img src="https://img.shields.io/badge/IPL-2026-orange?style=flat-square" alt="IPL 2026"/>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quickstart">Quickstart</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-data-pipeline">Data Pipeline</a> •
  <a href="#-modules">Modules</a> •
  <a href="#-deployment">Deployment</a> •
  <a href="#-contributing">Contributing</a>
</p>

---

## 🎯 What is PitchIQ?

**PitchIQ** is a production-grade coaching intelligence system designed for IPL team coaches sitting in the dugout during a live T20 match. It auto-detects the current match, pulls live data, and delivers **instant intelligent coaching decisions** — zero manual input required.

> **The coach never types anything manually.**  
> Everything is derived from live match data — from who should bat next, to which bowler for this over, to when to trigger the Impact Substitution.

### Why PitchIQ?

| Problem | PitchIQ Solution |
|---------|-----------------|
| Coaches rely on gut feel during high-pressure moments | Data-driven recommendations updated every 30 seconds |
| Pen-and-paper matchup tracking is slow | Real-time batter × bowler heatmap with auto-highlighted danger zones |
| Impact Sub timing is a guessing game | Situation-aware scoring with optimal timing recommendation |
| No centralized view of match situation | Single War Room dashboard with win probability, pressure index, and analysis |

---

## ⚡ Features

### 📊 War Room — Live Match Command Center
> Win probability, pressure index (0–100), run rate tracker, batters at crease, current bowler, last 6 balls, and natural-language situation analysis — all in one screen.

### 🏏 Batting Order — Who Bats Next
> Phase-weighted player ranking considering strike rate, form, vs-pace/spin matchups, and chase context. Features a **SEND IN NOW** hero card for the top pick.

### 🎯 Bowling Plan — Over-by-Over Strategy
> Optimal bowler selection for the next 6 overs with quota tracking, economy charts, line-and-length suggestions, and field placement hints per bowler.

### 🔥 Matchup Matrix — Batter × Bowler Heatmap
> Interactive Plotly heatmap showing danger zones (batter dominates) and bowler advantages. Auto-highlights current batters and bowler.

### 🔀 Impact Sub — Bench Player Intelligence
> Scores all 4 bench players for current-situation relevance. Recommends **who** to bring in, **when**, and **why** — with timing down to the over.

### 📝 Session Notes — Coach's Private Notepad
> Timestamped quick-insert buttons, auto-generated situation summaries, and `.txt` export. Notes persist across page switches.

---

## 🚀 Quickstart

### Prerequisites

- **Python 3.10+**
- **pip** (package manager)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/amangupta982/pitch-iq.git
cd pitch-iq

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # macOS / Linux
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your API key (see below)

# 5. Launch the dashboard
streamlit run app.py
```

The app opens at **`http://localhost:8501`**. If no API key is set, it automatically falls back to **demo mode** with a realistic RCB vs CSK match.

### Environment Variables

Create a `.env` file (or copy from `.env.example`):

```env
CRICDATA_KEY=your_free_key_from_cricketdata_org
DEBUG=false
```

| Variable | Required | Description |
|----------|----------|-------------|
| `CRICDATA_KEY` | Optional | Free API key from [cricketdata.org](https://cricketdata.org) (100 req/day) |
| `DEBUG` | Optional | Set to `true` for verbose API/fuzzy-match logging in terminal |

> **Note:** PitchIQ works fully offline in demo mode — no API key needed for development.

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         STREAMLIT APP                           │
│  ┌──────────┐  ┌──────────────────────────────────────────────┐ │
│  │ Sidebar  │  │              Page Router                     │ │
│  │          │  │  ┌─────────┐ ┌─────────┐ ┌──────────┐       │ │
│  │ • Match  │  │  │War Room │ │Batting  │ │Bowling   │       │ │
│  │   Select │  │  │         │ │ Order   │ │ Plan     │       │ │
│  │ • Ticker │  │  └─────────┘ └─────────┘ └──────────┘       │ │
│  │ • Team   │  │  ┌─────────┐ ┌─────────┐ ┌──────────┐       │ │
│  │   Select │  │  │Matchup  │ │Impact   │ │Session   │       │ │
│  │ • Nav    │  │  │ Matrix  │ │ Sub     │ │ Notes    │       │ │
│  │ • Debug  │  │  └─────────┘ └─────────┘ └──────────┘       │ │
│  └──────────┘  └──────────────────────────────────────────────┘ │
│                              │                                  │
│                    ┌─────────▼──────────┐                       │
│                    │   core/state.py    │ ← Single point of     │
│                    │  (Session State)   │   data mutation        │
│                    └─────────┬──────────┘                       │
│              ┌───────────────┼───────────────┐                  │
│      ┌───────▼──────┐ ┌─────▼─────┐ ┌───────▼──────┐           │
│      │squad_resolver│ │ engine.py  │ │ live_data.py │           │
│      │  (Fuzzy NLP) │ │(Analytics) │ │ (3-Tier API) │           │
│      └──────────────┘ └───────────┘ └──────┬───────┘           │
│                                      ┌─────┼─────┐             │
│                                    API  Scraper  Mock           │
└─────────────────────────────────────────────────────────────────┘
```

### Key Design Principles

1. **Single Source of Truth** — All pages read from `st.session_state`. Only `state.py` mutates state.
2. **Three-Tier Data Fallback** — API → Scraper → Mock. App always works, even offline.
3. **Fuzzy Name Resolution** — `rapidfuzz` matches player names from APIs to canonical profiles (75-point threshold).
4. **Team ID Resolution** — Exhaustive alias map + fuzzy fallback matches any team name variant to internal IDs.

---

## 🔌 Data Pipeline

```
┌───────────────────────────────────────────────────┐
│                  DATA PIPELINE                     │
├───────────────────────────────────────────────────┤
│                                                    │
│   Tier 1: cricketdata.org API  (CRICDATA_KEY)      │
│       ├── /currentMatches                          │
│       ├── /match_info                              │
│       ├── /match_squad                             │
│       └── /match_scorecard                         │
│                     │                              │
│                     ▼ (if fails / no key)           │
│   Tier 2: Cricbuzz Scraper  (BeautifulSoup)        │
│       └── /cricket-match/live-scores               │
│                     │                              │
│                     ▼ (if fails / no internet)      │
│   Tier 3: Built-in Mock Data  (always works)       │
│       └── RCB vs CSK demo match                    │
│                                                    │
└───────────────────────────────────────────────────┘
```

| Source | Latency | Rate Limit | Auth Required |
|--------|---------|------------|---------------|
| CricketData API | ~200ms | 100/day (free) | API key |
| Cricbuzz Scraper | ~1-2s | None | No |
| Built-in Mock | Instant | None | No |

---

## 📦 Modules

### Project Structure

```
pitch-iq/
├── app.py                         ← Entry point + page router
├── requirements.txt               ← Python dependencies
├── .env.example                   ← Environment template
├── .gitignore
├── README.md
│
├── .streamlit/
│   └── config.toml                ← Dark theme configuration
│
├── core/
│   ├── __init__.py
│   ├── live_data.py               ← Three-tier data fetching
│   ├── squad_resolver.py          ← Fuzzy name matching + team ID resolution
│   ├── engine.py                  ← All analytical/coaching logic
│   └── state.py                   ← Central session state manager
│
├── data/
│   ├── __init__.py
│   ├── teams_db.py                ← IPL 2026 all 10 team profiles
│   ├── player_profiles.py         ← ~150 player stats (all 10 teams)
│   └── mock_data.py               ← Offline demo match data
│
├── components/
│   ├── __init__.py
│   ├── sidebar.py                 ← Match select, team select, nav, refresh
│   ├── styles.py                  ← Global CSS dark theme
│   └── cards.py                   ← Reusable HTML card components
│
└── pages/
    ├── __init__.py
    ├── war_room.py                ← Live match overview
    ├── batting_order.py           ← Who bats next
    ├── bowling_plan.py            ← Over-by-over bowling strategy
    ├── matchup_matrix.py          ← Batter vs bowler heatmap
    ├── impact_sub.py              ← Bench player recommendation
    └── session_notes.py           ← Coach notepad with export
```

### Analytics Engine (`core/engine.py`)

| Algorithm | Description |
|-----------|-------------|
| **Win Probability** | DLS-inspired formula: required rate, wickets, phase, balls remaining |
| **Pressure Index** | 0–100 composite score with Controlled / Elevated / Critical labels |
| **Batting Order** | Phase-weighted scoring (PP → SR, Death → Death SR, Chase → Chase SR) |
| **Bowling Plan** | Optimal bowler per over with economy, form, matchup, and quota factors |
| **Matchup Matrix** | Hand-vs-spin-type advantages, form differentials, strike rate analysis |
| **Impact Sub** | Situation-aware bench scoring: chase acceleration, death bowling, depth |

### Team Resolution (`core/squad_resolver.py`)

Handles all team name variations from different data sources:

```
"Rajasthan Royals"             → rr
"RR"                           → rr
"Kolkata Knight Riders"        → kkr
"Royal Challengers Bengaluru"  → rcb
"Royal Challengers Bangalore"  → rcb
"Kings XI Punjab"              → pbks
"Delhi Daredevils"             → dc
...and 50+ more aliases
```

---

## 🧰 Tech Stack

| Technology | Purpose |
|-----------|---------|
| [Streamlit](https://streamlit.io) | Dashboard framework |
| [Plotly](https://plotly.com/python/) | Interactive charts |
| [rapidfuzz](https://github.com/maxbachmann/RapidFuzz) | Fuzzy name matching |
| [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) | HTML scraping fallback |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Environment management |
| [CricketData API](https://cricketdata.org) | Live match data |

---

## ☁️ Deployment

### Streamlit Community Cloud (Recommended)

1. **Push to GitHub** — Ensure `requirements.txt` is in the repo root.

2. **Connect on Streamlit Cloud** — Go to [share.streamlit.io](https://share.streamlit.io), click "New app", select your repo, branch, and set `app.py` as the main file.

3. **Add Secrets** — In the Streamlit Cloud dashboard, go to **App Settings → Secrets** and add:
   ```toml
   CRICDATA_KEY = "your_key_here"
   DEBUG = "false"
   ```

That's it — your app will be live at `https://your-app.streamlit.app`.

### Docker (Alternative)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"]
```

```bash
docker build -t pitchiq .
docker run -p 8501:8501 --env-file .env pitchiq
```

---

## 📊 Data Sources

| Source | Type | Rate Limit | Used For |
|--------|------|-----------|----------|
| [CricketData.org](https://cricketdata.org) | REST API | 100 req/day (free) | Live scores, squads, scorecards |
| [Cricbuzz](https://cricbuzz.com) | HTML scraping | Unlimited | Fallback live scores |
| Built-in Mock | Local JSON | Unlimited | Offline dev & demos |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Tips

- Set `DEBUG=true` in `.env` to see API responses and fuzzy-match logs
- The mock data provides a complete RCB vs CSK match for offline development
- All card components return HTML strings — always use `unsafe_allow_html=True`
- Team names from APIs must go through `resolve_team_id()` before lookup

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ for cricket, by cricket fans. 🏏<br/>
  <sub>PitchIQ v2 — IPL 2026</sub>
</p>
