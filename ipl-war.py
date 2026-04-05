import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import math

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL AI War Room",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.main { background-color: #0e1117; }

/* Metric cards */
[data-testid="metric-container"] {
    background: #1a1f2e;
    border: 1px solid #2d3548;
    border-radius: 12px;
    padding: 16px 20px;
}
[data-testid="metric-container"] label {
    color: #8b95a8 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #f0f4ff !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 12px !important;
}

/* Section headers */
.section-header {
    font-size: 11px;
    font-weight: 600;
    color: #5a6478;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 24px 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e2535;
}

/* Win probability bar */
.win-bar-container {
    background: #1a1f2e;
    border: 1px solid #2d3548;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.win-bar-title {
    font-size: 11px;
    font-weight: 600;
    color: #5a6478;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 14px;
}
.team-labels {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-weight: 600;
    font-size: 15px;
}
.win-bar-outer {
    height: 24px;
    border-radius: 12px;
    background: #2d3548;
    overflow: hidden;
    display: flex;
}
.win-bar-a {
    height: 100%;
    border-radius: 12px 0 0 12px;
    transition: width 0.5s ease;
}
.win-bar-b {
    height: 100%;
    border-radius: 0 12px 12px 0;
}
.pct-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 8px;
    font-size: 13px;
    color: #8b95a8;
    font-weight: 500;
}

