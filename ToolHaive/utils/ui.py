"""
utils/ui.py
───────────────────────────────────────────────────────────────────────────────
ToolHive AI — Shared UI / Frontend Layer
───────────────────────────────────────────────────────────────────────────────
"""

import html

import streamlit as st

# ── Hex-grid SVG patterns ─────────────────────────────────────────────────────
HEX_PATTERN_LG = (
    "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
    "width='90' height='104' viewBox='0 0 90 104'%3E"
    "%3Cpolygon points='45,4 86,25 86,69 45,90 4,69 4,25' "
    "fill='none' stroke='%23E5E5BE' stroke-width='1'/%3E%3C/svg%3E\")"
)
HEX_PATTERN_SM = (
    "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
    "width='70' height='80' viewBox='0 0 70 80'%3E"
    "%3Cpolygon points='35,3 67,19 67,52 35,68 3,52 3,19' "
    "fill='none' stroke='%23E5E5BE' stroke-width='1'/%3E%3C/svg%3E\")"
)
HEX_PATTERN_CARD = (
    "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
    "width='44' height='50' viewBox='0 0 44 50'%3E"
    "%3Cpolygon points='22,2 42,12 42,32 22,42 2,32 2,12' "
    "fill='none' stroke='white' stroke-width='1.2'/%3E%3C/svg%3E\")"
)

