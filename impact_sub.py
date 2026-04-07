"""pages/impact_sub.py — Impact substitution advisor."""
import streamlit as st
from core.engine import MatchState, impact_sub_recommendation
from data.teams_db import TEAMS, VENUES

def render():
    st.markdown("## 🔄 Impact Sub Advisor")
    st.markdown("*IPL 2026 Impact Player rule — who to bring in and when.*")

    teams_list  = list(TEAMS.keys())
    team_labels = {k: f"{v['short']} — {v['name']}" for k, v in TEAMS.items()}

    c1,c2,c3,c4,c5 = st.columns(5)
    team_id = c1.selectbox("Your team", teams_list, format_func=lambda k: team_labels[k])
    opp_id  = c2.selectbox("Opposition", teams_list, format_func=lambda k: team_labels[k], index=1)
    runs    = c3.number_input("Runs", 0, 300, 86, step=1)
    wickets = c4.number_input("Wickets", 0, 10, 3, step=1)
    overs   = c5.number_input("Overs", 0.0, 20.0, 10.0, step=0.1, format="%.1f")
    target  = st.number_input("Target (0 if first innings)", 0, 350, 167, step=1)
    venue   = st.selectbox("Venue", list(VENUES.keys()))

    ms = MatchState(batting_id=team_id, bowling_id=opp_id,
                    runs=runs, wickets=wickets, overs=overs,
                    target=target, venue_name=venue)

    team  = TEAMS[team_id]
    squad = team.get("squad", [])

    # Who's been used already
    st.markdown('<div class="section-hdr">Players already used (playing XI)</div>', unsafe_allow_html=True)
    all_players = [b["name"] for b in team["batters"]] + [b["name"] for b in team["bowlers"]]
    used = st.multiselect("Mark as used", all_players, default=all_players[:6])

    rec = impact_sub_recommendation(ms, squad, used)

    st.markdown('<div class="section-hdr">Impact sub recommendation</div>', unsafe_allow_html=True)
    if rec["player"]:
        p = rec["player"]
        st.markdown(f"""
        <div class="card card-green">
          <span class="badge badge-ok">Recommended sub</span>
          <div style="font-size:18px;font-weight:700;color:#f0f4ff;margin-bottom:6px;">{p['name']}</div>
          <div style="font-size:12px;color:#8b95a8;margin-bottom:6px;">Role: {p.get('role','').title()} &nbsp;|&nbsp; Form: {p.get('form',0)}/100</div>
          <div style="font-size:13px;color:#c8d0e0;margin-bottom:8px;">{rec['reason']}</div>
          <div style="font-size:12px;color:#f59e0b;font-weight:500;">⏱ Timing: {rec['timing']}</div>
        </div>""", unsafe_allow_html=True)

        if rec.get("alternatives"):
            st.markdown("**Alternative options:**")
            for alt in rec["alternatives"]:
                st.markdown(f'<div class="card"><span style="color:#c8d0e0;font-weight:500">{alt["name"]}</span> — {alt.get("role","").title()}, Form {alt.get("form",0)}/100</div>', unsafe_allow_html=True)
    else:
        st.info("No squad players available for substitution.")
