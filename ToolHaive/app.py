"""app.py — ToolHive AI · Landing / Onboarding Page."""

import streamlit as st
from utils.ui import inject_styles, render_html, render_navbar
from utils.ollama_client import MODEL_OPTIONS

# ── Import BUILTIN_TOOLS to compute counts dynamically ────────────────────────
# We import directly from the module so that adding a new tool to 0_Tools_Library.py
# automatically updates every count on the landing page.
import importlib, sys, os, types

def _load_builtin_tools():
    """Import BUILTIN_TOOLS without executing Streamlit UI calls."""
    src_path = os.path.join(os.path.dirname(__file__), "pages", "0_Tools_Library.py")
    spec = importlib.util.spec_from_file_location("_tools_lib", src_path)
    mod  = importlib.util.module_from_spec(spec)
    # Stub out streamlit so the page-level UI code doesn't execute
    _st_stub = types.ModuleType("streamlit")
    for attr in dir(st):
        setattr(_st_stub, attr, lambda *a, **kw: None)
    _st_stub.session_state = {}
    _st_stub.set_page_config = lambda **kw: None
    sys.modules["streamlit"] = _st_stub
    try:
        spec.loader.exec_module(mod)
    except Exception:
        pass
    finally:
        sys.modules["streamlit"] = st  # restore real streamlit
    return getattr(mod, "BUILTIN_TOOLS", [])

BUILTIN_TOOLS = _load_builtin_tools()

# ── Derived counts (single source of truth) ───────────────────────────────────
NUM_TOOLS        = len(BUILTIN_TOOLS)
NUM_MODELS_TOTAL = len(MODEL_OPTIONS)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ToolHive AI",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="home")

# ── Build preview cards dynamically from BUILTIN_TOOLS ────────────────────────
# HAIVE (general chat) is always first and links to /haive
HAIVE_CARD = """
      <a class=\"th-preview-card\" href=\"/haive\" target=\"_self\">
        <div class=\"th-preview-icon\" style=\"background:linear-gradient(135deg,#003973,#7AB1E3);\">
          <svg viewBox=\"0 0 24 24\"><path d=\"M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4z\"/><path d=\"M8 9h8M8 13h5\"/></svg>
        </div>
        <div class=\"th-preview-name\">HAIVE</div>
        <div class=\"th-preview-desc\">General AI chat with model selection and open-ended help</div>
      </a>
"""

# Gradient pool — cycles for each tool card
_GRADIENTS = [
    "linear-gradient(135deg,#002a58,#0056A3)",
    "linear-gradient(135deg,#003d1f,#1a7a4a)",
    "linear-gradient(135deg,#1a2a52,#2952a3)",
    "linear-gradient(135deg,#003d4a,#007a8a)",
    "linear-gradient(135deg,#2a1a52,#5a35a8)",
    "linear-gradient(135deg,#003355,#1a6e99)",
    "linear-gradient(135deg,#3d2200,#8a5200)",
    "linear-gradient(135deg,#002840,#005580)",
    "linear-gradient(135deg,#1a3a1a,#2e6b3a)",
    "linear-gradient(135deg,#3a1a1a,#8a3030)",
    "linear-gradient(135deg,#2a2a52,#4a4aa0)",
    "linear-gradient(135deg,#003a3a,#006060)",
]

def _tool_preview_card(tool: dict, idx: int) -> str:
    grad = _GRADIENTS[idx % len(_GRADIENTS)]
    icon = tool.get("icon_svg", "")
    name = tool.get("name", "")
    desc = tool.get("desc", "")
    page = tool.get("page", "/Tools_Library")
    return f"""
      <a class="th-preview-card" href="{page}" target="_self">
        <div class="th-preview-icon" style="background:{grad};">
          <svg viewBox="0 0 24 24">{icon}</svg>
        </div>
        <div class="th-preview-name">{name}</div>
        <div class="th-preview-desc">{desc[:80]}{'…' if len(desc) > 80 else ''}</div>
      </a>
"""

builtin_cards_html = "".join(
    _tool_preview_card(tool, idx) for idx, tool in enumerate(BUILTIN_TOOLS)
)

# ── Render page ───────────────────────────────────────────────────────────────
render_html(f"""
<div class="th-page" style="background:#0A1628;">

  <section class="th-hero">
    <div class="th-hero-hex-bg"></div>
    <div class="th-hero-glow"></div>
    <div class="th-hero-content">

      <div class="th-hero-eyebrow">
        openIT · Data Science Bootcamp · Capstone Project
      </div>

      <div class="th-hero-logo-row">
        <div class="th-hero-hex">
          <svg viewBox="0 0 24 24"><path d="M12 2L20 7V17L12 22L4 17V7L12 2Z"/></svg>
        </div>
        <div class="th-hero-wordmark">ToolHive AI</div>
      </div>

      <p class="th-hero-tagline">
        From <strong>HAIVE general chat</strong> to <strong>specialized assistants</strong>.<br/>
        A local AI workspace for open-ended thinking, focused tools, and fast task support.
      </p>

      <div class="th-hero-cta-row">
        <a class="th-btn-hero" href="/Tools_Library" target="_self">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none"
               stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2"  y="3"  width="7" height="7" rx="1"/>
            <rect x="15" y="3"  width="7" height="7" rx="1"/>
            <rect x="2"  y="14" width="7" height="7" rx="1"/>
            <rect x="15" y="14" width="7" height="7" rx="1"/>
          </svg>
          Explore Tools Library
        </a>
        <a class="th-btn-ghost" href="#tools-preview">Learn More</a>
      </div>

      <div class="th-hero-chips">
        <div class="th-chip">
          <svg viewBox="0 0 24 24"><rect x="2" y="3" width="7" height="7" rx="1"/><rect x="15" y="3" width="7" height="7" rx="1"/><rect x="2" y="14" width="7" height="7" rx="1"/><rect x="15" y="14" width="7" height="7" rx="1"/></svg>
          <span>{NUM_TOOLS} AI Tools</span>
        </div>
        <div class="th-chip">
          <svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="2"/><path d="M7 12h10M12 7v10"/></svg>
          <span>phi4-mini · Local</span>
        </div>
        <div class="th-chip">
          <svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          <span>100% Private</span>
        </div>
        <div class="th-chip">
          <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
          <span>Modular Platform</span>
        </div>
        <div class="th-chip">
          <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg>
          <span>Model Selector</span>
        </div>
      </div>

    </div>
  </section>

  <section class="th-preview" id="tools-preview">
    <div class="th-preview-label">General chat + {NUM_TOOLS} specialized tools · phi4-mini default · More models coming soon</div>
    <div class="th-preview-grid">

      {HAIVE_CARD}
      {builtin_cards_html}

    </div>

    <div class="th-stats-row">
      <div><div class="th-stat-num">{NUM_TOOLS}</div><div class="th-stat-label">AI Tools</div></div>
      <div><div class="th-stat-num">100%</div><div class="th-stat-label">Local · Private</div></div>
      <div><div class="th-stat-num">{NUM_MODELS_TOTAL}</div><div class="th-stat-label">Model Options</div></div>
      <div><div class="th-stat-num">∞</div><div class="th-stat-label">Custom Tools</div></div>
    </div>
  </section>

</div>
""")
