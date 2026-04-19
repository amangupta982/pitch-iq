"""
pages/batting_order.py
──────────────────────
Who should bat next — ranked recommendation list.

Available batters = Playing 11 MINUS dismissed (auto from scorecard).
No manual checkboxes needed.

Displays:
    • "SEND IN NOW" hero card for top pick
    • Ranked list with player cards + rationale
    • Form + SR comparison bar chart (Plotly)
    • Tail-ender warning if applicable
"""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from core.engine import batting_order_recommendation
from core.state import get_batting_team_players
from components.cards import send_now_card, player_card, analysis_card


def render() -> None:
    """Render the Batting Order page."""
    ms = st.session_state.get("match_state")
    if not ms:
        st.info("🏏 Select a match from the sidebar to begin.")
        return

    st.markdown(
        f'<h2 style="margin-bottom:0.1rem;">🏏 Batting Order</h2>'
        f'<p style="color:#6b7280;font-size:0.85rem;margin-top:0;">'
        f'{ms.batting_team.get("short", "")} · {ms.runs}/{ms.wickets} after {ms.overs} overs'
        f' · {ms.phase.upper()} phase</p>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ── Get available batters (not dismissed, not currently at crease batting) ─
    batting_players = get_batting_team_players()
    scorecard = st.session_state.get("scorecard", [])
    latest = scorecard[-1] if scorecard else {}

    # Find who is dismissed
    dismissed_names = set()
    at_crease_names = set()
    for b in latest.get("batters", []):
        if b.get("dismissed", False):
            dismissed_names.add(b["name"].lower())
        else:
            at_crease_names.add(b["name"].lower())

    # Available = Playing 11 batters who are NOT dismissed and NOT at crease
    available = []
    for p in batting_players:
        name_low = p["name"].lower()
        if name_low not in dismissed_names and name_low not in at_crease_names:
            available.append(p)

    if not available:
        st.warning("⚠️ No available batters remaining. All players have batted or are at the crease.")
        return

    # ── Get recommendations ──────────────────────────────────────────
    recommendations = batting_order_recommendation(ms, available)

    if not recommendations:
        st.info("No recommendations available.")
        return

    # ── Tail-ender warning ───────────────────────────────────────────
    if ms.wickets >= 7:
        st.markdown(
            analysis_card(
                "⚠️ <strong>Tail exposed!</strong> With "
                f"{10 - ms.wickets} wickets in hand, prioritize partnerships over strike rate. "
                "Send in someone who can rotate strike and protect the tail."
            ),
            unsafe_allow_html=True,
        )

    # ── Top pick: SEND IN NOW ────────────────────────────────────────
    top = recommendations[0]
    st.markdown(
        send_now_card(
            {"name": top["name"], "role": top["role"], "profile": top["profile"]},
            top["rationale"],
        ),
        unsafe_allow_html=True,
    )

    # ── Charts ───────────────────────────────────────────────────────
    st.markdown("### 📊 Comparison")
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        _render_form_chart(recommendations[:6])

    with col_chart2:
        _render_sr_chart(recommendations[:6], ms.phase)

    # ── Ranked list ──────────────────────────────────────────────────
    st.markdown("### 📋 Full Rankings")
    for i, rec in enumerate(recommendations):
        rank = i + 1
        highlight = (i == 0)
        st.markdown(
            player_card(
                {"name": rec["name"], "role": rec["role"], "profile": rec["profile"]},
                rank=rank,
                highlight=highlight,
            ),
            unsafe_allow_html=True,
        )
        # Show rationale
        st.markdown(
            f'<div style="color:#6b7280;font-size:0.8rem;margin:-0.5rem 0 0.8rem 2.5rem;">'
            f'💬 {rec["rationale"]} · Score: <strong>{rec["score"]}</strong></div>',
            unsafe_allow_html=True,
        )


def _render_form_chart(recs: list[dict]) -> None:
    """
    Render a horizontal bar chart of player form scores.

    Parameters
    ----------
    recs : list[dict]   top recommendations
    """
    names = [r["name"].split()[-1] for r in recs]  # last name for brevity
    forms = [r["profile"].get("form", 0) for r in recs]
    colors = ["#22c55e" if f > 75 else "#f59e0b" if f > 50 else "#ef4444" for f in forms]

    fig = go.Figure(go.Bar(
        x=forms,
        y=names,
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{f}" for f in forms],
        textposition="auto",
        textfont=dict(color="#fff", size=12),
    ))

    fig.update_layout(
        title=dict(text="Current Form", font=dict(size=14, color="#d1d5db")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#111827",
        font=dict(color="#9ca3af", family="Inter"),
        height=250,
        margin=dict(l=80, r=20, t=40, b=20),
        xaxis=dict(range=[0, 100], gridcolor="#1f2937", title=""),
        yaxis=dict(autorange="reversed", gridcolor="#1f2937"),
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)


def _render_sr_chart(recs: list[dict], phase: str) -> None:
    """
    Render a bar chart comparing relevant SR for the current phase.

    Parameters
    ----------
    recs  : list[dict]
    phase : str   "powerplay" | "middle" | "death"
    """
    sr_key = {
        "powerplay": "powerplay_sr",
        "middle": "sr",
        "death": "death_sr",
    }.get(phase, "sr")

    sr_label = {
        "powerplay": "Powerplay SR",
        "middle": "Overall SR",
        "death": "Death SR",
    }.get(phase, "SR")

    names = [r["name"].split()[-1] for r in recs]
    srs = [r["profile"].get(sr_key, 130) for r in recs]

    fig = go.Figure(go.Bar(
        x=srs,
        y=names,
        orientation="h",
        marker=dict(
            color=srs,
            colorscale=[[0, "#3b82f6"], [0.5, "#8b5cf6"], [1, "#ef4444"]],
            line=dict(width=0),
        ),
        text=[f"{s}" for s in srs],
        textposition="auto",
        textfont=dict(color="#fff", size=12),
    ))

    fig.update_layout(
        title=dict(text=sr_label, font=dict(size=14, color="#d1d5db")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#111827",
        font=dict(color="#9ca3af", family="Inter"),
        height=250,
        margin=dict(l=80, r=20, t=40, b=20),
        xaxis=dict(gridcolor="#1f2937", title=""),
        yaxis=dict(autorange="reversed", gridcolor="#1f2937"),
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)
