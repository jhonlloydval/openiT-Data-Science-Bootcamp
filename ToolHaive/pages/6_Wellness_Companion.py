"""pages/6_Wellness_Companion.py - ToolHive AI."""

import streamlit as st
from utils.ollama_client import chat
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container

st.set_page_config(
    page_title="Wellness Companion - ToolHive AI",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title="Wellness Companion",
    subtitle="Non-clinical reflection space · Supportive journaling companion",
    cover_class="cv-6",
)

SYSTEM_PROMPT = """You are a non-clinical wellness companion.
Your role is to help the user reflect, journal, and organize feelings in a calm and supportive way.

Boundaries:
- Do not diagnose, treat, or claim to provide therapy.
- Do not give medical instructions.
- Encourage professional or trusted human support if the user describes crisis, self-harm, abuse, or immediate danger.
- Ask gentle reflective questions and keep responses practical, grounded, and warm.
"""

if "wc_messages" not in st.session_state:
    st.session_state.wc_messages = [{"role": "system", "content": SYSTEM_PROMPT}]

with tool_body_container():
    st.info("This is a supportive reflection tool, not a clinical or emergency mental health service.")

    for msg in st.session_state.wc_messages[1:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if len(st.session_state.wc_messages) > 1:
        if st.button("Start New Reflection"):
            st.session_state.wc_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            st.rerun()

if prompt := st.chat_input("Share what is on your mind..."):
    st.session_state.wc_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = chat(st.session_state.wc_messages)
        st.markdown(reply)
    st.session_state.wc_messages.append({"role": "assistant", "content": reply})
