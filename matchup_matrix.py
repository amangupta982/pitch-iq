"""pages/matchup_matrix.py — Batter vs bowler threat map."""
import streamlit as st
import plotly.graph_objects as go
from core.engine import matchup_matrix
from data.teams_db import TEAMS

def render():
    st.markdown("## ⚔️ Matchup Matrix")
    st.markdown("*Batter vs bowler advantage map — red = batter danger, green = bowler dominates.*")

    teams_list  = list(TEAMS.keys())
    team_labels = {k: f"{v['short']} — {v['name']}" for k, v in TEAMS.items()}

    c1, c2 = st.columns(2)
    bat_id  = c1.selectbox("Batting team",  teams_list, format_func=lambda k: team_labels[k], index=0)
    bwl_id  = c2.selectbox("Bowling team",  teams_list, format_func=lambda k: team_labels[k], index=1)

    bat_team = TEAMS[bat_id]
    bwl_team = TEAMS[bwl_id]

    matrix = matchup_matrix(bat_team["batters"], bwl_team["bowlers"])

    # Heatmap
    batters_names = [b["name"] for b in bat_team["batters"]]
    bowler_names  = [b["name"] for b in bwl_team["bowlers"]]

    z = []
    text = []
    for batter in batters_names:
        row = []
        trow = []
        for bowler in bowler_names:
            m = next((x for x in matrix if x["batter"]==batter and x["bowler"]==bowler), None)
            val = m["advantage"] if m else 0
            row.append(val)
            trow.append(f"{m['label']}<br>{m['tip']}" if m else "")
        z.append(row)
        text.append(trow)

    fig = go.Figure(go.Heatmap(
        z=z, x=bowler_names, y=batters_names,
        colorscale=[[0,"#1a4a2e"],[0.5,"#2d3548"],[1,"#4a1515"]],
        zmin=-15, zmax=15,
        text=text, hoverinfo="text",
        showscale=True,
        colorbar=dict(title="Advantage<br>(+bat / -bowl)", tickfont=dict(color="#9ca3af"), titlefont=dict(color="#9ca3af")),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#111827",
        font=dict(color="#9ca3af",family="Inter"), height=300,
        margin=dict(l=10,r=10,t=10,b=10),
        xaxis=dict(tickfont=dict(size=10),side="bottom"),
        yaxis=dict(tickfont=dict(size=10)),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Top matchup alerts
    st.markdown('<div class="section-hdr">Key matchup alerts</div>', unsafe_allow_html=True)
    danger = [m for m in matrix if m["advantage"] > 5]
    dominant = [m for m in matrix if m["advantage"] < -5]

    if danger:
        st.markdown("**Batter danger zones** — avoid these matchups or set aggressive fields")
        for m in danger[:3]:
            st.markdown(f'<div class="card card-red"><span style="color:#ef4444;font-weight:600">{m["batter"]} vs {m["bowler"]}</span> — {m["tip"]}</div>', unsafe_allow_html=True)
    if dominant:
        st.markdown("**Bowler advantages** — target these matchups")
        for m in dominant[:3]:
            st.markdown(f'<div class="card card-green"><span style="color:#4caf7d;font-weight:600">{m["batter"]} vs {m["bowler"]}</span> — {m["tip"]}</div>', unsafe_allow_html=True)
