# PitchIQ — Cricket Coaching Intelligence System 🏏

> Real-time IPL coaching decision support. Who bats next. Which bowler for this over. Matchup dangers. Impact sub timing. Built for coaches sitting in the dugout.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## What it does

| Module | What it tells the coach |
|---|---|
| 🎯 War Room | Live win probability, run-rate chart, plain-English analysis |
| 🏏 Batting Order | Who to send in next — ranked by phase, form, chase context |
| 🎳 Bowling Plan | Over-by-over bowler assignments + field placements |
| ⚔️ Matchup Matrix | Batter × bowler threat heatmap — danger zones & advantages |
| 🔄 Impact Sub | Best impact player + optimal substitution timing |
| 📋 Session Notes | Real-time coaching notepad with export |

---

## Live data sources

PitchIQ tries data sources in this priority order:

1. **cricketdata.org API** (free tier, 100 req/day) — set `CRICDATA_KEY` in `.env`
2. **Cricbuzz scraper** — unofficial, no key needed, automatic fallback
3. **Demo/mock data** — used when offline or both sources fail

---

## Quickstart (local)

```bash
git clone https://github.com/YOUR_USERNAME/pitch-iq
cd pitch-iq
pip install -r requirements.txt
cp .env.example .env          # optional: add your cricketdata.org key
streamlit run app.py
```

---

## Deploy to Streamlit Community Cloud (free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → sign in
3. New app → select repo → main file: `app.py`
4. Add secret: `CRICDATA_KEY = "your_key"` (optional)
5. Deploy — get a public URL in ~2 minutes

---

## Project structure

```
pitch-iq/
├── app.py                    # Entry point
├── requirements.txt
├── .env.example
├── .streamlit/
│   └── config.toml           # Dark theme config
│
├── core/
│   ├── engine.py             # All analytics: win prob, batting order, bowling plan, matchups
│   └── live_data.py          # Data layer: API + scraper + mock fallback
│
├── data/
│   ├── teams_db.py           # IPL 2026 squads with full player profiles
│   └── mock_data.py          # Demo scorecard for offline use
│
├── components/
│   ├── sidebar.py            # Navigation + match selector
│   └── styles.py             # Global CSS theme
│
└── pages/
    ├── war_room.py           # Live overview
    ├── batting_order.py      # Who bats next
    ├── bowling_plan.py       # Over-by-over bowling
    ├── matchup_matrix.py     # Batter vs bowler heatmap
    ├── impact_sub.py         # Impact player advisor
    └── session_notes.py      # Coach's notepad
```

---

## Tech stack

- [Streamlit](https://streamlit.io) — UI
- [Plotly](https://plotly.com/python/) — Interactive charts
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — Cricbuzz scraper
- [cricketdata.org](https://cricketdata.org) — Official free API (optional)
- Zero paid services required

---

## Roadmap

- [ ] Historical head-to-head stats per matchup
- [ ] Player fatigue tracker (balls bowled, overs fielded)
- [ ] Wagon wheel visualization per batter
- [ ] Push notifications for key match events
- [ ] Multi-match session history

---

*Built during IPL 2026 season. Not affiliated with BCCI or any IPL franchise.*
