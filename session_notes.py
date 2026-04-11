"""pages/session_notes.py — Coach's match notepad with export."""
import streamlit as st
from datetime import datetime

def render():
    st.markdown("## 📋 Session Notes")
    st.markdown("*Real-time coaching notes — exportable after the match.*")

    if "notes" not in st.session_state:
        st.session_state["notes"] = []

    st.markdown('<div class="section-hdr">Add note</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    with c1:
        note_text = st.text_input("Note", placeholder="e.g. Kohli struggling against short-pitch pace — set leg-side trap", label_visibility="collapsed")
    with c2:
        category = st.selectbox("Category", ["Batting", "Bowling", "Field", "Strategy", "Injury", "Other"], label_visibility="collapsed")

    if st.button("Add note", use_container_width=False):
        if note_text.strip():
            st.session_state["notes"].append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "category": category,
                "text": note_text.strip(),
            })
            st.rerun()

    st.markdown('<div class="section-hdr">Notes this session</div>', unsafe_allow_html=True)

    cat_colors = {
        "Batting": "#3b82f6", "Bowling": "#f59e0b", "Field": "#4caf7d",
        "Strategy": "#a78bfa", "Injury": "#ef4444", "Other": "#8b95a8",
    }

    if not st.session_state["notes"]:
        st.markdown('<div class="card"><span style="color:#8b95a8;font-size:13px;">No notes yet — add your first observation above.</span></div>', unsafe_allow_html=True)
    else:
        filter_cat = st.multiselect("Filter by category", list(cat_colors.keys()), default=list(cat_colors.keys()))
        for i, n in enumerate(reversed(st.session_state["notes"])):
            if n["category"] not in filter_cat:
                continue
            color = cat_colors.get(n["category"], "#8b95a8")
            st.markdown(f"""
            <div class="card" style="border-left:3px solid {color};">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                <span style="font-size:11px;font-weight:600;color:{color};text-transform:uppercase">{n['category']}</span>
                <span style="font-size:11px;color:#5a6478">{n['time']}</span>
              </div>
              <div style="font-size:13px;color:#c8d0e0">{n['text']}</div>
            </div>""", unsafe_allow_html=True)

        # Export
        st.markdown('<div class="section-hdr">Export</div>', unsafe_allow_html=True)
        export_text = "\n".join([f"[{n['time']}] [{n['category']}] {n['text']}" for n in st.session_state["notes"]])
        st.download_button(
            label="Download notes as .txt",
            data=export_text,
            file_name=f"pitchiq_notes_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
        )
        if st.button("Clear all notes", type="secondary"):
            st.session_state["notes"] = []
            st.rerun()
