"""
components/cards.py
───────────────────
Reusable HTML card components for PitchIQ.

Each function returns an HTML string meant to be rendered via
st.markdown(..., unsafe_allow_html=True).

All cards use emoji only for icons — no Material Icons or external
icon fonts.
"""

from __future__ import annotations


def metric_card(label: str, value: str, sub: str = "") -> str:
    """
    Render a metric tile (e.g. Runs, Wickets, CRR).

    Parameters
    ----------
    label : str   uppercase heading
    value : str   main big number
    sub   : str   optional subtitle

    Returns
    -------
    str   HTML string.
    """
    sub_html = f'<div class="metric-sub">{sub}</div>' if sub else ""
    return f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {sub_html}
    </div>
    """


def player_card(
    player: dict,
    rank: int = 0,
    highlight: bool = False,
) -> str:
    """
    Render a player info card with stats.

    Parameters
    ----------
    player    : dict   player dict with 'profile' sub-dict
    rank      : int    ranking (0 = no rank)
    highlight : bool   green border highlight

    Returns
    -------
    str   HTML string.
    """
    prof = player.get("profile", {})
    name = player.get("name", "Unknown")
    role = player.get("role", prof.get("role", "bat"))
    avg = prof.get("avg", "-")
    sr = prof.get("sr", "-")
    death_sr = prof.get("death_sr", "-")
    form = prof.get("form", 0)
    vs_pace = prof.get("vs_pace", "-")
    vs_spin = prof.get("vs_spin", "-")

    hl_class = "highlight" if highlight else ""
    rank_html = f'<span style="color:#6b7280;font-size:0.8rem;font-weight:600;">#{rank}</span> ' if rank else ""

    role_labels = {"bat": "BATTER", "bowl": "BOWLER", "allrounder": "ALL-ROUNDER", "wk-bat": "WK-BATTER"}
    role_label = role_labels.get(role, role.upper())

    form_color = "#22c55e" if form > 75 else "#f59e0b" if form > 50 else "#ef4444"

    return f"""
    <div class="player-card {hl_class}">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <span class="player-role">{role_label}</span>
                <div class="player-name">{rank_html}{name}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:0.75rem;color:#6b7280;">FORM</div>
                <div style="font-size:1.3rem;font-weight:800;color:{form_color};">{form}</div>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr 1fr;gap:0.5rem;margin-top:0.7rem;">
            <div class="player-stat"><strong>{avg}</strong><br><span style="font-size:0.65rem;color:#6b7280;">AVG</span></div>
            <div class="player-stat"><strong>{sr}</strong><br><span style="font-size:0.65rem;color:#6b7280;">SR</span></div>
            <div class="player-stat"><strong>{death_sr}</strong><br><span style="font-size:0.65rem;color:#6b7280;">DEATH SR</span></div>
            <div class="player-stat"><strong>{vs_pace}</strong><br><span style="font-size:0.65rem;color:#6b7280;">vs PACE</span></div>
            <div class="player-stat"><strong>{vs_spin}</strong><br><span style="font-size:0.65rem;color:#6b7280;">vs SPIN</span></div>
        </div>
        <div class="form-bar"><div class="form-fill" style="width:{form}%;"></div></div>
    </div>
    """


def send_now_card(player: dict, rationale: str = "") -> str:
    """
    Render the "SEND IN NOW" hero card.

    Dark background with green left border — text remains readable.

    Parameters
    ----------
    player    : dict
    rationale : str

    Returns
    -------
    str   HTML string.
    """
    prof = player.get("profile", player)
    name = player.get("name", prof.get("name", "Unknown"))
    sr = prof.get("sr", "-")
    form = prof.get("form", "-")
    role = player.get("role", prof.get("role", "bat"))
    role_labels = {"bat": "BATTER", "bowl": "BOWLER", "allrounder": "ALL-ROUNDER", "wk-bat": "WK-BATTER"}

    return f"""
    <div class="send-now-card">
        <div class="send-tag">⚡ SEND IN NOW</div>
        <div class="player-name">{name}</div>
        <div style="color:rgba(255,255,255,0.7);font-size:0.8rem;margin-top:0.2rem;">
            {role_labels.get(role, role.upper())} · SR {sr} · Form {form}/100
        </div>
        <div style="color:rgba(255,255,255,0.85);font-size:0.85rem;margin-top:0.6rem;line-height:1.5;">
            {rationale}
        </div>
    </div>
    """


def strategy_card(tag: str, tag_type: str, text: str) -> str:
    """
    Render a strategy insight card with a colored tag.

    Parameters
    ----------
    tag      : str   e.g. "DANGER", "ADVANTAGE"
    tag_type : str   "danger" | "warning" | "success" | "info"
    text     : str   body text

    Returns
    -------
    str   HTML string.
    """
    return f"""
    <div class="pitchiq-card">
        <span class="strategy-tag {tag_type}">{tag}</span>
        <div style="margin-top:0.5rem;color:#d1d5db;font-size:0.9rem;line-height:1.5;">
            {text}
        </div>
    </div>
    """


def analysis_card(text: str) -> str:
    """
    Render a plain-English analysis box.

    Parameters
    ----------
    text : str   analysis paragraph

    Returns
    -------
    str   HTML string.
    """
    return f'<div class="analysis-box">💡 {text}</div>'


def over_plan_card(
    over: int,
    phase: str,
    bowler: str,
    line: str,
    reasoning: str,
    overs_used: float = 0.0,
) -> str:
    """
    Render a single over-plan row.

    Parameters
    ----------
    over      : int    over number
    phase     : str    "powerplay" | "middle" | "death"
    bowler    : str    bowler name
    line      : str    line & length suggestion
    reasoning : str    reason text
    overs_used: float  how many overs already bowled

    Returns
    -------
    str   HTML string.
    """
    phase_class = f"phase-{phase}"
    quota_pct = min(100, (overs_used / 4.0) * 100)
    quota_color = "#22c55e" if overs_used < 3 else "#f59e0b" if overs_used < 4 else "#ef4444"

    return f"""
    <div class="over-plan-card">
        <div class="over-number">{over}</div>
        <div style="flex:1;">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.2rem;">
                <span style="font-weight:700;color:#f0f4ff;">{bowler}</span>
                <span class="phase-badge {phase_class}">{phase}</span>
            </div>
            <div style="color:#9ca3af;font-size:0.8rem;">📍 {line}</div>
            <div style="color:#6b7280;font-size:0.75rem;margin-top:0.1rem;">{reasoning}</div>
            <div class="quota-bar"><div class="quota-fill" style="width:{quota_pct}%;background:{quota_color};"></div></div>
        </div>
    </div>
    """


def bench_player_card(
    player: dict,
    score: float,
    reason: str,
    timing: str,
    is_top: bool = False,
) -> str:
    """
    Render a bench player (Impact Sub candidate) card.

    TOP PICK uses dark background with green left border for readability.

    Parameters
    ----------
    player : dict
    score  : float   impact score
    reason : str     why this player helps
    timing : str     when to bring in
    is_top : bool    True = green-bordered hero card

    Returns
    -------
    str   HTML string.
    """
    prof = player.get("profile", player)
    name = player.get("name", prof.get("name", "Unknown"))
    role = player.get("role", prof.get("role", "bat"))
    role_labels = {"bat": "BATTER", "bowl": "BOWLER", "allrounder": "ALL-ROUNDER", "wk-bat": "WK-BATTER"}
    role_label = role_labels.get(role, role.upper())

    card_class = "bench-card top-pick" if is_top else "bench-card"
    name_color = "#f0f4ff"
    score_color = "#22c55e" if score > 40 else "#f59e0b" if score > 20 else "#9ca3af"
    role_color = "#3b82f6"

    top_tag = '<div class="send-tag" style="background:#22c55e;color:#000;margin-bottom:0.5rem;">⭐ TOP PICK</div>' if is_top else ""

    return f"""<div class="{card_class}">{top_tag}<div style="display:flex;justify-content:space-between;align-items:start;"><div><span style="font-size:0.7rem;color:{role_color};text-transform:uppercase;letter-spacing:1px;font-weight:600;">{role_label}</span><div style="font-size:1.1rem;font-weight:700;color:{name_color};">{name}</div></div><div style="text-align:right;"><div style="font-size:0.65rem;color:#6b7280;">IMPACT</div><div style="font-size:1.5rem;font-weight:800;color:{score_color};">{score:.0f}</div></div></div><div style="color:#9ca3af;font-size:0.85rem;margin-top:0.5rem;">{reason}</div><div class="bench-timing">🕐 {timing}</div></div>"""


def ball_viz(balls: list[str]) -> str:
    """
    Render a last-6-balls visualization row.

    Parameters
    ----------
    balls : list[str]   e.g. ["0", "1", "4", "W", "2", "6"]

    Returns
    -------
    str   HTML string.
    """
    html_parts = []
    for b in balls:
        css_class = f"ball-{b}" if b in ("0", "1", "2", "3", "4", "6", "W") else "ball-1"
        html_parts.append(f'<span class="ball-dot {css_class}">{b}</span>')
    return f'<div style="display:flex;gap:4px;margin:0.5rem 0;">{"".join(html_parts)}</div>'


def win_probability_bar(
    bat_team: dict,
    bowl_team: dict,
    bat_prob: float,
    bowl_prob: float,
) -> str:
    """
    Render a horizontal win-probability bar with team colors.

    Parameters
    ----------
    bat_team  : dict   {short, color}
    bowl_team : dict   {short, color}
    bat_prob  : float  0.0-1.0
    bowl_prob : float  0.0-1.0

    Returns
    -------
    str   HTML string.
    """
    bat_pct = max(5, int(bat_prob * 100))
    bowl_pct = max(5, int(bowl_prob * 100))
    bat_color = bat_team.get("color", "#3b82f6")
    bowl_color = bowl_team.get("color", "#ef4444")
    bat_short = bat_team.get("short", "BAT")
    bowl_short = bowl_team.get("short", "BOWL")

    return f"""
    <div style="margin:0.8rem 0;">
        <div style="display:flex;justify-content:space-between;margin-bottom:0.3rem;">
            <span style="color:{bat_color};font-weight:700;font-size:0.85rem;">{bat_short} {bat_pct}%</span>
            <span style="color:{bowl_color};font-weight:700;font-size:0.85rem;">{bowl_short} {bowl_pct}%</span>
        </div>
        <div class="win-bar-container">
            <div class="win-bar-segment" style="width:{bat_pct}%;background:{bat_color};">{bat_pct}%</div>
            <div class="win-bar-segment" style="width:{bowl_pct}%;background:{bowl_color};">{bowl_pct}%</div>
        </div>
    </div>
    """
