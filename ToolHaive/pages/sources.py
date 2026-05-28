"""pages/sources.py - ToolHaive AI sources page."""

from pathlib import Path

import streamlit as st

from utils.ui import HEX_PATTERN_SM, escape_html, inject_styles, render_html, render_navbar


st.set_page_config(
    page_title="Sources - ToolHaive AI",
    page_icon="TH",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="sources")


def file_rows() -> str:
    files_dir = Path(__file__).resolve().parent.parent / "files"
    if not files_dir.exists():
        return """
        <div class="src-row">
          <div class="src-row-title">Project files</div>
          <div class="src-row-copy">The files directory was not found in this workspace.</div>
        </div>
        """

    rows = []
    for path in sorted(item for item in files_dir.iterdir() if not item.name.startswith(".")):
        size_kb = path.stat().st_size / 1024
        rows.append(
            f"""
            <div class="src-row">
              <div class="src-row-title">{escape_html(path.name)}</div>
              <div class="src-row-copy">{size_kb:.1f} KB stored in the project files directory.</div>
            </div>
            """
        )

    if not rows:
        return """
        <div class="src-row">
          <div class="src-row-title">Project files</div>
          <div class="src-row-copy">No source files were found in the files directory.</div>
        </div>
        """
    return "".join(rows)


