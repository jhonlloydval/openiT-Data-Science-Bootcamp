"""pages/8_Career_Roadmap.py - ToolHive AI."""

import streamlit as st
from utils.ollama_client import chat
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container

st.set_page_config(
    page_title="Career Roadmap - ToolHive AI",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title="Career Roadmap",
    subtitle="Skill gaps, learning milestones, and next-step planning",
    cover_class="cv-8",
)

SYSTEM_PROMPT = """You are a practical career planning assistant.
Use the user's current role, skills, and target role to create a focused development roadmap.

Return exactly these sections:

## Target Readiness
A brief assessment of where the user stands now.

## Skill Gaps
Bullet list of the most important gaps to close.

## 30-60-90 Day Roadmap
Concrete milestones for the next 30, 60, and 90 days.

## Suggested Portfolio Proof
Specific project ideas or artifacts the user can build to demonstrate progress.
"""

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
