"""components/styles.py — PitchIQ global dark theme."""
import streamlit as st

def inject_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.main{background:#0e1117;}
[data-testid="metric-container"]{background:#1a1f2e;border:1px solid #2d3548;border-radius:12px;padding:14px 18px;}
[data-testid="metric-container"] label{color:#8b95a8!important;font-size:11px!important;font-weight:600!important;text-transform:uppercase;letter-spacing:.06em;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:#f0f4ff!important;font-size:26px!important;font-weight:700!important;}
[data-testid="stSidebar"]{background:#111827;border-right:1px solid #1e2535;}
[data-testid="stSidebar"] label{color:#8b95a8!important;font-size:12px!important;}
.stTabs [data-baseweb="tab-list"]{background:#1a1f2e;border-radius:8px;padding:3px;gap:2px;}
.stTabs [data-baseweb="tab"]{background:transparent;color:#8b95a8;border-radius:6px;font-size:13px;}
.stTabs [aria-selected="true"]{background:#2d3548!important;color:#f0f4ff!important;}
h1,h2,h3{color:#f0f4ff!important;}
p{color:#c8d0e0;}
.section-hdr{font-size:11px;font-weight:600;color:#5a6478;text-transform:uppercase;letter-spacing:.1em;margin:20px 0 10px;padding-bottom:6px;border-bottom:1px solid #1e2535;}
.card{background:#1a1f2e;border:1px solid #2d3548;border-radius:12px;padding:16px 20px;margin-bottom:12px;}
.card-green{border-left:3px solid #4caf7d;}
.card-amber{border-left:3px solid #f59e0b;}
.card-red  {border-left:3px solid #ef4444;}
.badge{display:inline-block;font-size:11px;font-weight:600;padding:3px 10px;border-radius:6px;margin-bottom:8px;text-transform:uppercase;letter-spacing:.05em;}
.badge-ok    {background:#0d2b1a;color:#4caf7d;border:1px solid #1a4a2e;}
.badge-warn  {background:#2b1f0a;color:#e8a94a;border:1px solid #4a3510;}
.badge-danger{background:#2b0d0d;color:#e85555;border:1px solid #4a1515;}
.badge-info  {background:#0d1e35;color:#60a5fa;border:1px solid #1e3a5f;}
.win-bar-outer{height:22px;border-radius:11px;background:#2d3548;overflow:hidden;display:flex;}
.analysis-card{background:#0d1e35;border-left:3px solid #3b82f6;border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:8px;}
.analysis-text{font-size:13px;color:#93c5fd;line-height:1.65;}
.live-dot{width:7px;height:7px;border-radius:50%;background:#e85555;display:inline-block;margin-right:5px;}
</style>""", unsafe_allow_html=True)
