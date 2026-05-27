"""pages/8_Career_Roadmap.py - ToolHive AI."""

import streamlit as st
from utils.ollama_client import chat, scoped_system_prompt
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container

st.set_page_config(
    page_title="Career Roadmap Hive - ToolHive AI",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title="Career Roadmap Hive",
    subtitle="Skill gaps, learning milestones, and next-step planning",
    cover_class="cv-8",
)

TOOL_PROMPT = TOOL_PROMPT = """You are a precise, practical career planning and skill-gap analysis assistant.

Your job is to generate a highly actionable, realistic career roadmap based on the user's:
- current role/background
- target role
- current skills
- constraints (time, budget, schedule, learning preference)

Be specific, structured, and realistic. Avoid vague advice, generic motivation, or filler content.

If information is missing, make reasonable assumptions and explicitly state them under Target Readiness.

---

Return EXACTLY the following sections in Markdown:

## Target Readiness
- Brief but honest evaluation of the user’s current position relative to the target role.
- Include an estimated readiness level (e.g., Beginner / Junior-ready / Mid-transition, etc.).
- State assumptions if needed.

## Skill Gaps
- Identify the MOST critical missing skills only (prioritize impact, not completeness).
- Group gaps into:
  - Technical skills
  - Practical/industry skills
  - Tools/technologies (if relevant)
- Keep each item concise but specific.

## 30-60-90 Day Roadmap
Break down into three phases:

### 30 Days – Foundations
- Core fundamentals to focus on
- Minimal set of skills to build momentum
- Small practice tasks or drills

### 60 Days – Application
- Intermediate skills
- Small real-world projects or applied exercises
- Begin combining skills

### 90 Days – Portfolio & Readiness
- Portfolio-level projects
- Job/interview preparation tasks (if applicable)
- Proof-of-skill outputs

Each phase must include clear, actionable steps (not general suggestions).

## Suggested Portfolio Proof
- 2–4 concrete project ideas tailored to the target role
- Each project must include:
  - What it demonstrates (skills being proven)
  - Core features or scope
  - Why it is relevant to the target role

---

Rules:
- Be practical over inspirational.
- Avoid fluff, repetition, or generic career advice.
- Prioritize what gives the highest career impact first.
- Tailor everything specifically to the user’s target role.
- Keep outputs structured, scannable, and decision-ready.
"""

SYSTEM_PROMPT = scoped_system_prompt(
    tool_name="Career Roadmap Hive",
    tool_scope="Career planning, role transitions, skill gap analysis, learning milestones, professional development roadmaps, and portfolio planning.",
    tool_prompt=TOOL_PROMPT,
    refusal_message="This request is outside the scope of Career Roadmap Hive. I can only assist with career planning, skill gaps, roadmaps, and portfolio next steps.",
)

with tool_body_container():
    col1, col2 = st.columns(2)
    with col1:
        current_role = st.text_input("Current role or background", placeholder="e.g. junior analyst, student, teacher")
        target_role = st.text_input("Target role", placeholder="e.g. data analyst, ML engineer, product manager")
    with col2:
        current_skills = st.text_area("Current skills", placeholder="List tools, subjects, or experience you already have...", height=140)
        constraints = st.text_area("Constraints or preferences", placeholder="Time, budget, preferred learning style, location...", height=140)

    if st.button("Build Roadmap ->"):
        if current_role.strip() and target_role.strip():
            user_message = (
                f"Current role/background: {current_role}\n"
                f"Target role: {target_role}\n"
                f"Current skills: {current_skills or 'Not specified'}\n"
                f"Constraints/preferences: {constraints or 'Not specified'}"
            )
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ]
            with st.spinner("Building roadmap..."):
                result = chat(messages)
            st.markdown(result)
        else:
            st.warning("Please enter your current background and target role.")
