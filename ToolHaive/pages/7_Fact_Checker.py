"""pages/7_Fact_Checker.py - ToolHive AI."""

import streamlit as st
from utils.ollama_client import chat
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container

st.set_page_config(
    page_title="Fact Checker - ToolHive AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title="Fact Checker",
    subtitle="Credibility analysis for claims, headlines, and article excerpts",
    cover_class="cv-7",
)

SYSTEM_PROMPT = """You are a careful media-literacy assistant.
Analyze the submitted claim or article excerpt for credibility signals.

Return exactly these sections:

## Credibility Assessment
Likely Reliable / Unclear / Likely Misleading, with a one-sentence rationale.

## Reasoning
Bullet points covering logical consistency, missing context, emotional language, and evidence quality.

## What To Verify Next
A short list of source types the user should consult. Do not invent live citations or claim you checked the web.
"""

with tool_body_container():
    user_text = st.text_area(
        "Claim, headline, or article excerpt",
        placeholder="Paste a headline, social media claim, or article excerpt here...",
        height=260,
    )

    run = st.button("Analyze Credibility ->")
    if run and user_text.strip():
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ]
        with st.spinner("Reviewing credibility signals..."):
            result = chat(messages)
        st.markdown(result)
    elif run:
        st.warning("Please paste a claim or excerpt first.")