FONTS_HTML = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
"""

BASE_CSS = """
<style>
*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; }
a { text-decoration: none; }
.th-nav-logo, .th-nav-link, .th-nav-cta, .th-btn-hero, .th-btn-ghost,
.th-preview-card, .th-tool-card, .th-card-add, .th-card-launch, .th-tool-back {
  text-decoration: none !important;
}
.th-nav-logo:visited, .th-nav-cta:visited, .th-btn-hero:visited, .th-btn-hero { color: white !important; }
.th-nav-link:visited { color: rgba(229,229,190,0.5) !important; }
.th-nav-link.active:visited { color: #E5E5BE !important; }
.th-btn-ghost:visited, .th-btn-ghost { color: rgba(229,229,190,0.7) !important; }
.th-preview-card:visited, .th-tool-card:visited, .th-card-add:visited { color: inherit !important; }

:root {
  --navy:        #003973;
  --navy-mid:    #0056A3;
  --sky:         #7AB1E3;
  --cream:       #E5E5BE;
  --cream-light: #F5F5E8;
  --cream-dark:  #C8C89A;
  --ink:         #0A1628;
  --ink-mid:     #2A3A5C;
  --ink-muted:   #6B7A96;
  --white:       #FFFFFF;
  --grad:        linear-gradient(90deg,#003973 0%,#0056A3 40%,#7AB1E3 75%,#E5E5BE 100%);
  --grad-135:    linear-gradient(135deg,#003973 0%,#0056A3 40%,#7AB1E3 75%,#E5E5BE 100%);
  --font-display:'Syne', sans-serif;
  --font-body:   'DM Sans', sans-serif;
  --font-mono:   'DM Mono', monospace;
}

[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
#MainMenu                         { visibility: hidden !important; }
footer                            { visibility: hidden !important; }
header                            { visibility: hidden !important; }
[data-testid="stToolbar"]         { display: none !important; }
[data-testid="stDecoration"]      { display: none !important; }

.block-container { padding: 0 !important; max-width: 100% !important; }
.stApp { font-family: var(--font-body) !important; background: var(--cream-light) !important; }

/* ── Navbar ── */
.th-nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
  background: rgba(10,22,40,0.92);
  backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(122,177,227,0.1);
  height: 64px; display: flex; align-items: center; padding: 0 48px;
}
.th-nav-logo {
  display: flex; align-items: center; gap: 12px;
  text-decoration: none; margin-right: auto; cursor: pointer;
}
.th-nav-hex {
  width: 34px; height: 34px;
  background: linear-gradient(135deg,#003973,#0056A3,#7AB1E3);
  clip-path: polygon(50% 0%,95% 25%,95% 75%,50% 100%,5% 75%,5% 25%);
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.th-nav-hex svg { width: 16px; height: 16px; fill: white; }
.th-nav-wordmark {
  font-family: var(--font-display); font-size: 20px; font-weight: 800;
  letter-spacing: -0.02em;
  background: var(--grad); -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; background-clip: text;
}
.th-nav-links { display: flex; align-items: center; gap: 4px; margin-right: 24px; }
.th-nav-link {
  font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.1em;
  text-transform: uppercase; color: rgba(229,229,190,0.5);
  padding: 8px 16px; border-radius: 8px; cursor: pointer;
  border: none; background: transparent;
  display: inline-flex; align-items: center; text-decoration: none;
  transition: color 0.2s, background 0.2s;
}
.th-nav-link:hover { color: rgba(229,229,190,0.9); background: rgba(255,255,255,0.05); }
.th-nav-link.active { color: #E5E5BE; }
.th-nav-cta {
  font-family: var(--font-body); font-size: 13px; font-weight: 500;
  background: var(--grad); color: white;
  padding: 9px 22px; border-radius: 9px; border: none; cursor: pointer;
  display: inline-flex; align-items: center; text-decoration: none;
  transition: opacity 0.2s, transform 0.2s; white-space: nowrap;
}
.th-nav-cta:hover { opacity: 0.9; transform: translateY(-1px); }

.th-page { padding-top: 64px; min-height: 100vh; }

/* ── LANDING: Hero ── */
.th-hero {
  min-height: calc(100vh - 64px); display: flex; flex-direction: column;
  align-items: center; justify-content: center; text-align: center;
  padding: 80px 48px 60px; position: relative; overflow: hidden;
  background: #0A1628;
}
.th-hero-hex-bg {
  position: absolute; inset: 0; opacity: 0.035;
  background-image: HEX_PATTERN_LG_PLACEHOLDER;
  background-size: 90px 104px; pointer-events: none;
}
.th-hero-glow {
  position: absolute; inset: 0; pointer-events: none;
  background:
    radial-gradient(ellipse 900px 600px at 15% 60%, rgba(0,56,115,0.55) 0%, transparent 70%),
    radial-gradient(ellipse 600px 500px at 85% 25%, rgba(122,177,227,0.16) 0%, transparent 65%),
    radial-gradient(ellipse 400px 400px at 55% 85%, rgba(229,229,190,0.06) 0%, transparent 60%);
}
.th-hero-content { position: relative; z-index: 2; max-width: 860px; width: 100%; }
.th-hero-eyebrow {
  font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.22em;
  text-transform: uppercase; color: var(--sky); margin-bottom: 28px; opacity: 0.8;
}
.th-hero-logo-row {
  display: flex; align-items: center; justify-content: center;
  gap: 18px; margin-bottom: 20px;
}
.th-hero-hex {
  width: 60px; height: 60px; flex-shrink: 0;
  background: linear-gradient(135deg,#003973,#0056A3,#7AB1E3);
  clip-path: polygon(50% 0%,95% 25%,95% 75%,50% 100%,5% 75%,5% 25%);
  display: flex; align-items: center; justify-content: center;
}
.th-hero-hex svg { width: 28px; height: 28px; fill: white; }
.th-hero-wordmark {
  font-family: var(--font-display); font-size: clamp(48px,8vw,80px); font-weight: 800;
  letter-spacing: -0.03em; line-height: 1;
  background: var(--grad); -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; background-clip: text;
}
.th-hero-tagline {
  font-family: var(--font-body); font-size: clamp(15px,2vw,19px); font-weight: 300;
  color: rgba(229,229,190,0.6); letter-spacing: 0.02em; margin-bottom: 40px; line-height: 1.6;
}
.th-hero-tagline strong { color: rgba(229,229,190,0.9); font-weight: 400; }
.th-hero-cta-row {
  display: flex; gap: 14px; justify-content: center; margin-bottom: 56px; flex-wrap: wrap;
}
.th-btn-hero {
  font-family: var(--font-body); font-size: 15px; font-weight: 500;
  background: var(--grad); color: white; padding: 14px 36px; border-radius: 11px;
  border: none; cursor: pointer; transition: opacity 0.2s, transform 0.2s;
  display: inline-flex; align-items: center; gap: 8px; text-decoration: none;
}
.th-btn-hero:hover { opacity: 0.9; transform: translateY(-2px); }
.th-btn-ghost {
  font-family: var(--font-body); font-size: 15px; font-weight: 400;
  background: transparent; color: rgba(229,229,190,0.7);
  padding: 13px 28px; border-radius: 11px;
  border: 1px solid rgba(229,229,190,0.2); cursor: pointer;
  display: inline-flex; align-items: center; text-decoration: none;
  transition: border-color 0.2s, color 0.2s;
}
.th-btn-ghost:hover { border-color: rgba(229,229,190,0.5); color: rgba(229,229,190,0.95); }
.th-hero-chips { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
.th-chip {
  background: rgba(255,255,255,0.05); border: 1px solid rgba(122,177,227,0.2);
  border-radius: 8px; padding: 7px 16px; display: inline-flex; align-items: center;
  gap: 8px; transition: border-color 0.2s;
}
.th-chip:hover { border-color: rgba(122,177,227,0.45); }
.th-chip svg {
  width: 14px; height: 14px; stroke: var(--sky); fill: none;
  stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; flex-shrink: 0;
}
.th-chip span {
  font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.1em;
  text-transform: uppercase; color: rgba(229,229,190,0.55);
}

/* ── LANDING: Preview strip ── */
.th-preview { padding: 60px 48px 80px; background: linear-gradient(180deg,#0A1628 0%,#0d1e35 100%); }
.th-preview-label {
  text-align: center; font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.2em;
  text-transform: uppercase; color: rgba(122,177,227,0.5); margin-bottom: 32px;
}
.th-preview-grid {
  display: grid; grid-template-columns: repeat(4,1fr);
  gap: 16px; max-width: 1300px; margin: 0 auto;
}
.th-preview-card {
  background: rgba(255,255,255,0.04); border: 1px solid rgba(122,177,227,0.12);
  border-radius: 16px; padding: 22px 20px; display: flex; flex-direction: column;
  gap: 10px; cursor: pointer; text-decoration: none;
  transition: background 0.2s, border-color 0.2s, transform 0.2s;
}
.th-preview-card:hover {
  background: rgba(255,255,255,0.07); border-color: rgba(122,177,227,0.3);
  transform: translateY(-3px);
}
.th-preview-icon {
  width: 40px; height: 40px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.th-preview-icon svg {
  width: 20px; height: 20px; fill: none; stroke: white;
  stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round;
}
.th-preview-name { font-family: var(--font-display); font-size: 13px; font-weight: 700; color: rgba(255,255,255,0.85); }
.th-preview-desc { font-size: 11px; color: rgba(255,255,255,0.35); line-height: 1.5; }
@media (max-width: 1100px) { .th-preview-grid { grid-template-columns: repeat(2,1fr); } }
@media (max-width: 640px)  { .th-preview-grid { grid-template-columns: 1fr; } }

/* ── Stats ── */
.th-stats-row {
  display: flex; justify-content: center; gap: 64px; flex-wrap: wrap;
  padding: 40px 48px; border-top: 1px solid rgba(122,177,227,0.08);
  max-width: 1300px; margin: 0 auto;
}
.th-stat-num {
  font-family: var(--font-display); font-size: 36px; font-weight: 800;
  letter-spacing: -0.02em; background: var(--grad);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; text-align: center;
}
.th-stat-label {
  font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.15em;
  text-transform: uppercase; color: rgba(229,229,190,0.35); margin-top: 4px; text-align: center;
}

/* ── DASHBOARD: Hero band ── */
.th-dash-hero {
  background: var(--ink); padding: 40px 48px 36px;
  position: relative; overflow: hidden;
}
.th-dash-hex-bg {
  position: absolute; inset: 0; opacity: 0.03;
  background-image: HEX_PATTERN_SM_PLACEHOLDER;
  background-size: 70px 80px; pointer-events: none;
}
.th-dash-glow {
  position: absolute; inset: 0; pointer-events: none;
  background: radial-gradient(ellipse 700px 300px at 0% 50%,rgba(0,56,115,0.5) 0%,transparent 70%);
}
.th-dash-inner {
  position: relative; z-index: 1; max-width: 1300px; margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between; gap: 24px; flex-wrap: wrap;
}
.th-dash-eyebrow {
  font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.2em;
  text-transform: uppercase; color: var(--sky); opacity: 0.7; margin-bottom: 8px;
}
.th-dash-title {
  font-family: var(--font-display); font-size: clamp(24px,3vw,36px); font-weight: 800;
  letter-spacing: -0.02em; background: var(--grad);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.th-dash-sub { font-size: 14px; color: rgba(229,229,190,0.45); margin-top: 6px; }
.th-dash-add-btn {
  font-family: var(--font-body); font-size: 13px; font-weight: 500;
  background: var(--grad); color: white; padding: 11px 24px; border-radius: 10px;
  border: none; cursor: pointer; white-space: nowrap; flex-shrink: 0;
  transition: opacity 0.2s, transform 0.2s;
  display: inline-flex; align-items: center; gap: 8px; text-decoration: none;
}
.th-dash-add-btn:hover { opacity: 0.9; transform: translateY(-1px); }
.th-dash-add-btn svg {
  width: 16px; height: 16px; fill: none; stroke: white;
  stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;
}

/* ── DASHBOARD: Toolbar ── */
.th-toolbar {
  background: white; border-bottom: 1px solid rgba(0,56,115,0.08);
  padding: 16px 48px; position: sticky; top: 64px; z-index: 100;
}
.th-toolbar-inner {
  max-width: 1300px; margin: 0 auto; width: 100%;
  display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
}
.th-search-wrap { position: relative; flex: 1; min-width: 200px; max-width: 360px; }
.th-search-wrap svg {
  position: absolute; left: 12px; top: 50%; transform: translateY(-50%);
  width: 15px; height: 15px; stroke: var(--ink-muted); fill: none;
  stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;
}
.th-search-input {
  width: 100%; border: 1.5px solid rgba(0,56,115,0.15); border-radius: 9px;
  padding: 9px 14px 9px 36px; font-size: 13px; font-family: var(--font-body);
  color: var(--ink); background: white; outline: none; transition: border-color 0.2s;
}
.th-search-input:focus { border-color: var(--navy-mid); }
.th-search-input::placeholder { color: var(--ink-muted); }
.th-tag-filters { display: flex; gap: 6px; flex-wrap: wrap; margin-left: auto; }
.th-tag-btn {
  font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.08em;
  text-transform: uppercase; padding: 7px 14px; border-radius: 7px;
  border: 1px solid rgba(0,56,115,0.15); background: transparent;
  color: var(--ink-muted); cursor: pointer; transition: all 0.15s;
}
.th-tag-btn:hover { border-color: var(--navy-mid); color: var(--navy-mid); }
.th-tag-btn.active { background: var(--navy); color: var(--cream); border-color: var(--navy); }
.th-result-count {
  font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--ink-muted); white-space: nowrap;
}
.st-key-tool-toolbar {
  background: white; border-bottom: 1px solid rgba(0,56,115,0.08);
  padding: 16px 48px; position: sticky; top: 64px; z-index: 100;
}
.st-key-tool-toolbar > div {
  max-width: 1300px; margin: 0 auto;
}
.st-key-tool-toolbar label {
  font-family: var(--font-mono) !important; font-size: 10px !important;
  letter-spacing: 0.12em !important; text-transform: uppercase !important;
  color: var(--ink-muted) !important;
}

/* ── DASHBOARD: Cards grid ── */
.th-cards-section { padding: 32px 48px 64px; background: var(--cream-light); }
.th-cards-inner { max-width: 1300px; margin: 0 auto; }
.th-section-divider { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.th-divider-line { flex: 1; height: 1px; background: rgba(0,56,115,0.1); }
.th-divider-label {
  font-family: var(--font-mono); font-size: 9px; letter-spacing: 0.18em;
  text-transform: uppercase; color: var(--ink-muted);
}
.th-cards-grid {
  display: grid; grid-template-columns: repeat(4,1fr); gap: 18px;
}
@media (max-width: 1200px) { .th-cards-grid { grid-template-columns: repeat(3,1fr); } }
@media (max-width: 900px)  { .th-cards-grid { grid-template-columns: repeat(2,1fr); } }
@media (max-width: 580px)  { .th-cards-grid { grid-template-columns: 1fr; } }

/* ── Tool card ── */
.th-tool-card {
  background: white; border: 1px solid rgba(0,56,115,0.1);
  border-radius: 20px; overflow: hidden; display: flex; flex-direction: column;
  cursor: pointer; color: inherit; text-decoration: none;
  transition: transform 0.22s, box-shadow 0.22s, border-color 0.22s;
}
.th-tool-card:hover {
  transform: translateY(-6px); box-shadow: 0 20px 56px rgba(0,56,115,0.14);
  border-color: rgba(0,86,163,0.2);
}
.th-card-cover {
  height: 120px; position: relative; overflow: hidden;
  display: flex; align-items: center; justify-content: center;
}
.th-card-cover-hex {
  position: absolute; inset: 0; opacity: 0.07;
  background-image: HEX_PATTERN_CARD_PLACEHOLDER; background-size: 44px 50px;
}
.th-card-cover-shade {
  position: absolute; inset: 0;
  background: linear-gradient(to bottom, transparent 30%, rgba(0,0,0,0.32) 100%);
}
.th-card-cover-icon {
  position: relative; z-index: 1; width: 52px; height: 52px;
  background: rgba(255,255,255,0.15); border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  backdrop-filter: blur(4px); border: 1px solid rgba(255,255,255,0.2);
}
.th-card-cover-icon svg {
  width: 26px; height: 26px; fill: none; stroke: white;
  stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round;
}
.cv-1 { background: linear-gradient(135deg,#002a58 0%,#003973 45%,#0056A3 100%); }
.cv-2 { background: linear-gradient(135deg,#003d1f 0%,#00552d 45%,#1a7a4a 100%); }
.cv-3 { background: linear-gradient(135deg,#1a2a52 0%,#1e3a7a 45%,#2952a3 100%); }
.cv-4 { background: linear-gradient(135deg,#003d4a 0%,#005566 45%,#007a8a 100%); }
.cv-5 { background: linear-gradient(135deg,#2a1a52 0%,#3d2278 45%,#5a35a8 100%); }
.cv-6 { background: linear-gradient(135deg,#003355 0%,#004d80 45%,#1a6e99 100%); }
.cv-7 { background: linear-gradient(135deg,#3d2200 0%,#5a3300 45%,#8a5200 100%); }
.cv-8 { background: linear-gradient(135deg,#002840 0%,#003d5c 45%,#005580 100%); }

.th-card-body { padding: 18px 20px 20px; display: flex; flex-direction: column; gap: 9px; flex: 1; }
.th-card-top-row { display: flex; align-items: flex-start; justify-content: space-between; gap: 8px; }
.th-card-cat-tag {
  font-family: var(--font-mono); font-size: 8.5px; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--navy-mid);
  background: rgba(0,86,163,0.08); padding: 3px 10px; border-radius: 100px; white-space: nowrap;
}
.th-card-turn-badge {
  font-family: var(--font-mono); font-size: 8px; letter-spacing: 0.06em;
  padding: 3px 9px; border-radius: 100px; white-space: nowrap;
}
.badge-multi  { background: rgba(122,177,227,0.15); color: #1a5d82; }
.badge-single { background: rgba(200,200,154,0.35); color: #5a5a28; }
.th-card-name {
  font-family: var(--font-display); font-size: 15px; font-weight: 700;
  color: var(--ink); letter-spacing: -0.01em; line-height: 1.2;
}
.th-card-user  { font-size: 11px; color: var(--sky); font-weight: 400; margin-top: -4px; }
.th-card-desc  { font-size: 11.5px; color: var(--ink-muted); line-height: 1.6; flex: 1; }
.th-card-footer {
  display: flex; align-items: center; justify-content: space-between;
  padding-top: 12px; margin-top: 6px; border-top: 1px solid rgba(0,56,115,0.07);
}
.th-card-launch {
  font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--navy-mid); background: rgba(0,86,163,0.07);
  border: none; padding: 7px 16px; border-radius: 7px; cursor: pointer;
  display: inline-flex; align-items: center; gap: 6px; text-decoration: none;
  transition: background 0.15s, color 0.15s;
}
.th-card-launch:hover { background: var(--navy); color: white; }
.th-card-launch svg {
  width: 11px; height: 11px; fill: none; stroke: currentColor;
  stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;
}

.th-card-add {
  background: transparent; border: 2px dashed rgba(0,86,163,0.2);
  border-radius: 20px; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 14px; padding: 40px 24px; cursor: pointer; text-align: center; text-decoration: none;
  min-height: 280px; transition: border-color 0.2s, background 0.2s;
}
.th-card-add:hover { border-color: rgba(0,86,163,0.45); background: rgba(0,86,163,0.03); }
.th-card-add-icon {
  width: 52px; height: 52px; border-radius: 14px;
  border: 2px dashed rgba(0,86,163,0.25);
  display: flex; align-items: center; justify-content: center;
}
.th-card-add-icon svg {
  width: 24px; height: 24px; fill: none; stroke: var(--navy-mid);
  stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; opacity: 0.6;
}
.th-card-add-label {
  font-family: var(--font-display); font-size: 14px; font-weight: 700;
  color: var(--navy-mid); opacity: 0.7;
}
.th-card-add-sub { font-size: 11px; color: var(--ink-muted); line-height: 1.5; opacity: 0.7; }

/* ── Tool page shared ── */
.th-tool-header {
  background: var(--ink); padding: 32px 48px 28px; position: relative; overflow: hidden;
}
.th-tool-header-hex {
  position: absolute; inset: 0; opacity: 0.03;
  background-image: HEX_PATTERN_SM_PLACEHOLDER; background-size: 70px 80px; pointer-events: none;
}
.th-tool-header-inner { position: relative; z-index: 1; max-width: 900px; margin: 0 auto; }
.th-tool-back {
  font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase;
  color: rgba(229,229,190,0.4); background: none; border: none; cursor: pointer;
  padding: 0; margin-bottom: 16px; display: inline-flex; align-items: center; gap: 6px;
  text-decoration: none; transition: color 0.2s;
}
.th-tool-back:hover { color: rgba(229,229,190,0.8); }
.th-tool-page-title {
  font-family: var(--font-display); font-size: 28px; font-weight: 800; letter-spacing: -0.02em;
  background: var(--grad); -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; background-clip: text;
}
.th-tool-page-sub { font-size: 13px; color: rgba(229,229,190,0.4); margin-top: 4px; }
.th-tool-body {
  max-width: 900px; margin: 0 auto; padding: 32px 48px 64px;
  background: var(--cream-light); min-height: calc(100vh - 200px);
}
.st-key-tool-body {
  max-width: 900px; margin: 0 auto; padding: 32px 48px 64px;
  background: var(--cream-light); min-height: calc(100vh - 200px);
}
.th-tool-body .stTextArea textarea, .st-key-tool-body textarea {
  border: 1.5px solid rgba(0,56,115,0.15) !important; border-radius: 10px !important;
  font-family: var(--font-body) !important; font-size: 14px !important;
  color: var(--ink) !important; background: white !important;
}
.th-tool-body .stTextArea textarea:focus, .st-key-tool-body textarea:focus {
  border-color: var(--navy-mid) !important; box-shadow: 0 0 0 3px rgba(0,86,163,0.08) !important;
}
.th-tool-body .stButton button, .st-key-tool-body .stButton button {
  background: linear-gradient(90deg,#003973,#0056A3) !important;
  color: white !important; border: none !important; border-radius: 9px !important;
  font-family: var(--font-body) !important; font-size: 14px !important;
  font-weight: 500 !important; padding: 10px 28px !important;
}
.th-tool-body .stButton button:hover, .st-key-tool-body .stButton button:hover { opacity: 0.88 !important; }

.th-output-box {
  background: white; border: 1px solid rgba(0,56,115,0.1);
  border-radius: 14px; padding: 24px 28px; margin-top: 20px;
}
.th-output-label {
  font-family: var(--font-mono); font-size: 9px; letter-spacing: 0.2em;
  text-transform: uppercase; color: var(--ink-muted); margin-bottom: 14px;
  display: flex; align-items: center; gap: 8px;
}
.th-output-label::after { content: ''; flex: 1; height: 1px; background: rgba(0,56,115,0.07); }
.th-empty-state {
  background: white; border: 1px solid rgba(0,56,115,0.1); border-radius: 16px;
  padding: 28px; text-align: center; color: var(--ink-muted); font-size: 14px;
}
.th-nav-logo, .th-nav-link, .th-nav-cta, .th-dash-add-btn, .th-btn-hero,
.th-btn-ghost, .th-preview-card, .th-tool-card, .th-card-add, .th-card-launch,
.th-tool-back {
  text-decoration: none !important;
}
.th-nav-cta, .th-nav-cta:visited, .th-dash-add-btn, .th-dash-add-btn:visited,
.th-btn-hero, .th-btn-hero:visited {
  color: white !important;
}
.th-nav-link, .th-nav-link:visited { color: rgba(229,229,190,0.5) !important; }
.th-nav-link.active, .th-nav-link.active:visited { color: #E5E5BE !important; }
.th-btn-ghost, .th-btn-ghost:visited { color: rgba(229,229,190,0.7) !important; }
</style>
"""

BASE_CSS = (
    BASE_CSS
    .replace("HEX_PATTERN_LG_PLACEHOLDER",   HEX_PATTERN_LG)
    .replace("HEX_PATTERN_SM_PLACEHOLDER",   HEX_PATTERN_SM)
    .replace("HEX_PATTERN_CARD_PLACEHOLDER", HEX_PATTERN_CARD)
)

# ── Public API ────────────────────────────────────────────────────────────────

def clean_html(markup: str) -> str:
    """Keep multi-line HTML out of Markdown's indented-code parser."""
    return "\n".join(line.lstrip() for line in markup.strip().splitlines())


def render_html(markup: str):
    st.markdown(clean_html(markup), unsafe_allow_html=True)


def escape_html(value) -> str:
    return html.escape(str(value), quote=True)


def tool_body_container():
    return st.container(key="tool-body")


def inject_styles():
    render_html(FONTS_HTML)
    render_html(BASE_CSS)


def render_navbar(active: str = "home"):
    """Render the fixed top navbar."""
    home_active = 'active' if active == 'home' else ''
    dash_active = 'active' if active == 'dashboard' else ''

    render_html(f"""
    <nav class="th-nav">
      <a class="th-nav-logo" href="/" target="_self" aria-label="ToolHive AI Home">
        <div class="th-nav-hex">
          <svg viewBox="0 0 24 24"><path d="M12 2L20 7V17L12 22L4 17V7L12 2Z"/></svg>
        </div>
        <span class="th-nav-wordmark">ToolHive AI</span>
      </a>
      <div class="th-nav-links">
        <a class="th-nav-link {home_active}" href="/" target="_self">Home</a>
        <a class="th-nav-link {dash_active}" href="/Tools_Library" target="_self">Tools Library</a>
        <a class="th-nav-link" href="/#tools-preview" target="_self">About</a>
      </div>
      <a class="th-nav-cta" href="/Tools_Library" target="_self">Launch a Tool →</a>
    </nav>
    """)


def render_tool_header(title: str, subtitle: str, cover_class: str = "cv-1"):
    render_html(f"""
    <div class="th-tool-header">
      <div class="th-tool-header-hex"></div>
      <div class="th-tool-header-inner">
        <a class="th-tool-back" href="/Tools_Library" target="_self">
          ← Back to Library
        </a>
        <div class="th-tool-page-title">{escape_html(title)}</div>
        <div class="th-tool-page-sub">{escape_html(subtitle)}</div>
      </div>
    </div>
    """)


def close_tool_body():
    pass


def render_output_box(content: str):
    safe_content = escape_html(content).replace(chr(10), "<br>")
    render_html(f"""
    <div class="th-output-box">
      <div class="th-output-label">AI Output</div>
      <div style="font-family:var(--font-body);font-size:14px;color:var(--ink);line-height:1.7;">
        {safe_content}
      </div>
    </div>
    """)


# ── New tool UI helpers ────────────────────────────────────────────────────────

def render_label(text: str):
    """Render a small section label above a widget."""
    render_html(f"""
    <div style="
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--ink-muted);
      margin: 20px 0 6px;
    ">{escape_html(text)}</div>
    """)


def render_section_divider():
    """Thin divider between tool sections."""
    render_html("""
    <hr style="border:none;border-top:1px solid rgba(0,57,115,0.12);margin:24px 0 20px;">
    """)


def render_grammar_badge(label: str, color: str = "#003973"):
    """Inline badge used in Grammar Checker output legend."""
    render_html(f"""
    <span style="
      display: inline-block;
      background: {color};
      color: white;
      font-family: var(--font-mono);
      font-size: 11px;
      padding: 3px 10px;
      border-radius: 999px;
      margin-right: 6px;
    ">{escape_html(label)}</span>
    """)


def render_tool_tip(message: str):
    """Light info-tip box for tool instructions."""
    render_html(f"""
    <div style="
      background: rgba(0,57,115,0.06);
      border-left: 3px solid var(--navy-mid);
      border-radius: 0 8px 8px 0;
      padding: 12px 16px;
      font-family: var(--font-body);
      font-size: 13px;
      color: var(--ink-mid);
      margin-bottom: 16px;
      line-height: 1.6;
    ">💡 {escape_html(message)}</div>
    """)


def render_output_header(title: str):
    """Bold section header used above AI output blocks."""
    render_html(f"""
    <div style="
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 700;
      color: var(--navy);
      margin: 28px 0 10px;
      padding-bottom: 6px;
      border-bottom: 2px solid rgba(0,57,115,0.15);
    ">{escape_html(title)}</div>
    """)