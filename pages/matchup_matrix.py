"""
pages/matchup_matrix.py
───────────────────────
Batter × Bowler matchup heatmap — danger zones and advantages.

Uses LIVE Playing 11 only (not full squad).
Auto-highlights current batters and bowler.

Displays:
    • Interactive Plotly heatmap
    • Danger zones (batter dominates)
    • Bowler advantages
    • Field suggestions for the most dangerous matchup
"""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from core.engine import matchup_matrix, field_placement_hints
from core.state import get_batting_team_players, get_bowling_team_players
from components.cards import strategy_card, analysis_card


def render() -> None:
    """Render the Matchup Matrix page."""
    ms = st.session_state.get("match_state")
    if not ms:
        st.info("🔥 Select a match from the sidebar to begin.")
        return

    st.markdown(
        f'<h2 style="margin-bottom:0.1rem;">🔥 Matchup Matrix</h2>'
        f'<p style="color:#6b7280;font-size:0.85rem;margin-top:0;">'
        f'{ms.batting_team.get("short", "")} batters vs {ms.bowling_team.get("short", "")} bowlers</p>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ── Get players ──────────────────────────────────────────────────
    batting_players = get_batting_team_players()
    bowling_players = get_bowling_team_players()

    # Filter to relevant roles
    batters = [
        p for p in batting_players
        if p.get("role") in ("bat", "wk-bat", "allrounder")
    ]
    bowlers = [
        p for p in bowling_players
        if p.get("role") in ("bowl", "allrounder")
        or (p.get("profile", {}).get("econ") is not None)
    ]

    if not batters or not bowlers:
        st.warning("⚠️ Not enough player data to build matchup matrix.")
        return

    # ── Compute matchups ─────────────────────────────────────────────
    matchups = matchup_matrix(batters, bowlers)

    if not matchups:
        st.info("No matchup data available.")
        return

    # ── Find current players at crease ───────────────────────────────
    scorecard = st.session_state.get("scorecard", [])
    latest = scorecard[-1] if scorecard else {}
    at_crease_names = set()
    for b in latest.get("batters", []):
        if not b.get("dismissed", True):
            at_crease_names.add(b["name"].lower())

    current_bowler_name = ""
    bowler_list = latest.get("bowlers", [])
    if bowler_list:
        current_bowler_name = bowler_list[-1].get("name", "").lower()

    # ── Build heatmap data ───────────────────────────────────────────
    batter_names = list(dict.fromkeys(m["batter"] for m in matchups))
    bowler_names = list(dict.fromkeys(m["bowler"] for m in matchups))

    # Create score matrix
    z_matrix = []
    hover_text = []
    for bat in batter_names:
        row = []
        hover_row = []
        for bowl in bowler_names:
            match_data = next(
                (m for m in matchups if m["batter"] == bat and m["bowler"] == bowl),
                None,
            )
            if match_data:
                row.append(match_data["score"])
                hover_row.append(
                    f"{bat} vs {bowl}<br>"
                    f"Score: {match_data['score']}<br>"
                    f"{match_data['label']}<br>"
                    f"Bat hand: {match_data['bat_hand']} | Bowl: {match_data['bowl_type']}"
                )
            else:
                row.append(0)
                hover_row.append(f"{bat} vs {bowl}")
        z_matrix.append(row)
        hover_text.append(hover_row)

    # ── Annotate batter names with "at crease" marker ────────────────
    display_batter_names = []
    for name in batter_names:
        if name.lower() in at_crease_names:
            display_batter_names.append(f"⚡ {name}")
        else:
            display_batter_names.append(name)

    display_bowler_names = []
    for name in bowler_names:
        if name.lower() == current_bowler_name:
            display_bowler_names.append(f"🎯 {name}")
        else:
            display_bowler_names.append(name)

    # ── Render heatmap ───────────────────────────────────────────────
    fig = go.Figure(data=go.Heatmap(
        z=z_matrix,
        x=display_bowler_names,
        y=display_batter_names,
        text=hover_text,
        hoverinfo="text",
        colorscale=[
            [0.0, "#166534"],    # bowler dominates (green)
            [0.3, "#15803d"],
            [0.45, "#374151"],   # even (neutral)
            [0.55, "#374151"],
            [0.7, "#b91c1c"],
            [1.0, "#dc2626"],    # batter dominates (red)
        ],
        colorbar=dict(
            title=dict(
                text="← Bowler | Batter →",
                font=dict(color="#9ca3af", size=11),
            ),
            tickfont=dict(color="#9ca3af"),
            len=0.8,
        ),
        zmin=-15,
        zmax=15,
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#111827",
        font=dict(color="#9ca3af", family="Inter"),
        height=max(350, len(batter_names) * 45),
        margin=dict(l=120, r=20, t=20, b=80),
        xaxis=dict(
            side="bottom",
            tickangle=-45,
            gridcolor="#1f2937",
        ),
        yaxis=dict(
            autorange="reversed",
            gridcolor="#1f2937",
        ),
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Danger Zones + Bowler Advantages ─────────────────────────────
    col_danger, col_advantage = st.columns(2)

    danger_matchups = [m for m in matchups if m["score"] > 5]
    bowler_matchups = [m for m in matchups if m["score"] < -5]

    with col_danger:
        st.markdown("### 🔴 Danger Zones")
        if danger_matchups:
            for m in danger_matchups[:5]:
                st.markdown(
                    strategy_card(
                        "DANGER",
                        "danger",
                        f"<strong>{m['batter']}</strong> dominates <strong>{m['bowler']}</strong> "
                        f"(score: {m['score']:+.1f}). "
                        f"Bat: {m['bat_hand']}H vs {m['bowl_type']}. "
                        f"Avoid this matchup if possible.",
                    ),
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                '<div style="color:#6b7280;font-size:0.85rem;">No extreme danger zones detected.</div>',
                unsafe_allow_html=True,
            )

    with col_advantage:
        st.markdown("### 🟢 Bowler Advantages")
        if bowler_matchups:
            for m in bowler_matchups[:5]:
                st.markdown(
                    strategy_card(
                        "ADVANTAGE",
                        "success",
                        f"<strong>{m['bowler']}</strong> dominates <strong>{m['batter']}</strong> "
                        f"(score: {m['score']:+.1f}). "
                        f"{m['bowl_type']} vs {m['bat_hand']}H. "
                        f"Target this matchup.",
                    ),
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                '<div style="color:#6b7280;font-size:0.85rem;">No clear bowler advantages found.</div>',
                unsafe_allow_html=True,
            )

    # ── Field suggestion for most dangerous matchup ──────────────────
    if danger_matchups:
        st.markdown("---")
        top_danger = danger_matchups[0]
        st.markdown(f"### 📐 Field Plan: {top_danger['batter']} vs {top_danger['bowler']}")

        # Find the actual player dicts
        danger_batter = next((b for b in batters if b["name"] == top_danger["batter"]), batters[0])
        danger_bowler = next((b for b in bowlers if b["name"] == top_danger["bowler"]), bowlers[0])
        hints = field_placement_hints(danger_batter, danger_bowler, ms.phase)

        cols = st.columns(len(hints))
        for col, hint in zip(cols, hints):
            with col:
                st.markdown(
                    strategy_card("FIELD", "info", hint),
                    unsafe_allow_html=True,
                )