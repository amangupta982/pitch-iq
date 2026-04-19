"""
pages/session_notes.py
──────────────────────
Coach's notepad — plain-text session notes with export.

Stored in st.session_state so notes persist across page switches
within the same session.  Export as downloadable .txt file.
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st


def render() -> None:
    """Render the Session Notes page."""
    ms = st.session_state.get("match_state")
    match = st.session_state.get("match")

    st.markdown(
        '<h2 style="margin-bottom:0.1rem;">📝 Session Notes</h2>'
        '<p style="color:#6b7280;font-size:0.85rem;margin-top:0;">'
        'Private coaching notes — saved within this session</p>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ── Match context header ─────────────────────────────────────────
    if match:
        st.markdown(
            f'<div class="pitchiq-card">'
            f'<div style="font-weight:700;color:#f0f4ff;">{match.get("title", "")}</div>'
            f'<div style="color:#9ca3af;font-size:0.8rem;">'
            f'{match.get("venue", "")} · '
            f'{datetime.now().strftime("%d %b %Y, %I:%M %p")}</div></div>',
            unsafe_allow_html=True,
        )

    # ── Quick-insert buttons ─────────────────────────────────────────
    st.markdown("### ⚡ Quick Insert")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📌 Key Moment", key="qi_moment", use_container_width=True):
            _append_note(f"\n📌 [{_timestamp()}] KEY MOMENT: ")

    with col2:
        if st.button("🏏 Batting Note", key="qi_batting", use_container_width=True):
            batter_info = ""
            if ms:
                batter_info = f" ({ms.runs}/{ms.wickets}, {ms.overs} ov)"
            _append_note(f"\n🏏 [{_timestamp()}] BATTING{batter_info}: ")

    with col3:
        if st.button("🎯 Bowling Note", key="qi_bowling", use_container_width=True):
            _append_note(f"\n🎯 [{_timestamp()}] BOWLING: ")

    with col4:
        if st.button("🔀 Sub Note", key="qi_sub", use_container_width=True):
            _append_note(f"\n🔀 [{_timestamp()}] IMPACT SUB: ")

    st.markdown("---")

    # ── Auto-generate situation summary ──────────────────────────────
    if ms and st.button("🤖 Auto-Generate Situation Summary", use_container_width=True, key="auto_summary"):
        summary = _generate_summary(ms)
        _append_note(f"\n\n{'='*50}\n📊 AUTO SUMMARY [{_timestamp()}]\n{'='*50}\n{summary}\n")
        st.rerun()

    # ── Notes text area ──────────────────────────────────────────────
    st.markdown("### 📄 Notes")
    current_notes = st.session_state.get("session_notes", "")

    updated_notes = st.text_area(
        "Session Notes",
        value=current_notes,
        height=400,
        key="notes_editor",
        label_visibility="collapsed",
        placeholder=(
            "Start typing your coaching notes here...\n\n"
            "Tips:\n"
            "• Use quick-insert buttons above for timestamped entries\n"
            "• Click 'Auto-Generate' for a situation snapshot\n"
            "• Notes persist while the app is running\n"
            "• Export as .txt when done"
        ),
    )

    if updated_notes != current_notes:
        st.session_state.session_notes = updated_notes

    st.markdown("---")

    # ── Export + controls ────────────────────────────────────────────
    col_export, col_clear, col_stats = st.columns([2, 1, 2])

    with col_export:
        match_title = match.get("title", "match") if match else "session"
        filename = f"pitchiq_notes_{match_title.replace(' ', '_').replace(',', '')}.txt"
        export_content = _build_export(updated_notes, match)

        st.download_button(
            label="📥 Export Notes (.txt)",
            data=export_content,
            file_name=filename,
            mime="text/plain",
            use_container_width=True,
        )

    with col_clear:
        if st.button("🗑️ Clear", key="clear_notes", use_container_width=True):
            st.session_state.session_notes = ""
            st.rerun()

    with col_stats:
        word_count = len(updated_notes.split()) if updated_notes else 0
        line_count = updated_notes.count("\n") + 1 if updated_notes else 0
        st.markdown(
            f'<div style="color:#6b7280;font-size:0.8rem;padding-top:0.5rem;">'
            f'📊 {word_count} words · {line_count} lines</div>',
            unsafe_allow_html=True,
        )


def _timestamp() -> str:
    """Return current time as HH:MM string."""
    return datetime.now().strftime("%H:%M")


def _append_note(text: str) -> None:
    """
    Append text to session notes.

    Parameters
    ----------
    text : str   the text to append
    """
    current = st.session_state.get("session_notes", "")
    st.session_state.session_notes = current + text


def _generate_summary(ms) -> str:
    """
    Auto-generate a situation summary from current MatchState.

    Parameters
    ----------
    ms : MatchState

    Returns
    -------
    str   multi-line summary text.
    """
    lines = []
    bat_name = ms.batting_team.get("short", "BAT")
    bowl_name = ms.bowling_team.get("short", "BOWL")

    lines.append(f"Match: {bat_name} vs {bowl_name}")
    lines.append(f"Score: {ms.runs}/{ms.wickets} after {ms.overs} overs")
    lines.append(f"Phase: {ms.phase.upper()}")
    lines.append(f"CRR: {ms.crr:.2f}")

    if ms.is_chasing:
        lines.append(f"Target: {ms.target}")
        lines.append(f"Runs needed: {ms.runs_needed}")
        lines.append(f"RRR: {ms.rrr:.2f}" if ms.rrr else "RRR: N/A")
    else:
        lines.append(f"Projected score: {ms.proj_score}")

    lines.append(f"Balls remaining: {ms.balls_left}")
    lines.append(f"Wickets in hand: {10 - ms.wickets}")

    return "\n".join(lines)


def _build_export(notes: str, match: dict | None) -> str:
    """
    Build a complete export string with header.

    Parameters
    ----------
    notes : str     raw notes text
    match : dict    match info

    Returns
    -------
    str   full export content.
    """
    header = [
        "=" * 60,
        "PITCHIQ — SESSION NOTES",
        "=" * 60,
        f"Date: {datetime.now().strftime('%d %b %Y, %I:%M %p')}",
    ]

    if match:
        header.append(f"Match: {match.get('title', 'N/A')}")
        header.append(f"Venue: {match.get('venue', 'N/A')}")

    header.append("=" * 60)
    header.append("")

    return "\n".join(header) + "\n" + (notes or "(No notes)")
