"""pages/bowling_plan.py — Over-by-over bowling assignments with field hints."""
import streamlit as st
import plotly.graph_objects as go
from core.engine import MatchState, bowling_plan, field_placement_hints
from data.teams_db import TEAMS, VENUES

def render():
    st.markdown("## 🎳 Bowling Plan")
    st.markdown("*Over-by-over bowling assignments, field placements and line/length.*")
    st.markdown('<div class="section-hdr">Match state</div>', unsafe_allow_html=True)

    teams_list  = list(TEAMS.keys())
    team_labels = {k: f"{v['short']} — {v['name']}" for k, v in TEAMS.items()}

    c1,c2,c3,c4 = st.columns(4)
    bowling_id = c1.selectbox("Bowling team", teams_list, format_func=lambda k: team_labels[k], index=1)
    batting_id = c2.selectbox("Batting team", teams_list, format_func=lambda k: team_labels[k], index=0)
    overs      = c3.number_input("Current over", 0.0, 20.0, 10.0, step=1.0, format="%.1f")
    venue      = c4.selectbox("Venue", list(VENUES.keys()))

    c5,c6,c7 = st.columns(3)
    runs    = c5.number_input("Runs conceded", 0, 300, 80, step=1)
    wickets = c6.number_input("Wickets taken", 0, 10, 2,  step=1)
    target  = c7.number_input("Target (if defending)", 0, 350, 175, step=1)

    ms = MatchState(batting_id=batting_id, bowling_id=bowling_id,
                    runs=runs, wickets=wickets, overs=overs,
                    target=target, venue_name=venue)

    bowl_team = TEAMS[bowling_id]
    bat_team  = TEAMS[batting_id]
    bowlers   = bowl_team["bowlers"]
    batters   = bat_team["batters"][:2]   # openers / current pair

    # Overs remaining per bowler
    st.markdown('<div class="section-hdr">Bowling quotas remaining</div>', unsafe_allow_html=True)
    overs_used = {}
    quota_cols = st.columns(len(bowlers))
    for i, b in enumerate(bowlers):
        used = quota_cols[i].number_input(f"{b['name']} overs used", 0, 4, 2, step=1, key=f"quota_{b['name']}")
        overs_used[b["name"]] = used
    available_bowlers = [b for b in bowlers if overs_used.get(b["name"], 0) < 4]

    plans = bowling_plan(ms, available_bowlers, batters)

    st.markdown('<div class="section-hdr">Over-by-over plan</div>', unsafe_allow_html=True)

    for p in plans:
        phase = "Powerplay" if p["over"] <= 6 else "Death" if p["over"] >= 17 else "Middle"
        phase_color = "#60a5fa" if phase == "Powerplay" else "#ef4444" if phase == "Death" else "#f59e0b"
        st.markdown(f"""
        <div class="card">
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
            <span style="font-size:18px;font-weight:700;color:#f0f4ff;min-width:50px;">Over {p['over']}</span>
            <span style="font-size:12px;font-weight:600;color:{phase_color};background:rgba(0,0,0,0.3);
                         padding:2px 8px;border-radius:6px;border:1px solid {phase_color}33;">{phase}</span>
            <span style="font-size:14px;font-weight:600;color:#f0f4ff;">{p['bowler']}</span>
          </div>
          <div style="font-size:12px;color:#8b95a8;margin-bottom:4px;">Line & length: <span style="color:#c8d0e0">{p['line']}</span></div>
          <div style="font-size:13px;color:#c8d0e0;font-style:italic;">{p['reasoning']}</div>
        </div>""", unsafe_allow_html=True)

    # Economy chart
    st.markdown('<div class="section-hdr">Bowler economy comparison</div>', unsafe_allow_html=True)
    names   = [b["name"] for b in bowlers]
    econs   = [b["econ"] for b in bowlers]
    d_econs = [b.get("death_econ", b["econ"]) for b in bowlers]
    colors  = ["#4caf7d" if e < 8 else "#f59e0b" if e < 9 else "#ef4444" for e in econs]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Overall economy", x=names, y=econs, marker_color=colors, opacity=0.85))
    fig.add_trace(go.Bar(name="Death economy",   x=names, y=d_econs, marker_color="#60a5fa", opacity=0.6))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#111827",
        font=dict(color="#9ca3af",family="Inter"), height=240,
        margin=dict(l=10,r=10,t=10,b=10), barmode="group",
        yaxis=dict(title="Economy",gridcolor="#1e2535"),
        xaxis=dict(tickfont=dict(size=11)),
        legend=dict(font=dict(size=11),bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Field hints
    st.markdown('<div class="section-hdr">Field placement hints</div>', unsafe_allow_html=True)
    if plans and available_bowlers:
        bwl_name = plans[0]["bowler"]
        bwl_obj  = next((b for b in bowlers if b["name"] == bwl_name), bowlers[0])
        bat_obj  = batters[0] if batters else {"name": "Batter", "hand": "R"}
        hints    = field_placement_hints(bat_obj, bwl_obj, ms.phase)
        for h in hints:
            st.markdown(f'<div class="analysis-card"><div class="analysis-text">🎯 {h}</div></div>', unsafe_allow_html=True)
