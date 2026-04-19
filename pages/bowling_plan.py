"""
pages/bowling_plan.py
─────────────────────
Over-by-over bowling strategy planner.

Available bowlers = Playing 11 bowlers with < 4 overs bowled
(auto-read from live scorecard).

Displays:
    • Quota tracker per bowler (visual progress bars)
    • Over-by-over plan for next 6 overs
    • Economy rate chart (Plotly bar)
    • Field placement hints for current over
    • Greyed-out bowlers who completed quota
"""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from core.engine import bowling_plan, field_placement_hints
from core.state import get_bowling_team_players, get_batting_team_players
from components.cards import over_plan_card, strategy_card, analysis_card


def render() -> None:
    """Render the Bowling Plan page."""
    ms = st.session_state.get("match_state")
    if not ms:
        st.info("🎯 Select a match from the sidebar to begin.")
        return

    st.markdown(
        f'<h2 style="margin-bottom:0.1rem;">🎯 Bowling Plan</h2>'
        f'<p style="color:#6b7280;font-size:0.85rem;margin-top:0;">'
        f'{ms.bowling_team.get("short", "")} bowling · Over {ms.overs} · {ms.phase.upper()}</p>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ── Get bowlers ──────────────────────────────────────────────────
    bowling_players = get_bowling_team_players()
    batting_players = get_batting_team_players()

    # Filter to bowlers/allrounders
    all_bowlers = [
        p for p in bowling_players
        if p.get("role") in ("bowl", "allrounder")
        or (p.get("profile", {}).get("econ") is not None)
    ]

    available_bowlers = [b for b in all_bowlers if b.get("overs_bowled", 0) < 4.0]
    completed_bowlers = [b for b in all_bowlers if b.get("overs_bowled", 0) >= 4.0]

    # Current batters at crease
    scorecard = st.session_state.get("scorecard", [])
    latest = scorecard[-1] if scorecard else {}
    batters_at_crease = []
    for bat_data in latest.get("batters", []):
        if not bat_data.get("dismissed", True):
            # Find the full player dict
            for bp in batting_players:
                if bp["name"].lower() == bat_data["name"].lower():
                    batters_at_crease.append(bp)
                    break

    # ── Quota Tracker ────────────────────────────────────────────────
    st.markdown("### 📊 Bowling Quota Tracker")
    cols = st.columns(min(4, len(all_bowlers)) if all_bowlers else 1)

    for i, bowler in enumerate(all_bowlers):
        col = cols[i % len(cols)]
        overs = bowler.get("overs_bowled", 0.0)
        pct = min(100, (overs / 4.0) * 100)
        remaining = max(0, 4.0 - overs)
        color = "#22c55e" if overs < 3 else "#f59e0b" if overs < 4 else "#ef4444"
        opacity = "0.4" if overs >= 4 else "1.0"

        with col:
            st.markdown(
                f'<div class="pitchiq-card" style="opacity:{opacity};text-align:center;">'
                f'<div style="font-weight:700;color:#f0f4ff;font-size:0.9rem;">'
                f'{bowler["name"].split()[-1]}</div>'
                f'<div style="font-size:1.5rem;font-weight:800;color:{color};">{overs}</div>'
                f'<div style="font-size:0.7rem;color:#6b7280;">of 4 overs</div>'
                f'<div class="quota-bar" style="margin-top:0.4rem;">'
                f'<div class="quota-fill" style="width:{pct}%;background:{color};"></div></div>'
                f'<div style="font-size:0.7rem;color:#6b7280;margin-top:0.2rem;">'
                f'{remaining:.1f} remaining</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    if completed_bowlers:
        st.markdown(
            f'<div style="color:#6b7280;font-size:0.8rem;margin-top:0.5rem;">'
            f'✅ Quota complete: {", ".join(b["name"] for b in completed_bowlers)}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Over-by-Over Plan ────────────────────────────────────────────
    st.markdown("### 📋 Next 6 Overs Plan")

    if not available_bowlers:
        st.warning("⚠️ No bowlers available — all have completed their quota.")
        return

    plan = bowling_plan(ms, available_bowlers, batters_at_crease)

    if not plan:
        st.info("No bowling plan available.")
        return

    for entry in plan:
        st.markdown(
            over_plan_card(
                over=entry["over"],
                phase=entry["phase"],
                bowler=entry["bowler"],
                line=entry["line"],
                reasoning=entry["reasoning"],
                overs_used=entry.get("overs_used", 0),
            ),
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Economy Rate Chart ───────────────────────────────────────────
    col_econ, col_field = st.columns([3, 2])

    with col_econ:
        st.markdown("### 💰 Economy Rates")
        _render_economy_chart(all_bowlers)

    # ── Field Placement ──────────────────────────────────────────────
    with col_field:
        st.markdown("### 📐 Field Placement")
        if batters_at_crease and plan:
            top_bowler = None
            for p in batting_players:
                if p["name"] == plan[0]["bowler"]:
                    top_bowler = p
                    break
            if not top_bowler:
                top_bowler = available_bowlers[0] if available_bowlers else None

            if top_bowler and batters_at_crease:
                primary_batter = batters_at_crease[0]
                hints = field_placement_hints(primary_batter, top_bowler, ms.phase)
                for hint in hints:
                    st.markdown(
                        strategy_card("FIELD", "info", hint),
                        unsafe_allow_html=True,
                    )
        else:
            st.info("Field suggestions available when batters are at the crease.")


def _render_economy_chart(bowlers: list[dict]) -> None:
    """
    Render a grouped bar chart: overall economy vs death economy.

    Parameters
    ----------
    bowlers : list[dict]
    """
    if not bowlers:
        return

    names = [b["name"].split()[-1] for b in bowlers]
    econ = [b.get("profile", {}).get("econ", 0) or 0 for b in bowlers]
    death_econ = [b.get("profile", {}).get("death_econ", 0) or 0 for b in bowlers]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=names, y=econ,
        name="Overall",
        marker=dict(color="#3b82f6", line=dict(width=0)),
        text=[f"{e:.1f}" for e in econ],
        textposition="auto",
        textfont=dict(color="#fff"),
    ))

    fig.add_trace(go.Bar(
        x=names, y=death_econ,
        name="Death Overs",
        marker=dict(color="#ef4444", line=dict(width=0)),
        text=[f"{e:.1f}" for e in death_econ],
        textposition="auto",
        textfont=dict(color="#fff"),
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#111827",
        font=dict(color="#9ca3af", family="Inter"),
        height=300,
        margin=dict(l=40, r=20, t=10, b=40),
        barmode="group",
        xaxis=dict(gridcolor="#1f2937"),
        yaxis=dict(gridcolor="#1f2937", title="Economy"),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            font=dict(size=11),
        ),
    )

    st.plotly_chart(fig, use_container_width=True)
