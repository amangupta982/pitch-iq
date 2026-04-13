"""pages/batting_order.py — Who bats next, with situational justification."""
import streamlit as st
import plotly.graph_objects as go
from core.engine import MatchState, batting_order_recommendation
from data.teams_db import TEAMS, VENUES

def render():
    st.markdown("## 🏏 Batting Order Advisor")
    st.markdown("*Who should come in next — ranked by the current match situation.*")
    st.markdown('<div class="section-hdr">Setup</div>', unsafe_allow_html=True)

    teams_list  = list(TEAMS.keys())
    team_labels = {k: f"{v['short']} — {v['name']}" for k, v in TEAMS.items()}

    c1,c2,c3,c4,c5 = st.columns(5)
    batting_id = c1.selectbox("Batting team", teams_list, format_func=lambda k: team_labels[k])
    runs       = c2.number_input("Runs",    0, 300, 86,  step=1)
    wickets    = c3.number_input("Wickets", 0, 10,  3,   step=1)
    overs      = c4.number_input("Overs",   0.0, 20.0, 11.0, step=0.1, format="%.1f")
    target     = c5.number_input("Target",  0, 350, 167, step=1)
    venue      = st.selectbox("Venue", list(VENUES.keys()))

    ms = MatchState(batting_id=batting_id, bowling_id=batting_id,
                    runs=runs, wickets=wickets, overs=overs,
                    target=target, venue_name=venue)

    team     = TEAMS[batting_id]
    batters  = team["batters"]

    # Let coach mark who's already out
    st.markdown('<div class="section-hdr">Mark dismissed batters</div>', unsafe_allow_html=True)
    dismissed = []
    cols = st.columns(len(batters))
    for i, b in enumerate(batters):
        if cols[i].checkbox(b["name"], key=f"out_{b['name']}"):
            dismissed.append(b["name"])

    available = [b for b in batters if b["name"] not in dismissed]
    ranked    = batting_order_recommendation(ms, available)

    st.markdown('<div class="section-hdr">Recommended batting order</div>', unsafe_allow_html=True)

    for rank, b in enumerate(ranked, 1):
        score_pct = min(100, round(b["situation_score"] / 2))
        color = "#4caf7d" if rank == 1 else "#f59e0b" if rank == 2 else "#8b95a8"
        badge = "Send now" if rank == 1 else f"#{rank}"
        badge_cls = "badge-ok" if rank == 1 else "badge-warn" if rank == 2 else "badge-info"
        st.markdown(f"""
        <div class="card {'card-green' if rank==1 else 'card-amber' if rank==2 else ''}">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
            <div>
              <span class="badge {badge_cls}">{badge}</span>
              <span style="font-size:15px;font-weight:600;color:#f0f4ff;margin-left:8px;">{b['name']}</span>
            </div>
            <span style="font-size:12px;color:#8b95a8;">Situation score: {b['situation_score']}</span>
          </div>
          <div style="font-size:12px;color:#8b95a8;margin-bottom:8px;">
            Avg {b['avg']} &nbsp;|&nbsp; SR {b['sr']} &nbsp;|&nbsp; Death SR {b.get('death_sr', b['sr'])} &nbsp;|&nbsp; Form {b['form']}/100
          </div>
          <div style="font-size:13px;color:#c8d0e0;font-style:italic;">{b['rationale']}</div>
        </div>""", unsafe_allow_html=True)

    # Form chart
    st.markdown('<div class="section-hdr">Player form comparison</div>', unsafe_allow_html=True)
    names  = [b["name"] for b in ranked]
    form   = [b["form"] for b in ranked]
    sr_val = [b["sr"] for b in ranked]
    colors = ["#4caf7d" if f >= 80 else "#f59e0b" if f >= 65 else "#6b7280" for f in form]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Form", x=names, y=form, marker_color=colors, opacity=0.9))
    fig.add_trace(go.Scatter(name="SR", x=names, y=sr_val, mode="lines+markers",
                             line=dict(color="#60a5fa",width=2), yaxis="y2"))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#111827",
        font=dict(color="#9ca3af",family="Inter"), height=260,
        margin=dict(l=10,r=60,t=10,b=10),
        yaxis=dict(title="Form",gridcolor="#1e2535",range=[0,110]),
        yaxis2=dict(title="Strike Rate",overlaying="y",side="right",gridcolor="#1e2535"),
        legend=dict(font=dict(size=11),bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(tickfont=dict(size=11)),
        barmode="group",
    )
    st.plotly_chart(fig, use_container_width=True)
