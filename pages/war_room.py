"""pages/war_room.py — Live match overview with win probability."""
import streamlit as st
import plotly.graph_objects as go
from core.engine import MatchState, win_probability, pressure_index
from data.teams_db import TEAMS, VENUES

def render():
    st.markdown("## 🎯 War Room")
    st.markdown('<div class="section-hdr">Match situation controls</div>', unsafe_allow_html=True)

    teams_list = list(TEAMS.keys())
    team_labels = {k: f"{v['short']} — {v['name']}" for k, v in TEAMS.items()}

    c1, c2 = st.columns(2)
    with c1:
        batting_id = st.selectbox("Batting team", teams_list, format_func=lambda k: team_labels[k], index=0)
    with c2:
        bowling_id = st.selectbox("Bowling team", teams_list, format_func=lambda k: team_labels[k], index=1)

    c3, c4, c5, c6, c7, c8 = st.columns(6)
    runs    = c3.number_input("Runs",     0, 300, 86,  step=1)
    wickets = c4.number_input("Wickets",  0, 10,  3,   step=1)
    overs   = c5.number_input("Overs",    0.0, 20.0, 11.0, step=0.1, format="%.1f")
    target  = c6.number_input("Target",   0, 350, 167, step=1)
    venue   = c7.selectbox("Venue", list(VENUES.keys()), index=0)
    _       = c8.empty()

    ms = MatchState(batting_id=batting_id, bowling_id=bowling_id,
                    runs=runs, wickets=wickets, overs=overs,
                    target=target, venue_name=venue)

    bat_team = TEAMS[batting_id]
    bwl_team = TEAMS[bowling_id]
    prob_bat, prob_bwl = win_probability(ms)
    pindex   = pressure_index(ms)
    pct_a    = round(prob_bat * 100)
    pct_b    = 100 - pct_a

    st.markdown("---")
    # Win prob bar
    st.markdown(f"""
    <div class="card">
      <div class="section-hdr" style="margin-top:0">Win probability</div>
      <div style="display:flex;justify-content:space-between;font-weight:600;font-size:15px;margin-bottom:8px;">
        <span style="color:{bat_team['color']}">{bat_team['short']}  {pct_a}%</span>
        <span style="color:{bwl_team['color']}">{bwl_team['short']}  {pct_b}%</span>
      </div>
      <div class="win-bar-outer">
        <div style="width:{pct_a}%;background:{bat_team['color']};height:100%;border-radius:11px 0 0 11px;"></div>
        <div style="width:{pct_b}%;background:{bwl_team['color']};height:100%;border-radius:0 11px 11px 0;"></div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Metrics
    m1,m2,m3,m4,m5 = st.columns(5)
    m1.metric("Current RR",   f"{ms.crr:.2f}")
    m2.metric("Required RR" if ms.is_chasing else "Proj. score",
              f"{ms.rrr:.2f}" if ms.is_chasing else str(ms.proj_score))
    m3.metric("Balls left",   ms.balls_left)
    m4.metric("Wickets left", 10 - ms.wickets)
    m5.metric("Pressure",     pindex["label"],
              delta=f"{pindex['score']}/100")

    # RR Chart
    st.markdown('<div class="section-hdr">Run rate progression</div>', unsafe_allow_html=True)
    st.plotly_chart(_rr_chart(ms, venue), use_container_width=True)

    # Analysis
    st.markdown('<div class="section-hdr">Plain-English analysis</div>', unsafe_allow_html=True)
    for line in _analysis(ms, bat_team, bwl_team):
        st.markdown(f'<div class="analysis-card"><div class="analysis-text">{line}</div></div>', unsafe_allow_html=True)


def _rr_chart(ms, venue_name):
    vavg   = VENUES[venue_name]["avg"]
    par_rr = vavg / 20
    labels = list(range(1, 21))
    actual = required = par = None

    actual   = [round(ms.runs * o / int(ms.overs)) if o <= int(ms.overs) and int(ms.overs)>0 else None for o in labels]
    par      = [round(par_rr * o, 1) for o in labels]
    needed   = ms.target - ms.runs
    ov_left  = 20 - int(ms.overs)
    required = [round(ms.runs + needed*(o - int(ms.overs))/ov_left) if ms.is_chasing and o >= int(ms.overs) and ov_left>0 else None for o in labels]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=labels, y=actual, name="Actual",   line=dict(color="#3b82f6",width=2.5), connectgaps=False))
    if ms.is_chasing:
        fig.add_trace(go.Scatter(x=labels, y=required, name="Required", line=dict(color="#ef4444",width=2,dash="dash"), connectgaps=False))
    fig.add_trace(go.Scatter(x=labels, y=par, name="Venue par", line=dict(color="#6b7280",width=1,dash="dot")))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#111827",
                      font=dict(color="#9ca3af",family="Inter"), height=220,
                      margin=dict(l=10,r=10,t=10,b=10),
                      legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,font=dict(size=11),bgcolor="rgba(0,0,0,0)"),
                      xaxis=dict(title="Over",tickfont=dict(size=10),gridcolor="#1e2535"),
                      yaxis=dict(title="Runs",tickfont=dict(size=10),gridcolor="#1e2535"),
                      hovermode="x unified")
    return fig

def _analysis(ms, bat_team, bwl_team):
    win_str = ("in a strong position" if ms.is_chasing and ms.rrr < 8
               else "under the pump" if ms.is_chasing and ms.rrr > 10
               else "building momentum" if not ms.is_chasing and ms.proj_score > VENUES[ms.venue_name]["avg"]
               else "slightly behind par")
    lines = [
        f"{bat_team['name']} are {win_str} — {round(win_probability(ms)[0]*100)}% win probability.",
    ]
    if ms.is_chasing:
        lines.append(f"Need {ms.target - ms.runs} from {ms.balls_left} balls (RRR {ms.rrr:.1f}).")
    else:
        lines.append(f"Projecting {ms.proj_score} at current rate vs venue avg {VENUES[ms.venue_name]['avg']}.")
    lines.append(f"Phase: {ms.phase} — {'powerplay boundaries set the tone' if ms.phase=='Powerplay' else 'death overs are the decider' if ms.phase=='Death overs' else 'middle overs build or break the innings'}.")
    return lines
