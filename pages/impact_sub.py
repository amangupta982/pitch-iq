"""
pages/impact_sub.py
───────────────────
Impact Substitution recommender.

Bench = Playing 15 MINUS Playing 11 (auto-detected).
Shows exactly who is on the bench (usually 4 players) and recommends
the best one to bring in, with timing.

Displays:
    • Bench player roster
    • Top recommendation card (green, large)
    • Alternatives (2nd and 3rd best)
    • Impact score bar chart
"""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from core.engine import impact_sub_recommendation
from core.state import get_bench_players
from components.cards import bench_player_card, analysis_card


def render() -> None:
    """Render the Impact Sub page."""
    ms = st.session_state.get("match_state")
    if not ms:
        st.info("🔀 Select a match from the sidebar to begin.")
        return

    st.markdown(
        f'<h2 style="margin-bottom:0.1rem;">🔀 Impact Substitution</h2>'
        f'<p style="color:#6b7280;font-size:0.85rem;margin-top:0;">'
        f'Bench options for {ms.batting_team.get("short", "")} · '
        f'{ms.runs}/{ms.wickets} · Over {ms.overs} · {ms.phase.upper()}</p>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ── Get bench players ────────────────────────────────────────────
    bench_batting = get_bench_players("batting")
    bench_bowling = get_bench_players("bowling")

    # Show context
    col_bat, col_bowl = st.columns(2)
    with col_bat:
        st.markdown(
            f'<div class="pitchiq-card">'
            f'<div style="font-size:0.75rem;color:#6b7280;text-transform:uppercase;'
            f'letter-spacing:1px;">Batting Team Bench</div>'
            f'<div style="font-size:1.8rem;font-weight:800;color:#f0f4ff;">'
            f'{len(bench_batting)} players</div>'
            f'<div style="color:#9ca3af;font-size:0.8rem;">'
            f'{ms.batting_team.get("name", "")}</div></div>',
            unsafe_allow_html=True,
        )
    with col_bowl:
        st.markdown(
            f'<div class="pitchiq-card">'
            f'<div style="font-size:0.75rem;color:#6b7280;text-transform:uppercase;'
            f'letter-spacing:1px;">Bowling Team Bench</div>'
            f'<div style="font-size:1.8rem;font-weight:800;color:#f0f4ff;">'
            f'{len(bench_bowling)} players</div>'
            f'<div style="color:#9ca3af;font-size:0.8rem;">'
            f'{ms.bowling_team.get("name", "")}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Batting team bench analysis ──────────────────────────────────
    st.markdown(f"### 🏏 {ms.batting_team.get('short', 'Batting')} — Bench Analysis")

    if not bench_batting:
        st.info("No bench players detected for batting team.")
    else:
        recs_bat = impact_sub_recommendation(ms, bench_batting)
        _render_bench_section(recs_bat, "batting")

    st.markdown("---")

    # ── Bowling team bench analysis ──────────────────────────────────
    st.markdown(f"### 🎯 {ms.bowling_team.get('short', 'Bowling')} — Bench Analysis")

    if not bench_bowling:
        st.info("No bench players detected for bowling team.")
    else:
        recs_bowl = impact_sub_recommendation(ms, bench_bowling)
        _render_bench_section(recs_bowl, "bowling")


def _render_bench_section(recs: list[dict], team_type: str) -> None:
    """
    Render bench player recommendation section.

    Parameters
    ----------
    recs      : list[dict]   ranked bench recommendations
    team_type : str          "batting" or "bowling"
    """
    ms = st.session_state.get("match_state")

    if not recs:
        st.info("No recommendations available.")
        return

    # ── Situation Summary ────────────────────────────────────────────
    if ms:
        if ms.is_chasing and ms.rrr and ms.rrr > 10:
            st.markdown(
                analysis_card(
                    f"High required rate ({ms.rrr:.1f}) — prioritize aggressive batting options. "
                    f"An Impact Sub batter could accelerate the chase immediately."
                ),
                unsafe_allow_html=True,
            )
        elif ms.wickets >= 5:
            st.markdown(
                analysis_card(
                    f"With {ms.wickets} wickets down, batting reinforcement is critical. "
                    f"Consider bringing in a reliable middle-order option."
                ),
                unsafe_allow_html=True,
            )
        elif ms.phase == "death" and not ms.is_chasing:
            st.markdown(
                analysis_card(
                    "Death overs approaching while defending — a death-bowling specialist "
                    "from the bench could be decisive."
                ),
                unsafe_allow_html=True,
            )

    # ── Top Pick ─────────────────────────────────────────────────────
    top = recs[0]
    st.markdown(
        bench_player_card(
            player={"name": top["name"], "role": top["role"], "profile": top["profile"]},
            score=top["score"],
            reason=top["reason"],
            timing=top["timing"],
            is_top=True,
        ),
        unsafe_allow_html=True,
    )

    # ── Alternatives ─────────────────────────────────────────────────
    if len(recs) > 1:
        st.markdown("#### Alternatives")
        alt_cols = st.columns(min(3, len(recs) - 1))
        for i, rec in enumerate(recs[1:4]):
            with alt_cols[i % len(alt_cols)]:
                st.markdown(
                    bench_player_card(
                        player={"name": rec["name"], "role": rec["role"], "profile": rec["profile"]},
                        score=rec["score"],
                        reason=rec["reason"],
                        timing=rec["timing"],
                        is_top=False,
                    ),
                    unsafe_allow_html=True,
                )

    # ── Impact Score Chart ───────────────────────────────────────────
    st.markdown("#### 📊 Impact Scores")
    _render_impact_chart(recs)


def _render_impact_chart(recs: list[dict]) -> None:
    """
    Render a bar chart of impact scores for all bench players.

    Parameters
    ----------
    recs : list[dict]
    """
    names = [r["name"].split()[-1] for r in recs]
    scores = [r["score"] for r in recs]
    colors = ["#22c55e" if i == 0 else "#3b82f6" for i in range(len(recs))]

    fig = go.Figure(go.Bar(
        x=names,
        y=scores,
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{s:.0f}" for s in scores],
        textposition="auto",
        textfont=dict(color="#fff", size=13, family="Inter"),
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#111827",
        font=dict(color="#9ca3af", family="Inter"),
        height=250,
        margin=dict(l=40, r=20, t=10, b=40),
        xaxis=dict(gridcolor="#1f2937"),
        yaxis=dict(gridcolor="#1f2937", title="Impact Score"),
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)
