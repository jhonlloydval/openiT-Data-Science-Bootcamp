"""
styles.py — Global theme, CSS, and UI component helpers.
Edit COLORS to change the entire app palette.
"""

import streamlit as st

COLORS = {
    "bg":        "#07091a",
    "surface1":  "#0c1023",
    "surface2":  "#111829",
    "surface3":  "#172036",
    "border":    "#1c2b45",
    "accent":    "#38bdf8",
    "amber":     "#f59e0b",
    "green":     "#22d3a0",
    "red":       "#f87171",
    "orange":    "#fb923c",
    "text":      "#e2e8f0",
    "muted":     "#64748b",
    "dim":       "#94a3b8",
}

RISK_COLORS = {
    "Low":      COLORS["green"],
    "Moderate": COLORS["amber"],
    "High":     COLORS["orange"],
    "Critical": COLORS["red"],
    "—":        COLORS["muted"],
}


def apply_styles():
    c = COLORS
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Hide Streamlit chrome ───────────────────────────────────── */
    #MainMenu, footer, header                    {{ visibility: hidden !important; }}
    [data-testid="stDecoration"]                 {{ display: none !important; }}
    [data-testid="stPageTitle"]                  {{ display: none !important; }}
    [data-testid="stSidebarNav"]                 {{ display: none !important; }}
    .stDeployButton                              {{ display: none !important; }}
    [data-testid="collapsedControl"]             {{ display: none !important; }}
    .block-container                             {{ padding-top: 1.8rem !important; padding-bottom: 2rem !important; }}

    /* ── Root ────────────────────────────────────────────────────── */
    :root {{
        --bg: {c['bg']}; --s1: {c['surface1']}; --s2: {c['surface2']}; --s3: {c['surface3']};
        --border: {c['border']}; --accent: {c['accent']}; --amber: {c['amber']};
        --green: {c['green']}; --red: {c['red']}; --orange: {c['orange']};
        --text: {c['text']}; --muted: {c['muted']}; --dim: {c['dim']};
        --font: 'Outfit', sans-serif; --mono: 'JetBrains Mono', monospace;
    }}

    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {{
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: var(--font) !important;
    }}

    /* ── Sidebar ─────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {{
        background-color: var(--s1) !important;
        border-right: 1px solid var(--border) !important;
    }}
    [data-testid="stSidebar"] * {{ color: var(--text) !important; font-family: var(--font) !important; }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{ color: var(--muted) !important; font-size: 12px; }}

    .gw-logo {{ font-size: 26px; font-weight: 800; letter-spacing: -1.5px; color: var(--text) !important; font-family: var(--font); line-height: 1; margin-top: 4px; }}
    .gw-logo span {{ color: var(--accent) !important; }}
    .gw-tagline {{ font-size: 10px; color: var(--muted) !important; text-transform: uppercase; letter-spacing: .18em; margin-top: 4px; margin-bottom: 2px; }}
    .gw-divider {{ height: 1px; background: var(--border); margin: 14px 0; }}
    .sidebar-label {{ font-size: 11px !important; color: var(--muted) !important; text-transform: uppercase; letter-spacing: .1em; margin-bottom: 4px; font-weight: 500; }}
    .sidebar-empty {{ font-size: 12px; color: var(--muted); background: var(--s2); border: 1px solid var(--border); border-radius: 8px; padding: 10px 12px; line-height: 1.5; }}

    /* ── Page header ─────────────────────────────────────────────── */
    .gw-page-title {{ font-size: 24px; font-weight: 800; letter-spacing: -.8px; color: var(--text); margin-bottom: 2px; }}
    .gw-page-sub   {{ font-size: 13px; color: var(--muted); margin-bottom: 20px; }}

    /* ── Cards ───────────────────────────────────────────────────── */
    .gw-card {{ background: var(--s2); border: 1px solid var(--border); border-radius: 12px; padding: 16px 18px; margin-bottom: 10px; }}
    .gw-card-label {{ font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: .1em; margin-bottom: 5px; }}
    .gw-card-value {{ font-size: 28px; font-weight: 700; font-family: var(--mono); letter-spacing: -1px; line-height: 1; }}
    .gw-card-sub   {{ font-size: 11px; color: var(--dim); margin-top: 5px; }}

    /* ── Badge ───────────────────────────────────────────────────── */
    .badge {{ display: inline-block; padding: 2px 9px; border-radius: 5px; font-size: 11px; font-weight: 600; }}
    .badge-low      {{ background: #0d2e2644; color: {c['green']};  border: 1px solid {c['green']}44; }}
    .badge-moderate {{ background: #2a1f0a44; color: {c['amber']};  border: 1px solid {c['amber']}44; }}
    .badge-high     {{ background: #2a160844; color: {c['orange']}; border: 1px solid {c['orange']}44; }}
    .badge-critical {{ background: #2a0d0d44; color: {c['red']};    border: 1px solid {c['red']}44; }}

    /* ── Grade Entry table rows ───────────────────────────────────── */
    .ge-table-header {{
        display: grid; grid-template-columns: 3fr 1fr 1fr 1fr 0.5fr;
        gap: 8px; padding: 6px 10px; margin-bottom: 2px;
        font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: .08em;
    }}
    .ge-row {{
        display: grid; grid-template-columns: 3fr 1fr 1fr 1fr 0.5fr;
        gap: 8px; padding: 8px 10px; background: var(--s3);
        border: 1px solid var(--border); border-radius: 7px; margin-bottom: 4px;
        align-items: center; font-size: 13px;
    }}
    .ge-row-name {{ font-weight: 500; color: var(--text); }}
    .ge-row-num  {{ font-family: var(--mono); color: var(--dim); }}
    .ge-row-pct  {{ font-family: var(--mono); font-weight: 600; }}
    .ge-category-grade {{
        display: flex; align-items: center; gap: 10px;
        background: var(--s2); border-radius: 7px;
        padding: 8px 12px; margin: 8px 0 4px;
        font-size: 12px; color: var(--muted);
    }}
    .ge-category-grade b {{ font-family: var(--mono); font-size: 15px; }}

    /* ── Chat bubbles ─────────────────────────────────────────────── */
    .chat-user {{ text-align: right; margin-bottom: 10px; }}
    .chat-user span {{
        display: inline-block; background: var(--accent); color: var(--bg);
        border-radius: 14px 14px 4px 14px; padding: 9px 14px;
        font-size: 14px; max-width: 80%; line-height: 1.5;
    }}
    .chat-ai {{ text-align: left; margin-bottom: 10px; }}
    .chat-ai-label {{ font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: .1em; margin-bottom: 4px; }}
    .chat-ai-inner {{
        display: inline-block; background: var(--s2); border: 1px solid var(--border);
        border-radius: 4px 14px 14px 14px; padding: 10px 14px;
        font-size: 14px; max-width: 85%; line-height: 1.6; white-space: pre-wrap;
    }}

    /* ── Inputs ───────────────────────────────────────────────────── */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] div[data-baseweb],
    [data-testid="stTextArea"] textarea {{
        background-color: var(--s3) !important; border: 1px solid var(--border) !important;
        color: var(--text) !important; font-family: var(--font) !important; border-radius: 7px !important;
    }}
    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus {{
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px {c['accent']}22 !important;
    }}

    /* ── Buttons ──────────────────────────────────────────────────── */
    .stButton > button {{
        background: var(--s3) !important; color: var(--dim) !important;
        border: 1px solid var(--border) !important; border-radius: 7px !important;
        font-family: var(--font) !important; font-weight: 500 !important; transition: all .15s;
    }}
    .stButton > button:hover {{
        border-color: var(--accent) !important; color: var(--accent) !important;
        background: var(--s2) !important;
    }}
    .stFormSubmitButton > button {{
        background: var(--s3) !important; border: 1px solid var(--border) !important;
        color: var(--dim) !important; border-radius: 7px !important; font-family: var(--font) !important;
    }}
    .stFormSubmitButton > button:hover {{
        border-color: var(--accent) !important; color: var(--accent) !important;
    }}

    /* ── st.metric ───────────────────────────────────────────────── */
    [data-testid="stMetric"] {{
        background: var(--s2); border: 1px solid var(--border);
        border-radius: 12px; padding: 14px 16px !important;
    }}
    [data-testid="stMetricLabel"] {{ font-size: 10px !important; text-transform: uppercase; letter-spacing: .08em; color: var(--muted) !important; }}
    [data-testid="stMetricValue"] {{ font-family: var(--mono) !important; font-size: 26px !important; font-weight: 700 !important; }}
    [data-testid="stMetricDelta"] {{ font-size: 11px !important; }}

    /* ── Tabs ────────────────────────────────────────────────────── */
    [data-testid="stTabs"] [data-baseweb="tab"] {{ background: transparent !important; color: var(--muted) !important; font-family: var(--font) !important; font-size: 14px; }}
    [data-testid="stTabs"] [aria-selected="true"]  {{ color: var(--accent) !important; border-bottom-color: var(--accent) !important; }}
    [data-testid="stTabs"] [data-baseweb="tab-panel"] {{ background: transparent !important; }}

    /* ── Expander ────────────────────────────────────────────────── */
    [data-testid="stExpander"] {{ background: var(--s2) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; }}
    [data-testid="stExpander"] summary {{ background: transparent !important; color: var(--text) !important; font-family: var(--font) !important; font-weight: 600; }}
    [data-testid="stExpander"] summary:hover {{ color: var(--accent) !important; }}

    /* ── Misc ────────────────────────────────────────────────────── */
    hr {{ border-color: var(--border) !important; }}
    h1, h2, h3, h4 {{ color: var(--text) !important; font-family: var(--font) !important; }}
    [data-testid="stMarkdownContainer"] p {{ color: var(--dim) !important; font-size: 13px; }}
    .stProgress > div > div {{ background: var(--s3) !important; border-radius: 99px; }}
    .stProgress > div > div > div {{ border-radius: 99px !important; }}
    [data-testid="stForm"] {{ background: transparent !important; border: none !important; }}
    </style>
    """, unsafe_allow_html=True)


# ── UI Helpers ─────────────────────────────────────────────────────────────────

def page_header(title: str, subtitle: str = ""):
    st.markdown(f'<div class="gw-page-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="gw-page-sub">{subtitle}</div>', unsafe_allow_html=True)


def metric_card(label: str, value: str, sub: str = "", color: str = None):
    col = color or COLORS["text"]
    st.markdown(f"""
    <div class="gw-card">
        <div class="gw-card-label">{label}</div>
        <div class="gw-card-value" style="color:{col}">{value}</div>
        {"<div class='gw-card-sub'>" + sub + "</div>" if sub else ""}
    </div>""", unsafe_allow_html=True)


def risk_badge(level: str) -> str:
    cls = f"badge-{level.lower()}" if level in ("Low","Moderate","High","Critical") else "badge-moderate"
    return f'<span class="badge {cls}">{level}</span>'


def grade_bar(value: float, color: str, height: int = 6) -> str:
    pct = min(100, max(0, value))
    return f"""
    <div style="width:100%;height:{height}px;background:{COLORS['surface3']};border-radius:99px;overflow:hidden">
        <div style="width:{pct}%;height:100%;background:{color};border-radius:99px;transition:width .3s"></div>
    </div>"""


def section_header(text: str):
    st.markdown(
        f'<p style="font-size:11px;color:{COLORS["muted"]};text-transform:uppercase;letter-spacing:.1em;'
        f'font-weight:600;margin:18px 0 8px">{text}</p>',
        unsafe_allow_html=True,
    )