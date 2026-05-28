"""pages/about.py - ToolHaive AI about page."""

import streamlit as st

from utils.tools_data import BUILTIN_TOOLS
from utils.ollama_client import MODEL_OPTIONS
from utils.ui import HEX_PATTERN_SM, inject_styles, render_html, render_navbar


st.set_page_config(
    page_title="About - ToolHaive AI",
    page_icon="TH",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="about")

NUM_TOOLS = len(BUILTIN_TOOLS)
NUM_MODELS = len(MODEL_OPTIONS)

render_html(
    f"""
<style>
.about-page {{
  padding-top: 64px;
  min-height: 100vh;
  background: var(--cream-light);
}}
.about-hero {{
  position: relative;
  overflow: hidden;
  background: var(--ink);
  padding: 78px 48px 64px;
}}
.about-hero::before {{
  content: "";
  position: absolute;
  inset: 0;
  opacity: 0.035;
  background-image: {HEX_PATTERN_SM};
  background-size: 70px 80px;
}}
.about-hero::after {{
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 720px 360px at 10% 20%, rgba(0,86,163,0.45), transparent 70%),
    radial-gradient(ellipse 520px 320px at 85% 35%, rgba(122,177,227,0.16), transparent 68%);
}}
.about-hero-inner,
.about-band-inner {{
  position: relative;
  z-index: 1;
  width: min(1180px, 100%);
  margin: 0 auto;
}}
.about-kicker {{
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--sky);
  margin-bottom: 14px;
}}
.about-title {{
  font-family: var(--font-display);
  font-size: clamp(40px, 6vw, 72px);
  line-height: 1;
  font-weight: 800;
  letter-spacing: 0;
  background: var(--grad-on-dark);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}
.about-sub {{
  max-width: 760px;
  margin-top: 18px;
  color: rgba(229,229,190,0.68);
  font-size: 17px;
  line-height: 1.75;
}}
.about-stats {{
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin-top: 34px;
}}
.about-stat {{
  border: 1px solid rgba(122,177,227,0.18);
  background: rgba(255,255,255,0.045);
  border-radius: 14px;
  padding: 18px;
}}
.about-stat-value {{
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 800;
  color: white;
}}
.about-stat-label {{
  font-family: var(--font-mono);
  font-size: 9px;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: rgba(229,229,190,0.55);
  margin-top: 4px;
}}
.about-band {{
  padding: 54px 48px;
  background: var(--cream-light);
}}
.about-band.alt {{
  background: white;
}}
.about-section-head {{
  display: grid;
  grid-template-columns: minmax(0, 0.7fr) minmax(0, 1.3fr);
  gap: 40px;
  align-items: start;
  margin-bottom: 28px;
}}
.about-section-label {{
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--navy-mid);
}}
.about-section-title {{
  font-family: var(--font-display);
  font-size: clamp(24px, 3vw, 36px);
  font-weight: 800;
  color: var(--ink);
  line-height: 1.1;
}}
.about-section-copy {{
  color: var(--ink-muted);
  font-size: 15px;
  line-height: 1.8;
}}
.about-grid {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}}
.about-item {{
  border-top: 2px solid rgba(0,86,163,0.24);
  padding: 18px 4px 4px;
}}
.about-item-title {{
  font-family: var(--font-display);
  font-size: 17px;
  font-weight: 800;
  color: var(--ink);
  margin-bottom: 8px;
}}
.about-item-copy {{
  color: var(--ink-muted);
  font-size: 13px;
  line-height: 1.7;
}}
.about-rows {{
  border-top: 1px solid rgba(0,56,115,0.12);
}}
.about-row {{
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr);
  gap: 28px;
  padding: 18px 0;
  border-bottom: 1px solid rgba(0,56,115,0.10);
}}
.about-row-title {{
  font-weight: 800;
  color: var(--ink);
}}
.about-row-copy {{
  color: var(--ink-muted);
  line-height: 1.7;
}}
@media (max-width: 900px) {{
  .about-page {{ padding-top: 64px; }}
  .about-hero, .about-band {{ padding-left: 24px; padding-right: 24px; }}
  .about-stats, .about-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  .about-section-head {{ grid-template-columns: 1fr; gap: 14px; }}
}}
@media (max-width: 620px) {{
  .about-page {{ padding-top: 106px; }}
  .about-stats, .about-grid, .about-row {{ grid-template-columns: 1fr; }}
  .about-row {{ gap: 6px; }}
}}
</style>
<div class="about-page">
  <section class="about-hero">
    <div class="about-hero-inner">
      <div class="about-kicker">openIT Data Science Bootcamp Capstone</div>
      <div class="about-title">ToolHaive AI</div>
      <div class="about-sub">
        A local, privacy-first AI workspace that brings HAIVE general chat,
        specialized prompt tools, and a custom assistant builder into one
        coherent study and productivity environment.
      </div>
      <div class="about-stats">
        <div class="about-stat"><div class="about-stat-value">{NUM_TOOLS}</div><div class="about-stat-label">Built-in hives</div></div>
        <div class="about-stat"><div class="about-stat-value">1</div><div class="about-stat-label">General chat hub</div></div>
        <div class="about-stat"><div class="about-stat-value">{NUM_MODELS}</div><div class="about-stat-label">Model options</div></div>
        <div class="about-stat"><div class="about-stat-value">Local</div><div class="about-stat-label">Private by design</div></div>
      </div>
    </div>
  </section>

  <section class="about-band">
    <div class="about-band-inner">
      <div class="about-section-head">
        <div>
          <div class="about-section-label">Product Idea</div>
          <div class="about-section-title">A focused tool library for everyday AI work.</div>
        </div>
        <div class="about-section-copy">
          ToolHaive AI was built to show how scoped assistants can make local
          AI more useful than one generic chat box. Each Hive has a clear task,
          prompt boundary, interface, and output expectation so users can move
          quickly without rewriting instructions every time.
        </div>
      </div>
      <div class="about-grid">
        <div class="about-item">
          <div class="about-item-title">Scoped assistants</div>
          <div class="about-item-copy">Each tool has a defined role, allowed task area, and refusal boundary for cleaner outputs.</div>
        </div>
        <div class="about-item">
          <div class="about-item-title">Local model flow</div>
          <div class="about-item-copy">The app routes AI calls through Ollama, keeping the prototype private and easy to run locally.</div>
        </div>
        <div class="about-item">
          <div class="about-item-title">Expandable platform</div>
          <div class="about-item-copy">The library supports built-in tools plus user-created custom assistants stored locally.</div>
        </div>
      </div>
    </div>
  </section>

  <section class="about-band alt">
    <div class="about-band-inner">
      <div class="about-section-head">
        <div>
          <div class="about-section-label">Limitations</div>
          <div class="about-section-title">Clear boundaries for a prototype build.</div>
        </div>
        <div class="about-section-copy">
          The project is intentionally lightweight. It demonstrates product
          structure, prompt engineering, and local AI integration while leaving
          deeper retrieval, persistence, and cloud model options for later.
        </div>
      </div>
      <div class="about-rows">
        <div class="about-row"><div class="about-row-title">No retrieval pipeline</div><div class="about-row-copy">Tools use encoded prompts and user inputs, not embeddings or semantic search over source files.</div></div>
        <div class="about-row"><div class="about-row-title">Local model limits</div><div class="about-row-copy">Small local models can produce weaker reasoning or formatting than larger cloud models on complex tasks.</div></div>
        <div class="about-row"><div class="about-row-title">Session-based memory</div><div class="about-row-copy">Most chat and tool state is kept in Streamlit session state and can reset on refresh.</div></div>
        <div class="about-row"><div class="about-row-title">Prototype persistence</div><div class="about-row-copy">Custom tools are saved locally as JSON; there is no team sync, account system, or cloud sharing layer.</div></div>
      </div>
    </div>
  </section>

  <section class="about-band">
    <div class="about-band-inner">
      <div class="about-section-head">
        <div>
          <div class="about-section-label">Next Steps</div>
          <div class="about-section-title">What would make the platform stronger.</div>
        </div>
        <div class="about-section-copy">
          The clearest improvements are streaming responses, persistent
          conversation history, document retrieval over the project sources,
          import/export for custom tools, and optional higher-capability cloud
          model connections.
        </div>
      </div>
    </div>
  </section>
</div>
"""
)
