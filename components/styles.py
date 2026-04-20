"""
components/styles.py
────────────────────
Global CSS theme injection for PitchIQ dark mode.

Call inject_css() once at the top of app.py to apply the stylesheet.
"""

import streamlit as st


def inject_css() -> None:
    """
    Inject PitchIQ global styles via st.markdown.

    Covers: sidebar, cards, metric tiles, heatmaps, animations,
    navigation buttons, scrollbar, and responsiveness.
    """
    st.markdown("""
    <style>
    /* ── Google Font ─────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    * { font-family: 'Inter', sans-serif !important; }

    /* ── Root variables ──────────────────────────────────────────── */
    :root {
        --bg-primary: #0e1117;
        --bg-secondary: #1a1f2e;
        --bg-card: #151b28;
        --bg-card-hover: #1e2538;
        --border-subtle: #2a3042;
        --text-primary: #f0f4ff;
        --text-secondary: #9ca3af;
        --text-muted: #6b7280;
        --accent-blue: #3b82f6;
        --accent-green: #22c55e;
        --accent-amber: #f59e0b;
        --accent-red: #ef4444;
        --accent-purple: #a855f7;
        --gradient-blue: linear-gradient(135deg, #3b82f6, #6366f1);
        --gradient-green: linear-gradient(135deg, #22c55e, #14b8a6);
        --gradient-red: linear-gradient(135deg, #ef4444, #f97316);
        --gradient-amber: linear-gradient(135deg, #f59e0b, #eab308);
        --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.25);
        --shadow-glow-blue: 0 0 20px rgba(59, 130, 246, 0.15);
        --radius: 12px;
        --radius-sm: 8px;
    }

    /* ── Hide Streamlit defaults ─────────────────────────────────── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* ── Hide stray material-icons text (Streamlit internal) ────── */
    .material-icons,
    .material-symbols-outlined,
    [class*="material-icons"] {
        font-size: 0 !important;
        overflow: hidden !important;
    }

    /* ── Main container ──────────────────────────────────────────── */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* ── Sidebar ─────────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1017 0%, #131926 100%);
        border-right: 1px solid var(--border-subtle);
    }
    section[data-testid="stSidebar"] .stMarkdown h1 {
        font-size: 1.4rem;
        background: var(--gradient-blue);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    /* ── Sidebar nav inactive buttons — subtle border ────────────── */
    section[data-testid="stSidebar"] button[kind="secondary"] {
        border: 0.5px solid #2d3548 !important;
    }
    section[data-testid="stSidebar"] button[kind="secondary"]:hover {
        border-color: var(--accent-blue) !important;
        background: rgba(59,130,246,0.08) !important;
    }

    /* ── Cards ────────────────────────────────────────────────────── */
    .pitchiq-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius);
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.8rem;
        box-shadow: var(--shadow-card);
        transition: all 0.25s ease;
    }
    .pitchiq-card:hover {
        background: var(--bg-card-hover);
        border-color: var(--accent-blue);
        box-shadow: var(--shadow-glow-blue);
        transform: translateY(-1px);
    }

    /* ── Metric Card ─────────────────────────────────────────────── */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius);
        padding: 1rem 1.2rem;
        text-align: center;
        box-shadow: var(--shadow-card);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-glow-blue);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.1;
    }
    .metric-label {
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 0.3rem;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-top: 0.2rem;
    }

    /* ── Player Card ─────────────────────────────────────────────── */
    .player-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius);
        padding: 1.2rem;
        margin-bottom: 0.6rem;
        transition: all 0.3s ease;
    }
    .player-card.highlight {
        border-color: var(--accent-green);
        box-shadow: 0 0 15px rgba(34, 197, 94, 0.2);
    }
    .player-card .player-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    .player-card .player-role {
        font-size: 0.75rem;
        color: var(--accent-blue);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    .player-card .player-stat {
        font-size: 0.85rem;
        color: var(--text-secondary);
    }

    /* ── Send Now Card — dark bg + green left border ─────────────── */
    .send-now-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-left: 4px solid #4caf7d;
        border-radius: var(--radius);
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 0 25px rgba(76, 175, 125, 0.15);
        animation: pulse-glow 2s ease-in-out infinite;
    }
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 15px rgba(76, 175, 125, 0.1); }
        50% { box-shadow: 0 0 30px rgba(76, 175, 125, 0.25); }
    }
    .send-now-card .player-name {
        font-size: 1.4rem;
        font-weight: 800;
        color: #fff;
    }
    .send-now-card .send-tag {
        background: var(--accent-green);
        color: #000;
        font-size: 0.7rem;
        font-weight: 800;
        padding: 0.25rem 0.8rem;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        display: inline-block;
        margin-bottom: 0.5rem;
    }

    /* ── Strategy Tag ────────────────────────────────────────────── */
    .strategy-tag {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-right: 0.4rem;
    }
    .strategy-tag.danger { background: rgba(239,68,68,0.15); color: var(--accent-red); }
    .strategy-tag.warning { background: rgba(245,158,11,0.15); color: var(--accent-amber); }
    .strategy-tag.success { background: rgba(34,197,94,0.15); color: var(--accent-green); }
    .strategy-tag.info { background: rgba(59,130,246,0.15); color: var(--accent-blue); }

    /* ── Analysis Box ────────────────────────────────────────────── */
    .analysis-box {
        background: linear-gradient(135deg, rgba(59,130,246,0.08), rgba(99,102,241,0.05));
        border: 1px solid rgba(59,130,246,0.2);
        border-left: 4px solid var(--accent-blue);
        border-radius: var(--radius-sm);
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* ── Over Plan Card ──────────────────────────────────────────── */
    .over-plan-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-sm);
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.2s ease;
    }
    .over-plan-card:hover {
        background: var(--bg-card-hover);
    }
    .over-number {
        background: var(--gradient-blue);
        color: #fff;
        font-weight: 800;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.85rem;
        flex-shrink: 0;
    }

    /* ── Ball Visualization ──────────────────────────────────────── */
    .ball-dot { display: inline-flex; align-items: center; justify-content: center;
                width: 32px; height: 32px; border-radius: 50%; font-size: 0.75rem;
                font-weight: 700; margin: 0 3px; }
    .ball-0 { background: #374151; color: #9ca3af; }
    .ball-1 { background: #1e3a5f; color: #60a5fa; }
    .ball-2 { background: #1e3a5f; color: #60a5fa; }
    .ball-3 { background: #1e3a5f; color: #60a5fa; }
    .ball-4 { background: #065f46; color: #34d399; }
    .ball-6 { background: #7c2d12; color: #fb923c; }
    .ball-W { background: #7f1d1d; color: #fca5a5; }

    /* ── Phase Badge ─────────────────────────────────────────────── */
    .phase-badge {
        display: inline-block;
        padding: 0.15rem 0.6rem;
        border-radius: 20px;
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .phase-powerplay { background: rgba(59,130,246,0.15); color: #60a5fa; }
    .phase-middle { background: rgba(168,85,247,0.15); color: #c084fc; }
    .phase-death { background: rgba(239,68,68,0.15); color: #fca5a5; }

    /* ── Win-Probability Bar ─────────────────────────────────────── */
    .win-bar-container {
        width: 100%;
        height: 40px;
        background: var(--bg-card);
        border-radius: var(--radius);
        overflow: hidden;
        display: flex;
        border: 1px solid var(--border-subtle);
        margin: 0.5rem 0;
    }
    .win-bar-segment {
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
        font-weight: 700;
        font-size: 0.85rem;
        transition: width 0.6s ease;
    }

    /* ── Progress bar (bowling quota) ────────────────────────────── */
    .quota-bar {
        width: 100%;
        height: 8px;
        background: #1f2937;
        border-radius: 4px;
        overflow: hidden;
        margin-top: 0.3rem;
    }
    .quota-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.4s ease;
    }

    /* ── Form Bar ────────────────────────────────────────────────── */
    .form-bar {
        width: 100%;
        height: 6px;
        background: #1f2937;
        border-radius: 3px;
        overflow: hidden;
        margin-top: 0.2rem;
    }
    .form-fill {
        height: 100%;
        border-radius: 3px;
        background: var(--gradient-green);
    }

    /* ── Bench Player Card — dark bg + green left border ─────────── */
    .bench-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius);
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
    }
    .bench-card.top-pick {
        background: var(--bg-secondary);
        border: 1px solid var(--border-subtle);
        border-left: 4px solid #4caf7d;
        box-shadow: 0 0 20px rgba(76, 175, 125, 0.15);
    }
    .bench-timing {
        background: rgba(59,130,246,0.12);
        color: var(--accent-blue);
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        display: inline-block;
        margin-top: 0.3rem;
    }

    /* ── Scrollbar ───────────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: #374151; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #4b5563; }

    /* ── Nav buttons in sidebar ───────────────────────────────────── */
    .nav-btn {
        display: block;
        width: 100%;
        padding: 0.65rem 1rem;
        margin-bottom: 0.3rem;
        background: transparent;
        border: 1px solid transparent;
        border-radius: var(--radius-sm);
        color: var(--text-secondary);
        font-size: 0.85rem;
        font-weight: 500;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .nav-btn:hover {
        background: rgba(59,130,246,0.08);
        color: var(--text-primary);
        border-color: var(--border-subtle);
    }
    .nav-btn.active {
        background: rgba(59,130,246,0.12);
        border-color: var(--accent-blue);
        color: var(--accent-blue);
        font-weight: 600;
    }

    /* ── Source badge ─────────────────────────────────────────────── */
    .source-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .source-api { background: rgba(34,197,94,0.15); color: var(--accent-green); }
    .source-scraper { background: rgba(245,158,11,0.15); color: var(--accent-amber); }
    .source-mock { background: rgba(59,130,246,0.15); color: var(--accent-blue); }
    .source-manual { background: rgba(168,85,247,0.15); color: var(--accent-purple); }

    /* ── Responsive ──────────────────────────────────────────────── */
    @media (max-width: 768px) {
        .main .block-container { padding-top: 1rem; }
        .metric-value { font-size: 1.4rem; }
    }
    </style>
    """, unsafe_allow_html=True)