render_html(
    f"""
<style>
.sources-page {{
  padding-top: 64px;
  min-height: 100vh;
  background: var(--cream-light);
}}
.src-hero {{
  position: relative;
  overflow: hidden;
  background: var(--ink);
  padding: 72px 48px 60px;
}}
.src-hero::before {{
  content: "";
  position: absolute;
  inset: 0;
  opacity: 0.035;
  background-image: {HEX_PATTERN_SM};
  background-size: 70px 80px;
}}
.src-hero::after {{
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 700px 340px at 12% 30%, rgba(0,86,163,0.45), transparent 70%),
    radial-gradient(ellipse 520px 320px at 86% 30%, rgba(122,177,227,0.14), transparent 68%);
}}
.src-inner {{
  position: relative;
  z-index: 1;
  width: min(1180px, 100%);
  margin: 0 auto;
}}
.src-kicker {{
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--sky);
  margin-bottom: 14px;
}}
.src-title {{
  font-family: var(--font-display);
  font-size: clamp(38px, 6vw, 68px);
  line-height: 1;
  font-weight: 800;
  letter-spacing: 0;
  background: var(--grad-on-dark);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}
.src-sub {{
  max-width: 760px;
  margin-top: 18px;
  color: rgba(229,229,190,0.68);
  font-size: 17px;
  line-height: 1.75;
}}
.src-band {{
  padding: 54px 48px;
  background: var(--cream-light);
}}
.src-band.alt {{
  background: white;
}}
.src-section-head {{
  display: grid;
  grid-template-columns: minmax(0, 0.7fr) minmax(0, 1.3fr);
  gap: 40px;
  align-items: start;
  margin-bottom: 28px;
}}
.src-section-label {{
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--navy-mid);
}}
.src-section-title {{
  font-family: var(--font-display);
  font-size: clamp(24px, 3vw, 36px);
  font-weight: 800;
  line-height: 1.1;
  color: var(--ink);
}}
.src-section-copy {{
  color: var(--ink-muted);
  font-size: 15px;
  line-height: 1.8;
}}
.src-grid {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}}
.src-source {{
  border-top: 2px solid rgba(0,86,163,0.24);
  padding: 18px 4px 4px;
}}
.src-source-title {{
  font-family: var(--font-display);
  font-size: 17px;
  font-weight: 800;
  color: var(--ink);
  margin-bottom: 8px;
}}
.src-source-copy {{
  color: var(--ink-muted);
  font-size: 13px;
  line-height: 1.7;
}}
.src-rows {{
  border-top: 1px solid rgba(0,56,115,0.12);
}}
.src-row {{
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr);
  gap: 28px;
  padding: 18px 0;
  border-bottom: 1px solid rgba(0,56,115,0.10);
}}
.src-row-title {{
  font-weight: 800;
  color: var(--ink);
  word-break: break-word;
}}
.src-row-copy {{
  color: var(--ink-muted);
  line-height: 1.7;
}}
.src-process {{
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}}
.src-step {{
  background: rgba(255,255,255,0.62);
  border: 1px solid rgba(0,56,115,0.10);
  border-radius: 14px;
  padding: 18px;
}}
.src-step-num {{
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: var(--navy-mid);
  margin-bottom: 10px;
}}
.src-step-copy {{
  color: var(--ink-muted);
  font-size: 13px;
  line-height: 1.7;
}}
@media (max-width: 900px) {{
  .sources-page {{ padding-top: 64px; }}
  .src-hero, .src-band {{ padding-left: 24px; padding-right: 24px; }}
  .src-section-head {{ grid-template-columns: 1fr; gap: 14px; }}
  .src-grid, .src-process {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
}}
@media (max-width: 620px) {{
  .sources-page {{ padding-top: 106px; }}
  .src-grid, .src-process, .src-row {{ grid-template-columns: 1fr; }}
  .src-row {{ gap: 6px; }}
}}
</style>
<div class="sources-page">
  <section class="src-hero">
    <div class="src-inner">
      <div class="src-kicker">Project Evidence And Preparation</div>
      <div class="src-title">Sources</div>
      <div class="src-sub">
        The documents and references behind ToolHaive's product structure,
        visual system, model wrapper, and prompt boundaries.
      </div>
    </div>
  </section>

  <section class="src-band">
    <div class="src-inner">
      <div class="src-section-head">
        <div>
          <div class="src-section-label">Source Set</div>
          <div class="src-section-title">What informed the build.</div>
        </div>
        <div class="src-section-copy">
          ToolHaive was assembled from a small, deliberate source set: the
          project paper, the brand guide, model/API documentation, and bootcamp
          lessons on prompt engineering and AI workflow design.
        </div>
      </div>
      <div class="src-grid">
        <div class="src-source">
          <div class="src-source-title">ToolHaive Paper</div>
          <div class="src-source-copy">Internal design and architecture document used for the tool taxonomy, workflow framing, and scope boundaries.</div>
        </div>
        <div class="src-source">
          <div class="src-source-title">Brand Guide</div>
          <div class="src-source-copy">Visual identity reference used for colors, typography, cards, navigation, and the dark blue ToolHaive theme.</div>
        </div>
        <div class="src-source">
          <div class="src-source-title">Model Docs And Lessons</div>
          <div class="src-source-copy">Ollama model/API references and bootcamp materials guided the local model wrapper and prompt-first approach.</div>
        </div>
      </div>
    </div>
  </section>

  <section class="src-band alt">
    <div class="src-inner">
      <div class="src-section-head">
        <div>
          <div class="src-section-label">Preparation</div>
          <div class="src-section-title">How sources became app behavior.</div>
        </div>
        <div class="src-section-copy">
          The source documents were manually reviewed and distilled into
          interface patterns, tool descriptions, shared prompt rules, and
          scoped system prompts. This keeps the prototype simple and auditable.
        </div>
      </div>
      <div class="src-process">
        <div class="src-step"><div class="src-step-num">Step 01</div><div class="src-step-copy">Review project and brand documents for product goals, names, colors, and UI direction.</div></div>
        <div class="src-step"><div class="src-step-num">Step 02</div><div class="src-step-copy">Translate tool ideas into structured app pages with clear input and output expectations.</div></div>
        <div class="src-step"><div class="src-step-num">Step 03</div><div class="src-step-copy">Encode shared scope rules so each Hive stays inside its intended task area.</div></div>
        <div class="src-step"><div class="src-step-num">Step 04</div><div class="src-step-copy">Connect pages to the shared local model client and polish the user-facing workflow.</div></div>
      </div>
    </div>
  </section>

  <section class="src-band">
    <div class="src-inner">
      <div class="src-section-head">
        <div>
          <div class="src-section-label">Files</div>
          <div class="src-section-title">Project files currently included.</div>
        </div>
        <div class="src-section-copy">
          These are the local files in the project source directory that support
          the documentation and brand story for the prototype.
        </div>
      </div>
      <div class="src-rows">
        {file_rows()}
      </div>
    </div>
  </section>

  <section class="src-band alt">
    <div class="src-inner">
      <div class="src-section-head">
        <div>
          <div class="src-section-label">Data Quality</div>
          <div class="src-section-title">What the sources do and do not cover.</div>
        </div>
        <div class="src-section-copy">
          The sources explain ToolHaive's product and UI design. Individual tool
          knowledge comes from the local model and the prompts embedded in each
          page. The app does not browse the web or retrieve from a vector store
          during normal tool use.
        </div>
      </div>
    </div>
  </section>
</div>
"""
)