/* Strategy cards */
.strategy-card {
    background: #1a1f2e;
    border: 1px solid #2d3548;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.strategy-tag {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 6px;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.tag-ok    { background: #0d2b1a; color: #4caf7d; border: 1px solid #1a4a2e; }
.tag-warn  { background: #2b1f0a; color: #e8a94a; border: 1px solid #4a3510; }
.tag-danger{ background: #2b0d0d; color: #e85555; border: 1px solid #4a1515; }
.strategy-text { font-size: 13px; color: #c8d0e0; line-height: 1.65; }

/* Analysis box */
.analysis-card {
    background: #0d1e35;
    border-left: 3px solid #3b82f6;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    margin-bottom: 10px;
}
.analysis-text { font-size: 13px; color: #93c5fd; line-height: 1.65; }

/* Live badge */
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #2b0d0d;
    color: #e85555;
    font-size: 11px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 20px;
    border: 1px solid #4a1515;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.live-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #e85555;
}

/* Player row */
.player-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #1e2535;
}
.player-row:last-child { border-bottom: none; }
.player-name { font-size: 13px; font-weight: 500; color: #e8eaf0; }
.player-stat { font-size: 12px; color: #8b95a8; }
.player-bar-wrap { width: 80px; height: 5px; background: #2d3548; border-radius: 3px; overflow: hidden; display:inline-block; vertical-align:middle; margin-right:10px; }
.player-bar-fill { height: 100%; border-radius: 3px; background: #3b82f6; }

/* Situation card */
.sit-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.sit-card {
    background: #1a1f2e;
    border: 1px solid #2d3548;
    border-radius: 10px;
    padding: 12px 14px;
}
.sit-label { font-size: 11px; color: #5a6478; margin-bottom: 4px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em; }
.sit-value { font-size: 14px; font-weight: 600; color: #e8eaf0; }

/* Sidebar */
[data-testid="stSidebar"] { background: #111827; border-right: 1px solid #1e2535; }
[data-testid="stSidebar"] label { color: #8b95a8 !important; font-size: 12px !important; font-weight: 500 !important; }

/* Selectbox / number input */
.stSelectbox > div > div, .stNumberInput > div > div > input {
    background: #1a1f2e !important;
    border: 1px solid #2d3548 !important;
    color: #e8eaf0 !important;
    border-radius: 8px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: #1a1f2e; border-radius: 8px; padding: 3px; gap: 2px; }
.stTabs [data-baseweb="tab"] { background: transparent; color: #8b95a8; border-radius: 6px; font-size: 13px; font-weight: 500; }
.stTabs [aria-selected="true"] { background: #2d3548 !important; color: #f0f4ff !important; }

h1,h2,h3 { color: #f0f4ff !important; }
p { color: #c8d0e0; }
</style>
""", unsafe_allow_html=True)


# ── Data ───────────────────────────────────────────────────────────────────────
TEAMS = {
    "rcb": {
        "name": "Royal Challengers Bengaluru", "short": "RCB", "color": "#E25822",
        "batters": [
            {"name": "Virat Kohli",     "avg": 52, "sr": 138, "form": 92},
            {"name": "Faf du Plessis",  "avg": 38, "sr": 145, "form": 74},
            {"name": "Glenn Maxwell",   "avg": 29, "sr": 175, "form": 65},
            {"name": "Rajat Patidar",   "avg": 34, "sr": 148, "form": 70},
        ],
        "bowlers": [
            {"name": "Mohammed Siraj",    "econ": 7.8, "wkts": 18, "form": 80},
            {"name": "Yuzvendra Chahal", "econ": 8.2, "wkts": 15, "form": 72},
            {"name": "Alzarri Joseph",   "econ": 8.9, "wkts": 12, "form": 65},
        ],
        "home": "Chinnaswamy", "avg_score": 178, "chase_win": 0.54,
    },
    "csk": {
        "name": "Chennai Super Kings", "short": "CSK", "color": "#F5A623",
        "batters": [
            {"name": "Ruturaj Gaikwad", "avg": 45, "sr": 135, "form": 85},
            {"name": "Devon Conway",    "avg": 40, "sr": 128, "form": 78},
            {"name": "MS Dhoni",        "avg": 25, "sr": 162, "form": 60},
            {"name": "Shivam Dube",     "avg": 32, "sr": 158, "form": 73},
        ],
        "bowlers": [
            {"name": "Deepak Chahar",       "econ": 7.5, "wkts": 14, "form": 76},
            {"name": "Ravindra Jadeja",     "econ": 7.1, "wkts": 11, "form": 82},
            {"name": "Matheesha Pathirana", "econ": 8.4, "wkts": 16, "form": 70},
        ],
        "home": "Chepauk", "avg_score": 172, "chase_win": 0.58,
    },
    "mi": {
        "name": "Mumbai Indians", "short": "MI", "color": "#1B6BB0",
        "batters": [
            {"name": "Rohit Sharma",        "avg": 42, "sr": 142, "form": 80},
            {"name": "Ishan Kishan",        "avg": 35, "sr": 155, "form": 68},
            {"name": "Suryakumar Yadav",    "avg": 38, "sr": 178, "form": 88},
            {"name": "Tim David",           "avg": 28, "sr": 168, "form": 72},
        ],
        "bowlers": [
            {"name": "Jasprit Bumrah",  "econ": 6.9, "wkts": 22, "form": 95},
            {"name": "Piyush Chawla",   "econ": 8.0, "wkts": 10, "form": 62},
            {"name": "Gerald Coetzee",  "econ": 9.1, "wkts": 13, "form": 66},
        ],
        "home": "Wankhede", "avg_score": 181, "chase_win": 0.52,
    },
    "kkr": {
        "name": "Kolkata Knight Riders", "short": "KKR", "color": "#6F4BA8",
        "batters": [
            {"name": "Phil Salt",    "avg": 36, "sr": 160, "form": 76},
            {"name": "Sunil Narine", "avg": 27, "sr": 170, "form": 72},
            {"name": "Shreyas Iyer", "avg": 43, "sr": 132, "form": 82},
            {"name": "Rinku Singh",  "avg": 30, "sr": 152, "form": 78},
        ],
        "bowlers": [
            {"name": "Varun Chakravarthy", "econ": 7.4, "wkts": 17, "form": 80},
            {"name": "Harshit Rana",       "econ": 8.6, "wkts": 12, "form": 65},
            {"name": "Mitchell Starc",     "econ": 8.8, "wkts": 14, "form": 70},
        ],
        "home": "Eden Gardens", "avg_score": 176, "chase_win": 0.55,
    },
    "dc": {
        "name": "Delhi Capitals", "short": "DC", "color": "#0B3D91",
        "batters": [
            {"name": "Jake Fraser-McGurk", "avg": 32, "sr": 172, "form": 80},
            {"name": "David Warner",       "avg": 41, "sr": 148, "form": 75},
            {"name": "Axar Patel",         "avg": 26, "sr": 145, "form": 68},
            {"name": "Tristan Stubbs",     "avg": 28, "sr": 155, "form": 66},
        ],
        "bowlers": [
            {"name": "Kuldeep Yadav",  "econ": 7.6, "wkts": 19, "form": 85},
            {"name": "Anrich Nortje",  "econ": 7.9, "wkts": 15, "form": 78},
            {"name": "Ishant Sharma",  "econ": 8.5, "wkts": 9,  "form": 55},
        ],
        "home": "Arun Jaitley", "avg_score": 174, "chase_win": 0.53,
    },
    "rr": {
        "name": "Rajasthan Royals", "short": "RR", "color": "#C0437A",
        "batters": [
            {"name": "Jos Buttler",       "avg": 48, "sr": 152, "form": 86},
            {"name": "Yashasvi Jaiswal",  "avg": 44, "sr": 162, "form": 90},
            {"name": "Sanju Samson",      "avg": 36, "sr": 145, "form": 74},
            {"name": "Shimron Hetmyer",   "avg": 27, "sr": 165, "form": 70},
        ],
        "bowlers": [
            {"name": "Trent Boult",           "econ": 7.2, "wkts": 18, "form": 82},
            {"name": "Yuzvendra Chahal",      "econ": 8.0, "wkts": 16, "form": 75},
            {"name": "Ravichandran Ashwin",   "econ": 7.8, "wkts": 12, "form": 72},
        ],
        "home": "Sawai Mansingh", "avg_score": 177, "chase_win": 0.56,
    },
    "srh": {
        "name": "Sunrisers Hyderabad", "short": "SRH", "color": "#F26522",
        "batters": [
            {"name": "Travis Head",      "avg": 38, "sr": 175, "form": 84},
            {"name": "Abhishek Sharma",  "avg": 30, "sr": 180, "form": 78},
            {"name": "Heinrich Klaasen", "avg": 42, "sr": 162, "form": 88},
            {"name": "Aiden Markram",    "avg": 35, "sr": 145, "form": 72},
        ],
        "bowlers": [
            {"name": "Pat Cummins",         "econ": 8.1, "wkts": 16, "form": 80},
            {"name": "Bhuvneshwar Kumar",   "econ": 7.6, "wkts": 13, "form": 72},
            {"name": "Mayank Markande",     "econ": 8.4, "wkts": 10, "form": 62},
        ],
        "home": "Rajiv Gandhi", "avg_score": 186, "chase_win": 0.50,
    },
    "lsg": {
        "name": "Lucknow Super Giants", "short": "LSG", "color": "#00A868",
        "batters": [
            {"name": "KL Rahul",        "avg": 46, "sr": 136, "form": 82},
            {"name": "Quinton de Kock", "avg": 38, "sr": 148, "form": 76},
            {"name": "Marcus Stoinis",  "avg": 30, "sr": 155, "form": 70},
            {"name": "Nicholas Pooran", "avg": 34, "sr": 162, "form": 74},
        ],
        "bowlers": [
            {"name": "Ravi Bishnoi", "econ": 7.5, "wkts": 16, "form": 80},
            {"name": "Avesh Khan",   "econ": 8.7, "wkts": 12, "form": 65},
            {"name": "Mark Wood",    "econ": 8.9, "wkts": 14, "form": 68},
        ],
        "home": "BRSABV Ekana", "avg_score": 173, "chase_win": 0.54,
    },
}

VENUES = {
    "Wankhede, Mumbai":           {"avg": 185, "dew": True,  "pace": True},
    "Chinnaswamy, Bengaluru":     {"avg": 192, "dew": True,  "pace": False},
    "Chepauk, Chennai":           {"avg": 162, "dew": False, "pace": False},
    "Eden Gardens, Kolkata":      {"avg": 178, "dew": True,  "pace": True},
    "Arun Jaitley, Delhi":        {"avg": 175, "dew": False, "pace": True},
    "Sawai Mansingh, Jaipur":     {"avg": 170, "dew": False, "pace": False},
    "Rajiv Gandhi, Hyderabad":    {"avg": 183, "dew": True,  "pace": True},
    "BRSABV Ekana, Lucknow":      {"avg": 171, "dew": True,  "pace": False},
}

MATCHES = [
    {"label": "RCB vs CSK  🔥 Tonight", "a": "rcb", "b": "csk"},
    {"label": "MI vs KKR",               "a": "mi",  "b": "kkr"},
    {"label": "SRH vs LSG",              "a": "srh", "b": "lsg"},
    {"label": "DC vs RR",                "a": "dc",  "b": "rr"},
]


# ── Logic ──────────────────────────────────────────────────────────────────────
def get_phase(overs):
    if overs <= 6:  return "Powerplay"
    if overs <= 15: return "Middle overs"
    return "Death overs"

def calc_win_prob(team_id, runs, wickets, overs, target, venue_name):
    team  = TEAMS[team_id]
    venue = VENUES[venue_name]
    balls_left = round((20 - overs) * 6)
    is_chasing = target > 0
    prob = 0.5

    if is_chasing:
        needed = target - runs
        if needed <= 0:        return 0.97
        if wickets >= 10:      return 0.03
        req_rate = (needed / balls_left * 6) if balls_left > 0 else 99
        prob  = team["chase_win"]
        prob -= (req_rate - 8.0) * 0.04
        prob -= wickets * 0.03
        prob += (venue["avg"] - 170) / 200
        prob += 0.02 if 6 < overs <= 15 else (-0.05 if overs > 15 else 0)
    else:
        crr  = runs / overs if overs > 0 else 0
        proj = runs + crr * (20 - overs)
        prob  = 0.5 + (proj - venue["avg"]) / 300
        prob -= wickets * 0.04
        if venue["dew"]: prob += 0.04

    return round(min(0.94, max(0.06, prob)), 4)

def build_rr_chart(runs, overs, target, venue_name):
    venue    = VENUES[venue_name]
    par_rr   = venue["avg"] / 20
    labels   = list(range(1, 21))
    actual   = []
    required = []
    par      = [round(par_rr * o, 1) for o in labels]

    floor_ov = int(overs)
    for o in labels:
        if o <= floor_ov and floor_ov > 0:
            actual.append(round(runs * o / floor_ov))
        else:
            actual.append(None)

        is_chasing = target > 0
        if is_chasing and o >= floor_ov:
            rem = target - runs
            ov_left = 20 - floor_ov
            req = runs + (rem * (o - floor_ov) / ov_left) if ov_left > 0 else target
            required.append(round(req))
        else:
            required.append(None)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=labels, y=actual, mode="lines+markers",
        name="Actual runs", line=dict(color="#3b82f6", width=2.5),
        marker=dict(size=4), connectgaps=False,
    ))
    if target > 0:
        fig.add_trace(go.Scatter(
            x=labels, y=required, mode="lines",
            name="Required pace", line=dict(color="#ef4444", width=2, dash="dash"),
            connectgaps=False,
        ))
    fig.add_trace(go.Scatter(
        x=labels, y=par, mode="lines",
        name="Venue par", line=dict(color="#6b7280", width=1, dash="dot"),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#111827",
        font=dict(color="#9ca3af", family="Inter"),
        margin=dict(l=10, r=10, t=10, b=10),
        height=240,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(size=11), bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            title="Over", tickfont=dict(size=10),
            gridcolor="#1e2535", tickvals=list(range(1,21,2)),
        ),
        yaxis=dict(
            title="Runs", tickfont=dict(size=10), gridcolor="#1e2535",
        ),
        hovermode="x unified",
    )
    return fig

def build_player_chart(players, mode):
    names  = [p["name"] for p in players]
    values = [p["form"] for p in players]
    colors = ["#3b82f6" if v >= 80 else "#f59e0b" if v >= 65 else "#6b7280" for v in values]

    if mode == "bat":
        hover = [f"Avg: {p['avg']}  •  SR: {p['sr']}  •  Form: {p['form']}/100" for p in players]
    else:
        hover = [f"Econ: {p['econ']}  •  Wkts: {p['wkts']}  •  Form: {p['form']}/100" for p in players]

    fig = go.Figure(go.Bar(
        x=values, y=names, orientation="h",
        marker_color=colors, hovertext=hover, hoverinfo="text",
        text=values, textposition="outside", textfont=dict(color="#9ca3af", size=11),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#111827",
        font=dict(color="#9ca3af", family="Inter"),
        margin=dict(l=10, r=60, t=10, b=10),
        height=180,
        xaxis=dict(range=[0, 110], showgrid=False, showticklabels=False),
        yaxis=dict(tickfont=dict(size=12, color="#c8d0e0"), gridcolor="#1e2535"),
        showlegend=False,
    )
    return fig

def get_strategies(runs, wickets, overs, target, venue_name, phase):
    venue       = VENUES[venue_name]
    is_chasing  = target > 0
    balls_left  = round((20 - overs) * 6)
    needed      = target - runs if is_chasing else 0
    req_rate    = round(needed / balls_left * 6, 1) if (is_chasing and balls_left > 0) else 0
    strategies  = []

    if is_chasing:
        if req_rate < 7.5:
            strategies.append(("Steady", "ok",
                f"Required rate of {req_rate} is very manageable. Play for partnership, rotate strike, "
                f"and explode in overs 16–20. Avoid unnecessary risks in the {phase}."))
        elif req_rate < 9.5:
            strategies.append(("Attack now", "warn",
                f"Required rate is climbing to {req_rate}. At least one batter must attack — "
                f"look for boundaries on powerplay overs and punish the shorter boundary side at {venue_name}."))
        else:
            strategies.append(("Desperate chase", "danger",
                f"Required rate of {req_rate} demands immediate big hitting. Target the spinner(s), "
                f"use depth in the lineup, and accept the risk of a wicket. Calculated aggression needed."))
        if wickets >= 7:
            strategies.append(("Tail protection", "danger",
                f"Only {10-wickets} wickets left — protect your lower order. "
                f"Strike rotation is critical; avoid big shots on good-length deliveries outside off-stump."))
        if venue["dew"]:
            strategies.append(("Dew advantage", "ok",
                f"Dew is likely at {venue_name} in the 2nd innings. The ball grips less — "
                f"this favors batting. Spinners will struggle to hold their line."))
    else:
        if phase == "Powerplay":
            strategies.append(("Powerplay push", "ok",
                f"Only {wickets} wickets down in the powerplay. Target boundaries through the off-side; "
                f"fielding restrictions mean gaps are wider. Aim for 50+ in 6 overs."))
        elif phase == "Middle overs":
            strategies.append(("Build platform", "warn",
                f"Middle overs — key to building a competitive total at {venue_name} "
                f"(avg: {venue['avg']}). Push for 8+ RPO here with {10-wickets} wickets in hand."))
        else:
            strategies.append(("Death blitz", "ok",
                f"Death overs! Maximize width and length — look for slog-sweeps, ramps, and paddle shots. "
                f"Target the fine leg and third man boundaries at {venue_name}."))
        if wickets >= 5:
            strategies.append(("Preserve wickets", "warn",
                f"{wickets} down — conserve lower-order batting. Avoid run-outs and playing against the turn. "
                f"You need at least 3 overs of explosive batting from your finishers."))

    return strategies

def get_analysis(team_id, opp_id, runs, wickets, overs, target, venue_name, prob, phase):
    team    = TEAMS[team_id]
    venue   = VENUES[venue_name]
    crr     = round(runs / overs, 2) if overs > 0 else 0
    balls_left = round((20 - overs) * 6)
    is_chasing = target > 0
    needed     = target - runs if is_chasing else 0
    req_rate   = round(needed / balls_left * 6, 1) if (is_chasing and balls_left > 0) else 0
    proj       = round(runs + crr * (20 - overs))
    win_str    = (
        "in a strong position" if prob > 0.65
        else "slightly ahead" if prob > 0.50
        else "under pressure" if prob > 0.35
        else "in serious trouble"
    )
    lines = [
        f"{team['name']} are {win_str} with a {round(prob*100)}% chance of winning.",
    ]
    if is_chasing:
        lines.append(f"They need {needed} runs off {balls_left} balls — a required rate of {req_rate}.")
        if req_rate > 10:
            lines.append("This is a steep ask, but T20 history shows chases of this nature are won by targeting spinners and short deliveries.")
    else:
        comparison = "above" if proj > venue["avg"] else "below"
        lines.append(f"At current run rate, {team['short']} are projecting {proj} — {comparison} the venue average of {venue['avg']}.")

    lines.append(f"The {phase} phase is critical — {'boundaries now set the tone for the innings' if phase=='Powerplay' else 'smart batting here decides the outcome'}.")
    if venue["pace"]:
        lines.append(f"{venue_name} has a pace-friendly surface — watch for extra bounce on back-of-length deliveries.")
    return lines


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏏 Match Setup")
    st.markdown("---")

    match_labels = [m["label"] for m in MATCHES]
    sel_match_idx = st.selectbox("Select match", range(len(MATCHES)), format_func=lambda i: MATCHES[i]["label"])
    sel_match = MATCHES[sel_match_idx]

    team_options = {tid: f"{t['short']} — {t['name']}" for tid, t in TEAMS.items()}
    batting_id = st.selectbox("Batting team", list(team_options.keys()),
                               format_func=lambda k: team_options[k],
                               index=list(team_options.keys()).index(sel_match["a"]))

    st.markdown("---")
    st.markdown("**Current innings**")
    runs    = st.number_input("Runs scored",      min_value=0,   max_value=300, value=86,  step=1)
    wickets = st.number_input("Wickets fallen",   min_value=0,   max_value=10,  value=3,   step=1)
    overs   = st.number_input("Overs completed",  min_value=0.0, max_value=20.0,value=11.0,step=0.1, format="%.1f")

    st.markdown("---")
    target  = st.number_input("Target (0 if batting first)", min_value=0, max_value=350, value=167, step=1)
    venue_name = st.selectbox("Venue", list(VENUES.keys()))

    st.markdown("---")
    st.markdown(
        '<div class="live-badge"><div class="live-dot"></div> Live analysis</div>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Data updated each season. Win probability uses a statistical model based on historical IPL data.")


# ── Main content ───────────────────────────────────────────────────────────────
team    = TEAMS[batting_id]
opp_id  = sel_match["b"] if batting_id == sel_match["a"] else sel_match["a"]
opp     = TEAMS[opp_id]
venue   = VENUES[venue_name]
is_chasing = target > 0
balls_left = round((20 - overs) * 6)
crr    = round(runs / overs, 2) if overs > 0 else 0
needed = target - runs if is_chasing else 0
req_rate = round(needed / balls_left * 6, 1) if (is_chasing and balls_left > 0) else 0
proj   = round(runs + crr * (20 - overs))
phase  = get_phase(overs)
prob   = calc_win_prob(batting_id, runs, wickets, overs, target, venue_name)
opp_prob = round(1 - prob, 4)

# ── Header ─────────────────────────────────────────────────────────────────────
col_title, col_badge = st.columns([5, 1])
with col_title:
    st.markdown(f"# IPL AI War Room")
    st.markdown(f"<p style='color:#8b95a8; font-size:14px; margin-top:-12px;'>Live match analysis — {team['name']} vs {opp['name']}</p>", unsafe_allow_html=True)

st.markdown("---")

# ── Win probability ────────────────────────────────────────────────────────────
pct_a = round(prob * 100)
pct_b = 100 - pct_a
st.markdown(f"""
<div class="win-bar-container">
  <div class="win-bar-title">Win probability</div>
  <div class="team-labels">
    <span style="color:{team['color']}">{team['short']}</span>
    <span style="color:{opp['color']}">{opp['short']}</span>
  </div>
  <div class="win-bar-outer">
    <div class="win-bar-a" style="width:{pct_a}%; background:{team['color']};"></div>
    <div class="win-bar-b" style="width:{pct_b}%; background:{opp['color']};"></div>
  </div>
  <div class="pct-labels"><span>{pct_a}%</span><span>{pct_b}%</span></div>
</div>
""", unsafe_allow_html=True)

# ── Metric cards ───────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.metric("Current RR",    f"{crr:.2f}",  "runs/over")
m2.metric(
    "Required RR" if is_chasing else "Proj. score",
    f"{req_rate:.2f}" if is_chasing else str(proj),
    "to win" if is_chasing else "at this rate",
)
m3.metric("Balls left",    str(balls_left))
m4.metric("Wickets left",  str(10 - wickets))

st.markdown("---")

# ── Situation snapshot + RR chart ──────────────────────────────────────────────
col_sit, col_chart = st.columns([1, 2])

with col_sit:
    st.markdown('<div class="section-header">Situation snapshot</div>', unsafe_allow_html=True)
    pressure = min(100, round(req_rate * 10 + wickets * 5)) if is_chasing else round((wickets / 3) * 30 + max(0, 8 - crr) * 5)
    pressure_label = "High" if pressure > 65 else "Medium" if pressure > 35 else "Low"
    pressure_color = "#ef4444" if pressure > 65 else "#f59e0b" if pressure > 35 else "#4caf7d"

    st.markdown(f"""
    <div class="sit-grid">
      <div class="sit-card"><div class="sit-label">Phase</div><div class="sit-value">{phase}</div></div>
      <div class="sit-card"><div class="sit-label">Pressure</div><div class="sit-value" style="color:{pressure_color}">{pressure_label} ({pressure}/100)</div></div>
      <div class="sit-card"><div class="sit-label">Venue avg</div><div class="sit-value">{venue['avg']} runs</div></div>
      <div class="sit-card"><div class="sit-label">Dew factor</div><div class="sit-value">{'Yes ✓' if venue['dew'] else 'No'}</div></div>
      <div class="sit-card"><div class="sit-label">Pitch type</div><div class="sit-value">{'Pace' if venue['pace'] else 'Spin'}-friendly</div></div>
      {'<div class="sit-card"><div class="sit-label">Needed</div><div class="sit-value">' + str(needed) + ' off ' + str(balls_left) + ' balls</div></div>' if is_chasing else ''}
    </div>
    """, unsafe_allow_html=True)

with col_chart:
    st.markdown('<div class="section-header">Run rate progression</div>', unsafe_allow_html=True)
    st.plotly_chart(build_rr_chart(runs, overs, target, venue_name), use_container_width=True)

st.markdown("---")

# ── Strategy + Analysis ────────────────────────────────────────────────────────
col_strat, col_analysis = st.columns(2)

with col_strat:
    st.markdown('<div class="section-header">AI strategy advisor</div>', unsafe_allow_html=True)
    for tag, typ, text in get_strategies(runs, wickets, overs, target, venue_name, phase):
        tag_class = f"tag-{typ}"
        st.markdown(f"""
        <div class="strategy-card">
          <div class="strategy-tag {tag_class}">{tag}</div>
          <div class="strategy-text">{text}</div>
        </div>""", unsafe_allow_html=True)

with col_analysis:
    st.markdown('<div class="section-header">Plain-English analysis</div>', unsafe_allow_html=True)
    for line in get_analysis(batting_id, opp_id, runs, wickets, overs, target, venue_name, prob, phase):
        st.markdown(f'<div class="analysis-card"><div class="analysis-text">{line}</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ── Key players ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Key players to watch</div>', unsafe_allow_html=True)
tab_bat, tab_bowl = st.tabs(["Batting", "Bowling"])

with tab_bat:
    col_bat_a, col_bat_b = st.columns(2)
    with col_bat_a:
        st.markdown(f"**{team['short']} — Batting**")
        st.plotly_chart(build_player_chart(team["batters"], "bat"), use_container_width=True)
        df_bat = pd.DataFrame(team["batters"])[["name","avg","sr","form"]]
        df_bat.columns = ["Player","Avg","SR","Form"]
        st.dataframe(df_bat, hide_index=True, use_container_width=True)
    with col_bat_b:
        st.markdown(f"**{opp['short']} — Batting**")
        st.plotly_chart(build_player_chart(opp["batters"], "bat"), use_container_width=True)
        df_bat2 = pd.DataFrame(opp["batters"])[["name","avg","sr","form"]]
        df_bat2.columns = ["Player","Avg","SR","Form"]
        st.dataframe(df_bat2, hide_index=True, use_container_width=True)

with tab_bowl:
    col_bwl_a, col_bwl_b = st.columns(2)
    with col_bwl_a:
        st.markdown(f"**{team['short']} — Bowling**")
        st.plotly_chart(build_player_chart(team["bowlers"], "bowl"), use_container_width=True)
        df_bwl = pd.DataFrame(team["bowlers"])[["name","econ","wkts","form"]]
        df_bwl.columns = ["Player","Economy","Wickets","Form"]
        st.dataframe(df_bwl, hide_index=True, use_container_width=True)
    with col_bwl_b:
        st.markdown(f"**{opp['short']} — Bowling**")
        st.plotly_chart(build_player_chart(opp["bowlers"], "bowl"), use_container_width=True)
        df_bwl2 = pd.DataFrame(opp["bowlers"])[["name","econ","wkts","form"]]
        df_bwl2.columns = ["Player","Economy","Wickets","Form"]
        st.dataframe(df_bwl2, hide_index=True, use_container_width=True)

st.markdown("---")
st.caption("IPL AI War Room · Built with Streamlit + Plotly · No external APIs — pure data & logic")