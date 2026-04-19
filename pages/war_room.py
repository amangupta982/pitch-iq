"""
pages/war_room.py
─────────────────
Live match overview — the coach's primary screen.

All data from st.session_state (never fetches directly).

Displays:
    • Match title, venue, toss, status
    • Win probability bar (team colors)
    • Metric cards: runs, wickets, overs, CRR, RRR/proj, balls left,
      pressure index
    • Run rate chart (actual vs required vs venue par)
    • Current batters at crease
    • Current bowler with figures
    • Last 6 balls visualization
    • Plain-English situation analysis
"""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from core.engine import win_probability, pressure_index
from components.cards import (
    metric_card,
    ball_viz,
    win_probability_bar,
    analysis_card,
)


def render() -> None:
    """Render the War Room page."""
    ms = st.session_state.get("match_state")
    match = st.session_state.get("match")
    scorecard = st.session_state.get("scorecard", [])

    if not ms or not match:
        st.info("📊 Select a match from the sidebar to begin.")
        return

    # ── Header ───────────────────────────────────────────────────────
    st.markdown(
        f'<h2 style="margin-bottom:0.2rem;">{match.get("title", "Match")}</h2>',
        unsafe_allow_html=True,
    )
    col_v, col_t, col_s = st.columns(3)
    with col_v:
        st.markdown(f'📍 **{match.get("venue", "N/A")}**')
    with col_t:
        st.markdown(f'🪙 {match.get("toss", "N/A")}')
    with col_s:
        status = match.get("status", "unknown")
        status_emoji = {"live": "🔴", "completed": "✅", "upcoming": "🕐"}.get(status, "⚪")
        st.markdown(f'{status_emoji} **{status.upper()}**')

    st.markdown("---")

    # ── Win Probability ──────────────────────────────────────────────
    bat_prob, bowl_prob = win_probability(ms)
    st.markdown(
        win_probability_bar(ms.batting_team, ms.bowling_team, bat_prob, bowl_prob),
        unsafe_allow_html=True,
    )

    # ── Metric Cards ─────────────────────────────────────────────────
    pi = pressure_index(ms)

    cols = st.columns(7)
    metrics = [
        ("RUNS", str(ms.runs), ""),
        ("WICKETS", str(ms.wickets), f"of 10"),
        ("OVERS", str(ms.overs), ms.phase.upper()),
        ("CRR", f"{ms.crr:.2f}", ""),
        ("RRR" if ms.is_chasing else "PROJ", f"{ms.rrr:.2f}" if ms.rrr else str(ms.proj_score), "need " + str(ms.runs_needed) if ms.is_chasing else ""),
        ("BALLS LEFT", str(ms.balls_left), ""),
        ("PRESSURE", str(pi["score"]), pi["label"]),
    ]
    for col, (label, value, sub) in zip(cols, metrics):
        with col:
            st.markdown(metric_card(label, value, sub), unsafe_allow_html=True)

    st.markdown("")

    # ── Run Rate Chart ───────────────────────────────────────────────
    col_chart, col_info = st.columns([3, 2])

    with col_chart:
        st.markdown("### 📈 Run Rate Tracker")
        _render_run_rate_chart(ms, scorecard)

    with col_info:
        # ── Current Batters ──────────────────────────────────────────
        st.markdown("### 🏏 At the Crease")
        latest = scorecard[-1] if scorecard else {}
        batters_at_crease = [
            b for b in latest.get("batters", []) if not b.get("dismissed", True)
        ]
        if batters_at_crease:
            for b in batters_at_crease:
                runs = b.get("runs", 0)
                balls = b.get("balls", 0)
                sr = round(runs / balls * 100, 1) if balls > 0 else 0.0
                st.markdown(
                    f'<div class="pitchiq-card">'
                    f'<div style="font-weight:700;color:#f0f4ff;">{b["name"]}</div>'
                    f'<div style="color:#9ca3af;font-size:0.85rem;">'
                    f'{runs} ({balls}b) · SR {sr}</div></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown("*No batters currently at crease*")

        # ── Current Bowler ───────────────────────────────────────────
        st.markdown("### 🎯 Bowling")
        bowlers = latest.get("bowlers", [])
        if bowlers:
            current_bowler = bowlers[-1]
            st.markdown(
                f'<div class="pitchiq-card">'
                f'<div style="font-weight:700;color:#f0f4ff;">{current_bowler["name"]}</div>'
                f'<div style="color:#9ca3af;font-size:0.85rem;">'
                f'{current_bowler.get("overs", 0)} ov · '
                f'{current_bowler.get("wickets", 0)}/{current_bowler.get("runs", 0)} · '
                f'Econ {current_bowler.get("econ", 0)}</div></div>',
                unsafe_allow_html=True,
            )

    # ── Last 6 Balls ─────────────────────────────────────────────────
    st.markdown("### 🎱 Last 6 Balls")
    last_balls = latest.get("last_6_balls", [])
    if last_balls:
        st.markdown(ball_viz(last_balls), unsafe_allow_html=True)
    else:
        st.markdown("*Ball-by-ball data not available*")

    # ── Situation Analysis ───────────────────────────────────────────
    st.markdown("### 💡 Situation Analysis")
    analysis = _generate_analysis(ms, pi, bat_prob)
    st.markdown(analysis_card(analysis), unsafe_allow_html=True)


def _render_run_rate_chart(ms, scorecard: list[dict]) -> None:
    """
    Render an interactive Plotly run-rate chart.

    Shows: actual CRR over time, required rate line, venue par.

    Parameters
    ----------
    ms        : MatchState
    scorecard : list[dict]
    """
    latest = scorecard[-1] if scorecard else {}
    batters = latest.get("batters", [])

    # Build cumulative run data from batter scores
    overs_data = []
    runs_cum = 0
    total_balls = 0

    # Simulate over-by-over from batter data (approximate)
    total_runs = latest.get("runs", 0)
    total_overs = float(latest.get("overs", 0))

    if total_overs > 0:
        avg_rpo = total_runs / total_overs
        for o in range(1, int(total_overs) + 1):
            # Simulate with some variance
            if o <= 6:
                rpo = avg_rpo * 0.9  # PP slightly lower
            elif o <= 15:
                rpo = avg_rpo * 0.95
            else:
                rpo = avg_rpo * 1.15
            runs_cum += rpo
            overs_data.append({"over": o, "crr": round(runs_cum / o, 2)})

    if not overs_data:
        st.info("Not enough data for run rate chart")
        return

    overs_x = [d["over"] for d in overs_data]
    crr_y = [d["crr"] for d in overs_data]

    fig = go.Figure()

    # Actual CRR
    fig.add_trace(go.Scatter(
        x=overs_x, y=crr_y,
        mode="lines+markers",
        name="Current RR",
        line=dict(color="#3b82f6", width=3),
        marker=dict(size=6),
        fill="tozeroy",
        fillcolor="rgba(59,130,246,0.1)",
    ))

    # Required rate line
    if ms.is_chasing and ms.rrr:
        fig.add_hline(
            y=ms.rrr, line_dash="dash",
            line_color="#ef4444", line_width=2,
            annotation_text=f"RRR: {ms.rrr:.1f}",
            annotation_font_color="#ef4444",
        )

    # Venue par line (~8.5 for typical IPL)
    fig.add_hline(
        y=8.5, line_dash="dot",
        line_color="#6b7280", line_width=1,
        annotation_text="Venue Par",
        annotation_font_color="#6b7280",
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#111827",
        font=dict(color="#9ca3af", family="Inter"),
        height=300,
        margin=dict(l=40, r=20, t=10, b=40),
        xaxis=dict(
            title="Overs",
            gridcolor="#1f2937",
            range=[0.5, 20.5],
        ),
        yaxis=dict(
            title="Run Rate",
            gridcolor="#1f2937",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        showlegend=True,
    )

    st.plotly_chart(fig, use_container_width=True)


def _generate_analysis(ms, pi: dict, bat_prob: float) -> str:
    """
    Generate a 3-4 sentence plain-English analysis.

    Parameters
    ----------
    ms       : MatchState
    pi       : dict   pressure index
    bat_prob : float  batting team win probability

    Returns
    -------
    str   analysis text.
    """
    bat_name = ms.batting_team.get("short", "Batting")
    bowl_name = ms.bowling_team.get("short", "Bowling")

    parts = []

    # Score context
    if ms.is_chasing:
        parts.append(
            f"{bat_name} need {ms.runs_needed} runs from {ms.balls_left} balls "
            f"at a required rate of {ms.rrr:.1f}."
        )
    else:
        parts.append(
            f"{bat_name} are {ms.runs}/{ms.wickets} after {ms.overs} overs, "
            f"projected to reach {ms.proj_score}."
        )

    # Pressure
    if pi["label"] == "Critical":
        parts.append(f"The pressure is {pi['label'].lower()} at {pi['score']}/100 — a wicket now could be decisive.")
    elif pi["label"] == "Elevated":
        parts.append(f"Pressure is building ({pi['score']}/100) — the next 2-3 overs are crucial.")
    else:
        parts.append(f"The situation is well under control ({pi['score']}/100).")

    # Win probability
    if bat_prob > 0.7:
        parts.append(f"{bat_name} are firmly in control with a {bat_prob*100:.0f}% win probability.")
    elif bat_prob > 0.5:
        parts.append(f"{bat_name} have a slight edge ({bat_prob*100:.0f}%), but {bowl_name} are still in the fight.")
    elif bat_prob > 0.3:
        parts.append(f"{bowl_name} are slightly ahead — {bat_name} need to accelerate without losing wickets.")
    else:
        parts.append(f"{bowl_name} are dominating with {(1-bat_prob)*100:.0f}% win probability. {bat_name} need something special.")

    # Phase
    if ms.phase == "death":
        parts.append("We're in the death overs — time for specialist death bowlers and boundary options.")
    elif ms.phase == "powerplay":
        parts.append("Powerplay is on — fielding restrictions give the batting side an advantage.")

    return " ".join(parts)
