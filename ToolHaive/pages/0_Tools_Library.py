"""
pages/0_Tools_Library.py — ToolHive AI · Dashboard
──────────────────────────────────────────────────────────────────────────────
Renders the cream-background dashboard: hero band, sticky toolbar with
live search + category filters, and the 4-column tool card grid.

All styling comes from utils/ui.py.
Custom user tools are loaded from data/custom_tools.json and merged here.
──────────────────────────────────────────────────────────────────────────────
"""

import json
import os
import html
import streamlit as st
from utils.ui import inject_styles, render_html, render_navbar
from utils.tools_data import BUILTIN_TOOLS

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title   = "Tools Library — ToolHive AI",
    page_icon    = "🔷",
    layout       = "wide",
    initial_sidebar_state = "collapsed",
)

inject_styles()
render_navbar(active="dashboard")

# ── Load custom tools from JSON ───────────────────────────────────────────────
CUSTOM_TOOLS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "custom_tools.json")

DEFAULT_CUSTOM_ICON = '<path d="M12 5v14M5 12h14"/>'


def load_custom_tools() -> list[dict]:
    try:
        if os.path.exists(CUSTOM_TOOLS_PATH):
            with open(CUSTOM_TOOLS_PATH) as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
    except Exception:
        pass
    return []

def normalize_custom_tool(tool: dict, idx: int) -> dict:
    name = str(tool.get("name") or f"Custom Tool {idx + 1}")
    cat = str(tool.get("cat") or tool.get("category") or "custom").lower()
    return dict(
        id=str(tool.get("id") or f"custom_{idx}"),
        name=name,
        user=str(tool.get("user") or tool.get("target_user") or "User-created assistant"),
        desc=str(tool.get("desc") or tool.get("description") or "A custom prompt-powered assistant."),
        cat=cat,
        cat_label=str(tool.get("cat_label") or cat.title()),
        turn=str(tool.get("turn") or "single"),
        cover=str(tool.get("cover") or "cv-8"),
        page=str(tool.get("page") or "/Custom_Tool_Runner"),
        icon_svg=str(tool.get("icon_svg") or DEFAULT_CUSTOM_ICON),
    )


CUSTOM_TOOLS = [normalize_custom_tool(t, i) for i, t in enumerate(load_custom_tools()) if isinstance(t, dict)]
ALL_TOOLS = BUILTIN_TOOLS + CUSTOM_TOOLS
CATEGORY_OPTIONS = {
    "All": "all",
    "Professional": "professional",
    "Academic": "academic",
    "Education": "education",
    "Wellness": "wellness",
    "Media": "media",
    "Custom": "custom",
}

render_html("""
<style>
.th-featured-strip {
  background: var(--cream-light); padding: 26px 48px 28px;
}
.th-featured-inner {
  max-width: 1300px; margin: 0 auto;
}
.th-featured-card {
  display: grid; grid-template-columns: minmax(0,1fr) auto; align-items: center;
  gap: 24px; padding: 28px 30px; border-radius: 22px;
  background:
    linear-gradient(135deg,rgba(10,22,40,0.98),rgba(0,57,115,0.94)),
    linear-gradient(90deg,#003973,#0056A3,#7AB1E3);
  border: 1px solid rgba(122,177,227,0.38);
  box-shadow: 0 24px 60px rgba(0,56,115,0.18);
  color: white; text-decoration: none !important; overflow: hidden;
  position: relative;
}
.th-featured-label {
  display: inline-flex; width: fit-content; margin-bottom: 12px;
  font-family: var(--font-mono); font-size: 9px; letter-spacing: 0.16em;
  text-transform: uppercase; color: var(--cream);
  border: 1px solid rgba(229,229,190,0.24); border-radius: 999px;
  padding: 5px 10px; background: rgba(229,229,190,0.06);
}
.th-featured-title {
  font-family: var(--font-display); font-size: clamp(28px,4vw,46px);
  font-weight: 800; letter-spacing: 0; line-height: 1;
  background: var(--grad); -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; background-clip: text;
}
.th-featured-sub {
  font-size: 15px; color: rgba(229,229,190,0.68);
  margin-top: 10px; line-height: 1.6; max-width: 720px;
}
.th-featured-action {
  font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.12em;
  text-transform: uppercase; color: white; background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.18); border-radius: 12px;
  padding: 13px 18px; white-space: nowrap;
}
@media (max-width: 760px) {
  .th-featured-strip { padding: 22px 22px 24px; }
  .th-featured-card { grid-template-columns: 1fr; padding: 24px; }
  .th-featured-action { width: fit-content; }
}
/* Ensure toolbar container has a clear white background and no overlap */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"]:has(.st-key-tool-toolbar) {
  background: white !important;
  position: sticky !important;
  top: 64px !important;
  z-index: 100 !important;
}
div[data-testid="stColumn"] > div[data-testid="stVerticalBlock"] {
  gap: 0 !important;
}
</style>
""")

