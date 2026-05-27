"""
pages/3_Document_Paraphraser.py — ToolHive AI
Assigned to: Iris
"""

import streamlit as st
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container
from utils.ollama_client import chat

st.set_page_config(
    page_title="Doc Paraphraser — ToolHive AI",
    page_icon="✏️", layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title    = "Document Paraphraser",
    subtitle = "Rewrite in Formal · Casual · Academic · Simplified tone",
    cover_class = "cv-3",
)

SYSTEM_PROMPTS = {
    "Formal": "You are a professional editor. Rewrite the submitted text in a formal, polished tone suitable for corporate or official documents. Preserve all original meaning exactly — do not add or remove any information. Return ONLY the rewritten text, no commentary.",
    "Casual": "You are a professional editor. Rewrite the submitted text in a friendly, conversational, casual tone — as if speaking to a colleague. Preserve all original meaning exactly. Return ONLY the rewritten text, no commentary.",
    "Academic": "You are a professional editor. Rewrite the submitted text in an academic, scholarly tone appropriate for university papers or journals. Use precise vocabulary and formal sentence structures. Preserve all original meaning exactly. Return ONLY the rewritten text, no commentary.",
    "Simplified": "You are a professional editor. Rewrite the submitted text in simple, clear language that anyone can understand — use short sentences and common words. Preserve all original meaning exactly. Return ONLY the rewritten text, no commentary.",
}

with tool_body_container():
    tone = st.selectbox("Select output tone", list(SYSTEM_PROMPTS.keys()))
    user_text = st.text_area(
        label            = "Your text",
        label_visibility = "collapsed",
        placeholder      = "Paste the text you want to paraphrase…",
        height           = 260,
    )

    run = st.button("Paraphrase →", use_container_width=False)
    if run and user_text.strip():
        messages = [
            {"role": "system", "content": SYSTEM_PROMPTS[tone]},
            {"role": "user",   "content": user_text},
        ]
        with st.spinner(f"Rewriting in {tone} tone…"):
            result = chat(messages)
        st.markdown(f"**{tone} version:**")
        st.markdown(result)
    elif run:
        st.warning("Please paste some text first.")
