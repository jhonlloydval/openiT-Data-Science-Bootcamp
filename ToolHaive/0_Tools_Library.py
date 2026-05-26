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
import streamlit as st
from utils.ui import inject_styles, render_navbar, FILTER_JS

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
        name        = "Interview Coach",
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
        name        = "Doc Summarizer",
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
        name        = "Doc Paraphraser",
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
        name        = "Grade Predictor",
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
        name        = "Roleplay Creator",
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
        name        = "Wellness Companion",
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
        name        = "Fact Checker",
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
        name        = "Career Roadmap",
        user        = "For professionals",
        desc        = "Structured career transition plan with identified skill gaps, learning milestones, and recommended resources based on your current role and goals.",
        cat         = "professional",
        cat_label   = "Professional",
        turn        = "single",
        cover       = "cv-8",
        page        = "/Career_Roadmap",
        icon_svg    = '<polygon points="3,11 22,2 13,21 11,13 3,11"/>',
    ),
]

# ── Load custom tools from JSON ───────────────────────────────────────────────
CUSTOM_TOOLS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "custom_tools.json")

def load_custom_tools() -> list[dict]:
    try:
        if os.path.exists(CUSTOM_TOOLS_PATH):
            with open(CUSTOM_TOOLS_PATH) as f:
                return json.load(f)
    except Exception:
        pass
    return []

ALL_TOOLS = BUILTIN_TOOLS + load_custom_tools()

# ── Helper: render a single tool card ────────────────────────────────────────
def card_html(tool: dict) -> str:
    badge_class = "badge-multi" if tool.get("turn") == "multi" else "badge-single"
    badge_label = "Multi-turn"  if tool.get("turn") == "multi" else "Single-turn"
    page_href   = tool.get("page", "/Tools_Library")

    return f"""
    <div class="th-tool-card"
         data-cat="{tool['cat']}"
         data-name="{tool['name'].lower()}"
         onclick="window.location.href='{page_href}'">
      <div class="th-card-cover {tool['cover']}">
        <div class="th-card-cover-hex"></div>
        <div class="th-card-cover-shade"></div>
        <div class="th-card-cover-icon">
          <svg viewBox="0 0 24 24">{tool['icon_svg']}</svg>
        </div>
      </div>
      <div class="th-card-body">
        <div class="th-card-top-row">
          <span class="th-card-cat-tag">{tool['cat_label']}</span>
          <span class="th-card-turn-badge {badge_class}">{badge_label}</span>
        </div>
        <div class="th-card-name">{tool['name']}</div>
        <div class="th-card-user">{tool['user']}</div>
        <div class="th-card-desc">{tool['desc']}</div>
        <div class="th-card-footer">
          <button class="th-card-launch"
                  onclick="event.stopPropagation();window.location.href='{page_href}'">
            Launch
            <svg viewBox="0 0 24 24">
              <line x1="5" y1="12" x2="19" y2="12"/>
              <polyline points="12,5 19,12 12,19"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
    """

# ── Build all cards HTML ──────────────────────────────────────────────────────
all_cards_html = "".join(card_html(t) for t in ALL_TOOLS)

add_card_html = """
<div class="th-card-add" id="th-card-add"
     onclick="window.location.href='/Custom_Tool_Runner'">
  <div class="th-card-add-icon">
    <svg viewBox="0 0 24 24">
      <line x1="12" y1="5" x2="12" y2="19"/>
      <line x1="5"  y1="12" x2="19" y2="12"/>
    </svg>
  </div>
  <div class="th-card-add-label">Build Your Own Tool</div>
  <div class="th-card-add-sub">
    Define a name, system prompt, and input format —
    your tool is instantly available in this library.
  </div>
</div>
"""

# ── Render page ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="th-page" style="background:var(--cream-light);">

  <!-- ═══════════════  DASHBOARD HERO BAND  ═══════════════ -->
  <div class="th-dash-hero">
    <div class="th-dash-hex-bg"></div>
    <div class="th-dash-glow"></div>
    <div class="th-dash-inner">
      <div>
        <div class="th-dash-eyebrow">Modular GenAI Tools Library</div>
        <div class="th-dash-title">Tools Library</div>
        <div class="th-dash-sub">
          {len(ALL_TOOLS)} specialized assistants · Launch any tool or build your own
        </div>
      </div>
      <button class="th-dash-add-btn"
              onclick="window.location.href='/Custom_Tool_Runner'">
        <svg viewBox="0 0 24 24">
          <line x1="12" y1="5" x2="12" y2="19"/>
          <line x1="5"  y1="12" x2="19" y2="12"/>
        </svg>
        Add New Toolkit
      </button>
    </div>
  </div>

  <!-- ═══════════════  STICKY TOOLBAR  ═══════════════ -->
  <div class="th-toolbar">
    <div class="th-toolbar-inner">
      <div class="th-search-wrap">
        <svg viewBox="0 0 24 24">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input class="th-search-input"
               type="text"
               placeholder="Search tools by name or tag…"
               oninput="thSearch(this.value)"/>
      </div>
      <div class="th-tag-filters">
        <button class="th-tag-btn active" data-tag="all"
                onclick="thFilterTag('all')">All</button>
        <button class="th-tag-btn" data-tag="professional"
                onclick="thFilterTag('professional')">Professional</button>
        <button class="th-tag-btn" data-tag="academic"
                onclick="thFilterTag('academic')">Academic</button>
        <button class="th-tag-btn" data-tag="education"
                onclick="thFilterTag('education')">Education</button>
        <button class="th-tag-btn" data-tag="wellness"
                onclick="thFilterTag('wellness')">Wellness</button>
        <button class="th-tag-btn" data-tag="media"
                onclick="thFilterTag('media')">Media</button>
      </div>
      <span class="th-result-count" id="th-result-count">{len(ALL_TOOLS)} tools</span>
    </div>
  </div>

  <!-- ═══════════════  CARDS GRID  ═══════════════ -->
  <div class="th-cards-section">
    <div class="th-cards-inner">
      <div class="th-section-divider">
        <div class="th-divider-line"></div>
        <div class="th-divider-label">All tools available</div>
        <div class="th-divider-line"></div>
      </div>
      <div class="th-cards-grid" id="th-cards-grid">
        {all_cards_html}
        {add_card_html}
      </div>
    </div>
  </div>

</div>

{FILTER_JS}
""", unsafe_allow_html=True)
