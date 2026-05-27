"""
pages/1_Interview_Coach.py — ToolHive AI
──────────────────────────────────────────────────────────────────────────────
Multi-turn AI interview simulator. Asks one question at a time, evaluates
the user's answer, and gives structured feedback before asking the next.

Assigned to: Iris
──────────────────────────────────────────────────────────────────────────────
"""

import streamlit as st
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container
from utils.ollama_client import chat

st.set_page_config(
    page_title="Interview Coach — ToolHive AI",
    page_icon="🎙️", layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title    = "Interview Coach",
    subtitle = "Role-specific mock interviews · AI-powered feedback",
    cover_class = "cv-1",
)

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a professional interviewer with expertise across multiple industries.
Your job is to conduct a realistic mock interview with the user.

Rules:
- Ask exactly ONE interview question at a time. Never ask two questions together.
- After the user responds, evaluate their answer on: Clarity, Relevance, and Depth.
- Give a score out of 10 and structured feedback.
- Then ask the next interview question.

Output format for each evaluation:
**Evaluation**
- Clarity: X/10
- Relevance: X/10
- Depth: X/10
- Overall: X/10

**Feedback**
[2-3 sentences on what was good and what can improve]

**Improved Sample Answer**
[A stronger version of their answer in 2-3 sentences]

---

Then ask the next question. Start by warmly greeting the user and asking what role/industry
they are preparing for, then immediately ask your first interview question."""

# ── Session state ─────────────────────────────────────────────────────────────
if "ic_messages" not in st.session_state:
    st.session_state.ic_messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# ── Render chat history ───────────────────────────────────────────────────────
with tool_body_container():
    for msg in st.session_state.ic_messages[1:]:   # skip system
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if len(st.session_state.ic_messages) == 1:
        st.info("Start by telling the coach what role or industry you are preparing for.")

    # ── Reset button ──────────────────────────────────────────────────────────
    if len(st.session_state.ic_messages) > 1:
        if st.button("Start New Interview"):
            st.session_state.ic_messages = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
            st.rerun()

# ── Handle new input ──────────────────────────────────────────────────────────
if prompt := st.chat_input("Type your answer or ask a question…"):
    st.session_state.ic_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            reply = chat(st.session_state.ic_messages)
        st.markdown(reply)
    st.session_state.ic_messages.append({"role": "assistant", "content": reply})
