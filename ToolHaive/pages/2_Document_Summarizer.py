"""
pages/2_Document_Summarizer.py — ToolHive AI
──────────────────────────────────────────────────────────────────────────────
Single-turn document summarizer. Returns structured summary, key points,
and action items from pasted text.

Assigned to: Iris
──────────────────────────────────────────────────────────────────────────────
"""

import streamlit as st
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container
from utils.ollama_client import chat

st.set_page_config(
    page_title="Doc Summarizer — ToolHive AI",
    page_icon="📄", layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title    = "Document Summarizer",
    subtitle = "Paste any text · Get structured summary, key points & action items",
    cover_class = "cv-2",
)

SYSTEM_PROMPT = """You are an expert document analyst. Analyze the submitted text and return
EXACTLY three sections — nothing else, no preamble, no commentary outside these sections:

## Summary
2–3 sentences capturing the core message.

## Key Points
Bullet list of the most important facts, arguments, or findings.

## Action Items
Bullet list of any recommended actions, next steps, or decisions mentioned.
If there are no action items, write: None identified."""

# ── UI ────────────────────────────────────────────────────────────────────────
with tool_body_container():
    st.markdown("#### Paste your document or text below")
    user_text = st.text_area(
        label       = "Document text",
        label_visibility = "collapsed",
        placeholder = "Paste an article, report, email, research paper, or any text here…",
        height      = 280,
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        run = st.button("Summarize →", use_container_width=True)
    with col2:
        if st.button("Clear", use_container_width=False):
            st.rerun()

    if run and user_text.strip():
        messages = [
            {"role": "system",  "content": SYSTEM_PROMPT},
            {"role": "user",    "content": user_text},
        ]
        with st.spinner("Analyzing…"):
            result = chat(messages)
        st.markdown(result)
    elif run:
        st.warning("Please paste some text first.")
