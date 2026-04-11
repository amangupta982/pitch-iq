"""components/sidebar.py"""
import streamlit as st
from core.live_data import get_live_matches

def render_sidebar(pages: dict) -> str:
    with st.sidebar:
        st.markdown("## 🏏 PitchIQ")
        st.caption("Coaching Intelligence System")
        st.markdown("---")

        # Live match selector
        st.markdown("**Live match**")
        with st.spinner("Fetching matches..."):
            matches = get_live_matches()
        labels  = [m["label"] for m in matches]
        sel_idx = st.selectbox("Select match", range(len(labels)),
                               format_func=lambda i: labels[i], key="match_sel")
        sel = matches[sel_idx]
        src_color = "#4caf7d" if sel["source"] == "api" else "#f59e0b" if sel["source"] == "scraper" else "#8b95a8"
        st.markdown(f'<span style="font-size:11px;color:{src_color}">● Source: {sel["source"]}</span>', unsafe_allow_html=True)
        st.session_state["active_match"] = sel

        st.markdown("---")
        st.markdown("**Navigation**")

        icons = {"war_room":"🎯","batting_order":"🏏","bowling_plan":"🎳",
                 "matchup_matrix":"⚔️","impact_sub":"🔄","session_notes":"📋"}
        if "page" not in st.session_state:
            st.session_state["page"] = "war_room"

        for key, (label, _) in pages.items():
            active = st.session_state["page"] == key
            style  = "background:#2d3548;border-radius:8px;" if active else ""
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state["page"] = key

        st.markdown("---")
        st.caption("PitchIQ v1.0 · IPL 2026")

    return st.session_state["page"]
