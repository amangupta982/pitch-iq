import streamlit as st

st.set_page_config(
    page_title="PitchIQ — Coaching Intelligence",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.sidebar import render_sidebar
from components.styles import inject_styles
from pages import war_room, batting_order, bowling_plan, matchup_matrix, impact_sub, session_notes

inject_styles()

PAGES = {
    "war_room":       ("🎯 War Room",        war_room),
    "batting_order":  ("🏏 Batting Order",   batting_order),
    "bowling_plan":   ("🎳 Bowling Plan",    bowling_plan),
    "matchup_matrix": ("⚔️  Matchup Matrix", matchup_matrix),
    "impact_sub":     ("🔄 Impact Sub",      impact_sub),
    "session_notes":  ("📋 Session Notes",   session_notes),
}

page_key = render_sidebar(PAGES)
PAGES[page_key][1].render()