# ── Helper: render a single tool card ────────────────────────────────────────
def card_html(tool: dict) -> str:
    badge_class = "badge-multi" if tool.get("turn") == "multi" else "badge-single"
    badge_label = "Multi-turn"  if tool.get("turn") == "multi" else "Single-turn"
    page_href = str(tool.get("page") or "/Tools_Library")
    if not page_href.startswith("/"):
        page_href = "/Tools_Library"
    safe_href = html.escape(page_href, quote=True)
    safe_name = html.escape(str(tool.get("name", "Untitled Tool")), quote=True)
    safe_cat = html.escape(str(tool.get("cat", "custom")), quote=True)
    safe_cover = html.escape(str(tool.get("cover", "cv-8")), quote=True)
    safe_cat_label = html.escape(str(tool.get("cat_label", "Custom")), quote=True)
    safe_user = html.escape(str(tool.get("user", "")), quote=True)
    safe_desc = html.escape(str(tool.get("desc", "")), quote=True)

    return f"""
    <div class="th-tool-card"
         data-cat="{safe_cat}"
         data-name="{safe_name.lower()}">
      <div class="th-card-cover {safe_cover}">
        <div class="th-card-cover-hex"></div>
        <div class="th-card-cover-shade"></div>
        <div class="th-card-cover-icon">
          <svg viewBox="0 0 24 24">{tool.get('icon_svg', DEFAULT_CUSTOM_ICON)}</svg>
        </div>
      </div>
      <div class="th-card-body">
        <div class="th-card-top-row">
          <span class="th-card-cat-tag">{safe_cat_label}</span>
          <span class="th-card-turn-badge {badge_class}">{badge_label}</span>
        </div>
        <div class="th-card-name">{safe_name}</div>
        <div class="th-card-user">{safe_user}</div>
        <div class="th-card-desc">{safe_desc}</div>
        <div class="th-card-footer">
          <a class="th-card-launch" href="{safe_href}" target="_self">
            Launch
            <svg viewBox="0 0 24 24">
              <line x1="5" y1="12" x2="19" y2="12"/>
              <polyline points="12,5 19,12 12,19"/>
            </svg>
          </a>
        </div>
      </div>
    </div>
    """

add_card_html = """
<div class="th-card-add" id="th-card-add">
  <div class="th-card-add-icon">
    <svg viewBox="0 0 24 24">
      <line x1="12" y1="5" x2="12" y2="19"/>
      <line x1="5"  y1="12" x2="19" y2="12"/>
    </svg>
  </div>
  <div class="th-card-add-label">Build Your Own Hive</div>
  <div class="th-card-add-sub">
    Define a name, system prompt, and input format —
    your custom assistant is instantly available in this library.
  </div>
  <a class="th-card-launch" href="/Custom_Tool_Runner" target="_self">Build Hive</a>
</div>
"""

# ── Render page ───────────────────────────────────────────────────────────────
render_html(f"""
<div style="padding-top:64px;background:var(--ink);">

  <!-- ═══════════════  DASHBOARD HERO BAND  ═══════════════ -->
  <div class="th-dash-hero">
    <div class="th-dash-hex-bg"></div>
    <div class="th-dash-glow"></div>
    <div class="th-dash-inner">
      <div>
        <div class="th-dash-eyebrow">Modular GenAI Tools Library</div>
        <div class="th-dash-title">Tools Library</div>
        <div class="th-dash-sub">
          HAIVE general chat + {len(ALL_TOOLS)} specialized assistants · Launch any Hive or build your own
        </div>
      </div>
      <a class="th-dash-add-btn" href="/Custom_Tool_Runner" target="_self">
        <svg viewBox="0 0 24 24">
          <line x1="12" y1="5" x2="12" y2="19"/>
          <line x1="5"  y1="12" x2="19" y2="12"/>
        </svg>
        Add New Hive
      </a>
    </div>
  </div>
</div>
""")

render_html("""
<div class="th-featured-strip">
  <div class="th-featured-inner">
    <a class="th-featured-card" href="/haive" target="_self">
      <div class="th-featured-content">
        <div class="th-featured-label">Featured · General Chat</div>
        <div class="th-featured-title">HAIVE</div>
        <div class="th-featured-sub">
          General AI Assistant for open-ended chat, drafting, studying, planning, and problem solving.
          Powered by phi4-mini by default, with a model selector and more models coming soon.
        </div>
      </div>
      <div class="th-featured-action">Launch HAIVE →</div>
    </a>
  </div>
</div>
<div style="height:1px;background:rgba(0,56,115,0.09);"></div>
""")

with st.container(key="tool-toolbar"):
    search_col, category_col, count_col = st.columns([2.2, 3.2, 0.7], vertical_alignment="bottom")
    with search_col:
        query = st.text_input(
            "Search",
            placeholder="Search tools by name or tag...",
            label_visibility="collapsed",
        )
    with category_col:
        category_label = st.segmented_control(
            "Category",
            options=list(CATEGORY_OPTIONS.keys()),
            default="All",
            label_visibility="collapsed",
        ) or "All"

selected_category = CATEGORY_OPTIONS[category_label]
query_norm = query.lower().strip()

def matches_filters(tool: dict) -> bool:
    haystack = " ".join([
        str(tool.get("name", "")),
        str(tool.get("cat", "")),
        str(tool.get("cat_label", "")),
        str(tool.get("user", "")),
        str(tool.get("desc", "")),
    ]).lower()
    category_match = selected_category == "all" or tool.get("cat") == selected_category
    query_match = not query_norm or query_norm in haystack
    return category_match and query_match


visible_tools = [tool for tool in ALL_TOOLS if matches_filters(tool)]
with count_col:
    st.caption(f"{len(visible_tools)} tool{'s' if len(visible_tools) != 1 else ''}")

cards_html = "".join(card_html(t) for t in visible_tools)
if selected_category == "all" and not query_norm:
    cards_html += add_card_html

empty_html = ""
if not visible_tools:
    empty_html = """
    <div class="th-empty-state">
      No tools match that search. Try another category or keyword.
    </div>
    """

render_html(f"""
<div style="background:var(--cream-light);">
  <div class="th-cards-section">
    <div class="th-cards-inner">
      <div class="th-section-divider">
        <div class="th-divider-line"></div>
        <div class="th-divider-label">All tools available</div>
        <div class="th-divider-line"></div>
      </div>
      <div class="th-cards-grid" id="th-cards-grid">
        {cards_html}
      </div>
      {empty_html}
    </div>
  </div>
</div>
""")