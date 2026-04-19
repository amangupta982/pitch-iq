"""
app.py — PitchIQ v2 Entry Point
════════════════════════════════
Production-grade IPL cricket coaching intelligence system.

Runs as:  streamlit run app.py

Architecture:
    • Streamlit wide-layout, dark theme
    • Sidebar: match selector, navigation, refresh, debug
    • Pages: War Room, Batting Order, Bowling Plan,
             Matchup Matrix, Impact Sub, Session Notes
    • Data flows through core/state.py only — pages never fetch directly
"""

import streamlit as st

# ── Page config MUST be first Streamlit call ─────────────────────────
st.set_page_config(
    page_title="PitchIQ — IPL Coaching Intelligence",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "PitchIQ v2 — Real-time IPL coaching intelligence system",
    },
)

# ── Inject styles + init state ───────────────────────────────────────
from components.styles import inject_css
from core.state import init_state
from components.sidebar import render_sidebar

inject_css()
init_state()

# ── Render sidebar (match selector, nav, refresh) ────────────────────
render_sidebar()

# ── Route to current page ────────────────────────────────────────────
page = st.session_state.get("current_page", "war_room")

if page == "war_room":
    from pages.war_room import render
    render()
elif page == "batting_order":
    from pages.batting_order import render
    render()
elif page == "bowling_plan":
    from pages.bowling_plan import render
    render()
elif page == "matchup_matrix":
    from pages.matchup_matrix import render
    render()
elif page == "impact_sub":
    from pages.impact_sub import render
    render()
elif page == "session_notes":
    from pages.session_notes import render
    render()
else:
    from pages.war_room import render
    render()

# ── Auto-refresh (every 30 seconds) ─────────────────────────────────
import time

if st.session_state.get("auto_refresh", True):
    match = st.session_state.get("match")
    if match and match.get("status") == "live":
        last = st.session_state.get("last_updated", 0)
        if time.time() - last > 30:
            from core.state import refresh_live_score
            refresh_live_score()
            st.rerun()
