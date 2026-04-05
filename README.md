# 🏏 IPL AI War Room

A live IPL match analysis dashboard — win probability, strategy advisor, player insights. No external APIs, pure logic + data.

## Features
- Win probability engine (based on required rate, wickets, phase, venue, dew factor)
- Real-time run rate chart vs par score & required pace
- AI strategy advisor with situation-specific advice
- Plain-English match analysis
- Side-by-side player stats for both teams (batting + bowling)
- 8 IPL teams · 8 venues · 4 match scenarios

## Deploy on Streamlit Community Cloud (Free)

1. Fork / push this repo to your GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app**
4. Select your repo → set **Main file path** to `ipl_war_room.py`
5. Click **Deploy** — done in ~2 minutes!

## Run locally

```bash
pip install -r requirements.txt
streamlit run ipl_war_room.py
```

## File structure

```
ipl-war-room/
├── ipl_war_room.py        # Main app
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml        # Theme & server config
└── README.md
```

## Tech stack
- [Streamlit](https://streamlit.io) — UI framework
- [Plotly](https://plotly.com/python/) — Interactive charts
- [Pandas](https://pandas.pydata.org/) — Data tables
- Zero external APIs — all logic is self-contained
