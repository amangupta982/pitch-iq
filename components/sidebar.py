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

        source = matches[0]["source"] if matches else "mock"

        # ── Data source status banner ──────────────────────────────────────────
        if source == "api":
            st.success("🟢 Live data — cricketdata.org API")
        elif source == "scraper":
            st.warning("🟡 Live data — Cricbuzz scraper")
        else:
            st.info("🔵 Demo mode — no live matches right now")
            st.caption("The app will automatically switch to live data when IPL matches are in progress.")

        labels  = [m["label"] for m in matches]
        sel_idx = st.selectbox(
            "Select match", range(len(labels)),
            format_func=lambda i: labels[i],
            key="match_sel",
        )
        st.session_state["active_match"] = matches[sel_idx]

        st.markdown("---")
        st.markdown("**Navigation**")

        if "page" not in st.session_state:
            st.session_state["page"] = "war_room"

        for key, (label, _) in pages.items():
            active = st.session_state["page"] == key
            btn_type = "primary" if active else "secondary"
            if st.button(label, key=f"nav_{key}", use_container_width=True, type=btn_type):
                st.session_state["page"] = key

        st.markdown("---")

        # ── Data source legend ─────────────────────────────────────────────────
        with st.expander("ℹ️ Data source info"):
            st.markdown("""
**How data works:**

1. 🟢 **API** — cricketdata.org free key  
   Set `CRICDATA_KEY` in your `.env` file

2. 🟡 **Scraper** — Cricbuzz (no key needed)  
   Auto-used when API has no matches

3. 🔵 **Demo** — Built-in mock data  
   Used when no live matches are on

The app switches automatically — you don't need to do anything.
            """)

        st.caption("PitchIQ v1.0 · IPL 2026")

    return st.session_state["page"]