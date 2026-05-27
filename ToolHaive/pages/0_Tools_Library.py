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

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title   = "Tools Library — ToolHive AI",
    page_icon    = "🔷",
    layout       = "wide",
    initial_sidebar_state = "collapsed",
)

inject_styles()
render_navbar(active="dashboard")

# ── Built-in tool definitions ─────────────────────────────────────────────────
BUILTIN_TOOLS = [
    dict(
        id          = "interview_coach",
        name        = "Interview Coach Hive",
        user        = "For job applicants & professionals",
        desc        = "Simulates mock interviews with role-specific questions, evaluates answers, and provides structured feedback with improved suggestions.",
        cat         = "professional",
        cat_label   = "Professional",
        turn        = "multi",
        cover       = "cv-1",
        page        = "/Interview_Coach",
        icon_svg    = '<path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/>',
    ),
    dict(
        id          = "doc_summarizer",
        name        = "Doc Summarizer Hive",
        user        = "For students & researchers",
        desc        = "Accepts pasted text and returns a structured summary, key points, and action items — designed for fast academic and professional use.",
        cat         = "academic",
        cat_label   = "Academic",
        turn        = "single",
        cover       = "cv-2",
        page        = "/Document_Summarizer",
        icon_svg    = '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14,2 14,8 20,8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
    ),
    dict(
        id          = "doc_paraphraser",
        name        = "Doc Paraphraser Hive",
        user        = "For students & writers",
        desc        = "Rewrites user-submitted text in formal, casual, academic, or simplified tone while fully preserving original meaning.",
        cat         = "academic",
        cat_label   = "Academic",
        turn        = "single",
        cover       = "cv-3",
        page        = "/Document_Paraphraser",
        icon_svg    = '<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>',
    ),
    dict(
        id          = "grade_predictor",
        name        = "Grade Predictor Hive",
        user        = "For students",
        desc        = "Estimates academic performance from study hours, attendance, past grades, and self-assessed engagement with improvement tips.",
        cat         = "academic",
        cat_label   = "Academic",
        turn        = "single",
        cover       = "cv-4",
        page        = "/Grade_Predictor",
        icon_svg    = '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
    ),
    dict(
        id          = "roleplay_creator",
        name        = "Roleplay Creator Hive",
        user        = "For educators & trainers",
        desc        = "Configure an AI persona — historical figure, interviewer, or character — and engage in a structured in-character conversation.",
        cat         = "education",
        cat_label   = "Education",
        turn        = "multi",
        cover       = "cv-5",
        page        = "/Roleplay_Creator",
        icon_svg    = '<circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>',
    ),
    dict(
        id          = "wellness_companion",
        name        = "Wellness Companion Hive",
        user        = "For general users",
        desc        = "A judgment-free space for emotional reflection and journaling. Not a clinical tool — a supportive companion for everyday wellbeing.",
        cat         = "wellness",
        cat_label   = "Wellness",
        turn        = "multi",
        cover       = "cv-6",
        page        = "/Wellness_Companion",
        icon_svg    = '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>',
    ),
    dict(
        id          = "fact_checker",
        name        = "Fact Checker Hive",
        user        = "For general users",
        desc        = "Credibility analysis on news headlines, claims, or article excerpts — with logical consistency checks and verification source suggestions.",
        cat         = "media",
        cat_label   = "Media Literacy",
        turn        = "single",
        cover       = "cv-7",
        page        = "/Fact_Checker",
        icon_svg    = '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    ),
    dict(
        id          = "career_roadmap",
        name        = "Career Roadmap Hive",
        user        = "For professionals",
        desc        = "Structured career transition plan with identified skill gaps, learning milestones, and recommended resources based on your current role and goals.",
        cat         = "professional",
        cat_label   = "Professional",
        turn        = "single",
        cover       = "cv-8",
        page        = "/Career_Roadmap",
        icon_svg    = '<polygon points="3,11 22,2 13,21 11,13 3,11"/>',
    ),
    dict(
        id          = "grammar_checker",
        name        = "Grammar Checker Hive",
        user        = "For students & writers",
        desc        = "Review grammar, spelling, punctuation, and clarity. Get a writing quality score and targeted improvement suggestions without rewriting your voice.",
        cat         = "academic",
        cat_label   = "Academic",
        turn        = "single",
        cover       = "cv-2",
        page        = "/Grammar_Checker",
        icon_svg    = '<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><polyline points="17,4 20,7 13,14 10,14 10,11"/>',
    ),
    dict(
        id          = "essay_generator",
        name        = "Essay Generator Hive",
        user        = "For students & content creators",
        desc        = "Generate a structured essay or article draft from a topic, tone, and essay type. Optionally paste reference notes for the AI to draw from.",
        cat         = "academic",
        cat_label   = "Academic",
        turn        = "single",
        cover       = "cv-3",
        page        = "/Essay_Generator",
        icon_svg    = '<path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>',
    ),
    dict(
        id          = "quiz_flashcard_generator",
        name        = "Quiz & Flashcard Generator Hive",
        user        = "For students & educators",
        desc        = "Paste notes or a document excerpt and generate multiple choice questions, true/false quizzes, short answer sets, or study flashcards instantly.",
        cat         = "education",
        cat_label   = "Education",
        turn        = "single",
        cover       = "cv-4",
        page        = "/Quiz_Flashcard_Generator",
        icon_svg    = '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/><path d="M9 9h1m4 0h1M9 12h6"/>',
    ),
]

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
  background: var(--cream-light); padding: 26px 48px 4px;
}
.th-featured-inner {
  max-width: 1300px; margin: 0 auto;
}
.th-featured-card {
  display: grid; grid-template-columns: minmax(0,1fr) auto; align-items: center;
  gap: 24px; padding: 28px 30px; border-radius: 18px;
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
  font-weight: 800; letter-spacing: -0.02em; line-height: 1;
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
  border: 1px solid rgba(255,255,255,0.18); border-radius: 10px;
  padding: 13px 18px; white-space: nowrap;
}
@media (max-width: 760px) {
  .th-featured-strip { padding: 22px 22px 4px; }
  .th-featured-card { grid-template-columns: 1fr; padding: 24px; }
  .th-featured-action { width: fit-content; }
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
<div style="padding-top:64px;background:var(--cream-light);">

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
        <div class="th-featured-label">Featured</div>
        <div class="th-featured-title">HAIVE</div>
        <div class="th-featured-sub">
          General AI Assistant for open-ended chat, drafting, studying, planning, and problem solving.
          Powered by phi4-mini by default, with a model selector and more models coming soon.
        </div>
      </div>
      <div class="th-featured-action">Launch HAIVE -></div>
    </a>
  </div>
</div>
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