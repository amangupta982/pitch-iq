"""
components/sidebar.py
─────────────────────
PitchIQ sidebar: match selector, manual entry, live ticker, team selector,
navigation, refresh controls, and optional debug panel.

Called once per page render from app.py.
"""

from __future__ import annotations

import os
import time

import streamlit as st

from core.live_data import fetch_live_matches, DEBUG
from core.state import load_match, load_manual_match, refresh_live_score
from data.teams_db import get_all_teams


def render_sidebar() -> None:
    """
    Render the full sidebar.

    Sections:
        1. Logo / title
        2. Match mode toggle (Live API / Manual Entry)
        3. Match selector OR manual entry form
        4. Mini live ticker (from session_state.match)
        5. Team perspective selector
        6. Data source badge
        7. Last-updated + refresh button
        8. Navigation buttons (6 pages) — plain text + emoji only
        9. Debug panel (if DEBUG=true)
    """
    with st.sidebar:
        # ── Logo + Title ─────────────────────────────────────────────
        st.markdown("# 🏏 PitchIQ")
        st.markdown(
            '<p style="color:#6b7280;font-size:0.75rem;margin-top:-0.8rem;'
            'letter-spacing:2px;text-transform:uppercase;">COACHING INTELLIGENCE</p>',
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # ── Match Mode Toggle ────────────────────────────────────────
        mode = st.radio(
            "Match Data Source",
            options=["live", "manual"],
            format_func=lambda x: "📡 Live / Demo" if x == "live" else "✏️ Manual Entry",
            index=0 if st.session_state.get("match_mode", "live") == "live" else 1,
            key="match_mode_radio",
            horizontal=True,
            label_visibility="collapsed",
        )
        st.session_state.match_mode = mode

        if mode == "live":
            _render_live_mode()
        else:
            _render_manual_mode()

        # ── Live Ticker ──────────────────────────────────────────────
        match = st.session_state.get("match")
        if match:
            team_a = match.get("team_a", {})
            team_b = match.get("team_b", {})
            innings = match.get("innings", [])

            st.markdown(
                f'<div style="text-align:center;padding:0.5rem 0;">'
                f'<span style="color:{team_a.get("color", "#fff")};font-weight:800;font-size:1.1rem;">'
                f'{team_a.get("short", "?")}</span>'
                f'<span style="color:#4b5563;margin:0 0.5rem;font-size:0.85rem;">vs</span>'
                f'<span style="color:{team_b.get("color", "#fff")};font-weight:800;font-size:1.1rem;">'
                f'{team_b.get("short", "?")}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Show scores from innings data
            for inn in innings:
                team_key = inn.get("batting_team", "")
                runs = inn.get("runs", 0)
                wkts = inn.get("wickets", 0)
                overs = inn.get("overs", 0)

                # Resolve team short name
                short = ""
                if team_key == team_a.get("id"):
                    short = team_a.get("short", "")
                elif team_key == team_b.get("id"):
                    short = team_b.get("short", "")

                if not short:
                    inn_num = inn.get("inning_number", 0)
                    if inn_num == 1:
                        short = team_a.get("short", f"Inn {inn_num}")
                    elif inn_num == 2:
                        short = team_b.get("short", f"Inn {inn_num}")
                    else:
                        short = f"Inn {inn_num}"

                st.markdown(
                    f'<div style="text-align:center;color:#d1d5db;font-size:0.9rem;">'
                    f'{short}: <strong>{runs}/{wkts}</strong> ({overs} ov)</div>',
                    unsafe_allow_html=True,
                )

            # ── Source badge ─────────────────────────────────────────
            source = match.get("source", "mock")
            badge_map = {
                "api": ("🟢 Live API", "source-api"),
                "scraper": ("🟡 Scraper", "source-scraper"),
                "mock": ("🔵 Demo Mode", "source-mock"),
                "manual": ("🟣 Manual Entry", "source-manual"),
            }
            badge_text, badge_class = badge_map.get(source, ("⚪ Unknown", ""))
            st.markdown(
                f'<div style="text-align:center;margin:0.5rem 0;">'
                f'<span class="source-badge {badge_class}">{badge_text}</span></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="text-align:center;color:#6b7280;padding:1rem 0;">'
                '⏳ Select a match or enter manually</div>',
                unsafe_allow_html=True,
            )

        # ── Last Updated + Refresh ───────────────────────────────────
        last = st.session_state.get("last_updated")
        if last:
            ago = int(time.time() - last)
            st.markdown(
                f'<div style="text-align:center;color:#6b7280;font-size:0.75rem;">'
                f'Updated {ago}s ago</div>',
                unsafe_allow_html=True,
            )

        # Only show refresh for live mode
        if mode == "live":
            if st.button("🔄 Refresh Now", use_container_width=True, key="refresh_btn"):
                with st.spinner("Refreshing..."):
                    refresh_live_score()
                st.rerun()

        st.markdown("---")

        # ── Team Perspective Selector ─────────────────────────────────
        ms = st.session_state.get("match_state")
        if ms and match:
            bat_short = ms.batting_team.get("short", "BAT")
            bowl_short = ms.bowling_team.get("short", "BOWL")

            st.markdown(
                '<div style="font-size:0.75rem;color:#6b7280;text-transform:uppercase;'
                'letter-spacing:1px;margin-bottom:0.3rem;">Analyze Team</div>',
                unsafe_allow_html=True,
            )

            perspective = st.radio(
                "Team perspective",
                options=["batting", "bowling"],
                format_func=lambda x: f"🏏 {bat_short} (Batting)" if x == "batting" else f"🎯 {bowl_short} (Bowling)",
                index=0 if st.session_state.get("selected_perspective", "batting") == "batting" else 1,
                key="team_perspective_radio",
                label_visibility="collapsed",
                horizontal=True,
            )

            if perspective != st.session_state.get("selected_perspective"):
                st.session_state.selected_perspective = perspective

            st.markdown("---")

        # ── Navigation ───────────────────────────────────────────────
        phase_caption = ""
        if ms:
            phase_emoji = {"powerplay": "⚡ PP", "middle": "🔄 MID", "death": "💀 DEATH"}
            phase_caption = phase_emoji.get(ms.phase, "")

        pages = [
            ("war_room",       "📊 War Room"),
            ("batting_order",  "🏏 Batting Order"),
            ("bowling_plan",   "🎯 Bowling Plan"),
            ("matchup_matrix", "🔥 Matchup Matrix"),
            ("impact_sub",     "🔀 Impact Sub"),
            ("session_notes",  "📝 Session Notes"),
        ]

        current = st.session_state.get("current_page", "war_room")
        for page_id, label in pages:
            btn_type = "primary" if page_id == current else "secondary"
            if st.button(label, key=f"nav_{page_id}", use_container_width=True,
                        type=btn_type):
                st.session_state.current_page = page_id
                st.rerun()

            if page_id == "war_room" and phase_caption:
                st.markdown(
                    f'<div style="text-align:center;color:#9ca3af;font-size:0.7rem;'
                    f'margin-top:-0.5rem;margin-bottom:0.3rem;">Phase: {phase_caption}</div>',
                    unsafe_allow_html=True,
                )

        # ── Debug Panel ──────────────────────────────────────────────
        if DEBUG:
            st.markdown("---")
            with st.expander("🔧 Debug Info", expanded=False):
                st.markdown(f"**Source:** {match.get('source', 'N/A') if match else 'No match'}")
                api_key = os.getenv("CRICDATA_KEY", "")
                key_status = "✅ Set" if api_key and api_key != "your_free_key_from_cricketdata_org" else "❌ Not set"
                st.markdown(f"**API Key:** {key_status}")
                st.markdown(f"**Match ID:** {st.session_state.get('match_id', 'N/A')}")
                st.markdown(f"**Squad A:** {len(st.session_state.get('squad_a', []))} players")
                st.markdown(f"**Squad B:** {len(st.session_state.get('squad_b', []))} players")
                st.markdown(f"**Playing 11 A:** {len(st.session_state.get('playing_11_a', []))}")
                st.markdown(f"**Playing 11 B:** {len(st.session_state.get('playing_11_b', []))}")
                st.markdown(f"**Bench A:** {len(st.session_state.get('bench_a', []))}")
                st.markdown(f"**Bench B:** {len(st.session_state.get('bench_b', []))}")

                if ms:
                    st.markdown(f"**Batting:** {ms.batting_team.get('short', '?')}")
                    st.markdown(f"**Bowling:** {ms.bowling_team.get('short', '?')}")
                    st.markdown(f"**Phase:** {ms.phase}")

                logs = st.session_state.get("debug_log", [])
                if logs:
                    st.text_area("Log", "\n".join(logs[-20:]), height=200)


# ═══════════════════════════════════════════════════════════════════════
# LIVE MODE
# ═══════════════════════════════════════════════════════════════════════

def _render_live_mode() -> None:
    """Render the live/demo match selector."""
    matches = fetch_live_matches()
    if matches:
        match_titles = [m["title"] for m in matches]
        default_idx = 0
        for i, m in enumerate(matches):
            if m.get("status") == "live":
                default_idx = i
                break

        selected_idx = st.selectbox(
            "Select Match",
            range(len(match_titles)),
            format_func=lambda i: match_titles[i],
            index=default_idx,
            key="match_selector",
        )
        selected_match = matches[selected_idx]

        current_id = st.session_state.get("match_id")
        if current_id != selected_match["id"]:
            with st.spinner("Loading match data..."):
                load_match(selected_match["id"])


# ═══════════════════════════════════════════════════════════════════════
# MANUAL ENTRY MODE
# ═══════════════════════════════════════════════════════════════════════

def _render_manual_mode() -> None:
    """Render the manual match entry form for when API is unavailable."""
    all_teams = get_all_teams()
    team_ids = list(all_teams.keys())
    team_labels = [f"{all_teams[tid]['short']} — {all_teams[tid]['name']}" for tid in team_ids]

    st.markdown(
        '<div style="font-size:0.7rem;color:#a78bfa;font-weight:600;'
        'text-transform:uppercase;letter-spacing:1px;margin-bottom:0.3rem;">'
        '✏️ Create Match</div>',
        unsafe_allow_html=True,
    )

    # ── Team Selection ───────────────────────────────────────────────
    col_a, col_b = st.columns(2)
    with col_a:
        team_a_idx = st.selectbox(
            "Team A",
            range(len(team_ids)),
            format_func=lambda i: all_teams[team_ids[i]]["short"],
            index=0,
            key="manual_team_a",
        )
    with col_b:
        # Default to a different team
        default_b = min(1, len(team_ids) - 1)
        team_b_idx = st.selectbox(
            "Team B",
            range(len(team_ids)),
            format_func=lambda i: all_teams[team_ids[i]]["short"],
            index=default_b,
            key="manual_team_b",
        )

    team_a_id = team_ids[team_a_idx]
    team_b_id = team_ids[team_b_idx]

    if team_a_id == team_b_id:
        st.warning("⚠️ Select two different teams")
        return

    team_a_short = all_teams[team_a_id]["short"]
    team_b_short = all_teams[team_b_id]["short"]

    st.markdown("---")

    # ── Innings / Situation ──────────────────────────────────────────
    innings_type = st.radio(
        "Situation",
        options=["batting_first", "chasing"],
        format_func=lambda x: "🏏 Batting First" if x == "batting_first" else "🎯 Chasing",
        horizontal=True,
        key="manual_innings_type",
        label_visibility="collapsed",
    )

    # Which team is batting?
    batting_team_id = st.radio(
        "Currently Batting",
        options=[team_a_id, team_b_id],
        format_func=lambda x: f"🏏 {all_teams[x]['short']} batting",
        horizontal=True,
        key="manual_batting_team",
        label_visibility="collapsed",
    )

    # ── Score Input ──────────────────────────────────────────────────
    col_r, col_w, col_o = st.columns(3)
    with col_r:
        runs = st.number_input("Runs", min_value=0, max_value=400, value=85, step=1, key="manual_runs")
    with col_w:
        wickets = st.number_input("Wkts", min_value=0, max_value=10, value=2, step=1, key="manual_wkts")
    with col_o:
        overs = st.number_input("Overs", min_value=0.0, max_value=20.0, value=10.0, step=0.1,
                               format="%.1f", key="manual_overs")

    # ── Target (if chasing) ──────────────────────────────────────────
    target = None
    innings = 1
    if innings_type == "chasing":
        innings = 2
        target = st.number_input(
            "Target Score",
            min_value=50, max_value=400, value=175, step=1,
            key="manual_target",
        )

    # ── Start Analysis Button ────────────────────────────────────────
    if st.button("⚡ Start Analysis", use_container_width=True, key="manual_start",
                type="primary"):
        with st.spinner("Building match..."):
            load_manual_match(
                team_a_id=team_a_id,
                team_b_id=team_b_id,
                batting_team_id=batting_team_id,
                runs=int(runs),
                wickets=int(wickets),
                overs=float(overs),
                innings=innings,
                target=int(target) if target else None,
            )
        st.rerun()