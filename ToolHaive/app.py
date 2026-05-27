"""app.py — ToolHive AI · Landing / Onboarding Page."""

import streamlit as st
from utils.ui import inject_styles, render_html, render_navbar

st.set_page_config(
    page_title="ToolHive AI",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="home")

render_html("""
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
        From <strong>general chatbot</strong> to <strong>specialized assistant</strong>.<br/>
        Purpose-built AI tools for every task — no prompt engineering needed.
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
          <span>8 Specialized Tools</span>
        </div>
        <div class="th-chip">
          <svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="2"/><path d="M7 12h10M12 7v10"/></svg>
          <span>Llama 3.2 · Local</span>
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
          <span>No Prompt Needed</span>
        </div>
      </div>

    </div>
  </section>

  <section class="th-preview" id="tools-preview">
    <div class="th-preview-label">Available tools · Click any to launch</div>
    <div class="th-preview-grid">

      <a class="th-preview-card" href="/Tools_Library" target="_self">
        <div class="th-preview-icon" style="background:linear-gradient(135deg,#002a58,#0056A3);">
          <svg viewBox="0 0 24 24"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>
        </div>
        <div class="th-preview-name">Interview Coach</div>
        <div class="th-preview-desc">Role-specific mock interviews with AI feedback</div>
      </a>

      <a class="th-preview-card" href="/Tools_Library" target="_self">
        <div class="th-preview-icon" style="background:linear-gradient(135deg,#003d1f,#1a7a4a);">
          <svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14,2 14,8 20,8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
        </div>
        <div class="th-preview-name">Doc Summarizer</div>
        <div class="th-preview-desc">Key points and action items from any text</div>
      </a>

      <a class="th-preview-card" href="/Tools_Library" target="_self">
        <div class="th-preview-icon" style="background:linear-gradient(135deg,#1a2a52,#2952a3);">
          <svg viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
        </div>
        <div class="th-preview-name">Doc Paraphraser</div>
        <div class="th-preview-desc">Rewrite text in any tone or style</div>
      </a>

      <a class="th-preview-card" href="/Tools_Library" target="_self">
        <div class="th-preview-icon" style="background:linear-gradient(135deg,#003d4a,#007a8a);">
          <svg viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        </div>
        <div class="th-preview-name">Grade Predictor</div>
        <div class="th-preview-desc">Academic performance estimate from study habits</div>
      </a>

      <a class="th-preview-card" href="/Tools_Library" target="_self">
        <div class="th-preview-icon" style="background:linear-gradient(135deg,#2a1a52,#5a35a8);">
          <svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
        </div>
        <div class="th-preview-name">Roleplay Creator</div>
        <div class="th-preview-desc">Configure AI personas for scenario-based learning</div>
      </a>

      <a class="th-preview-card" href="/Tools_Library" target="_self">
        <div class="th-preview-icon" style="background:linear-gradient(135deg,#003355,#1a6e99);">
          <svg viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
        </div>
        <div class="th-preview-name">Wellness Companion</div>
        <div class="th-preview-desc">Judgment-free emotional reflection and journaling</div>
      </a>

      <a class="th-preview-card" href="/Tools_Library" target="_self">
        <div class="th-preview-icon" style="background:linear-gradient(135deg,#3d2200,#8a5200);">
          <svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        </div>
        <div class="th-preview-name">Fact Checker</div>
        <div class="th-preview-desc">Credibility analysis on news and claims</div>
      </a>

      <a class="th-preview-card" href="/Tools_Library" target="_self">
        <div class="th-preview-icon" style="background:linear-gradient(135deg,#002840,#005580);">
          <svg viewBox="0 0 24 24"><polygon points="3,11 22,2 13,21 11,13 3,11"/></svg>
        </div>
        <div class="th-preview-name">Career Roadmap</div>
        <div class="th-preview-desc">Structured plan with skill gaps and milestones</div>
      </a>

    </div>

    <div class="th-stats-row">
      <div><div class="th-stat-num">8</div><div class="th-stat-label">Specialized Tools</div></div>
      <div><div class="th-stat-num">100%</div><div class="th-stat-label">Local · Private</div></div>
      <div><div class="th-stat-num">0</div><div class="th-stat-label">Prompt Eng. Required</div></div>
      <div><div class="th-stat-num">∞</div><div class="th-stat-label">Custom Tools</div></div>
    </div>
  </section>

</div>
""")
