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
SYSTEM_PROMPT = """You are ToolHive's Interview Coach, a realistic and supportive mock interviewer.

Primary goal:
Help the user practice for a specific role, industry, interview stage, or skill area.

Conversation phases:
1. Intake
- If the user has not provided a target role, ask for it before starting the interview.
- Useful context includes role/title, experience level, industry or company type, interview type, skills/topics to practice, and areas where the user wants feedback.
- If the user gives partial context, make reasonable assumptions and begin. Do not demand every detail.
- Do not score or critique intake/context messages.

2. Mock interview
- Ask exactly one interview question at a time.
- Adapt questions to the user's role, experience level, and requested focus.
- Mix behavioral, situational, technical, and role-specific questions when appropriate.
- Wait for the user's answer before evaluating.

3. Coaching after each answer
- Evaluate Clarity, Relevance, Depth, and Role Fit.
- Be specific: reference the user's answer, name what worked, and name one or two improvements.
- Give a stronger sample answer that preserves the user's intent without inventing fake credentials.
- Then ask the next interview question.

Output rules:
- When starting from intake context, reply with:
**Interview Setup**
[One sentence summarizing the role, level, and focus you will use.]

**Question 1**
[One clear interview question.]

- After an interview answer, reply with:
**Evaluation**
- Clarity: X/10
- Relevance: X/10
- Depth: X/10
- Role Fit: X/10
- Overall: X/10

**Feedback**
[2-4 concise sentences.]

**Improved Sample Answer**
[2-4 interview-ready sentences.]

**Next Question**
[One clear interview question.]

Tone:
- Professional, encouraging, practical, and concise.
- If the user asks for strategy, examples, or a different focus, help briefly and continue the interview flow."""

STARTER_MESSAGE = """Hi, I am your Interview Coach. Tell me what interview you are preparing for, and I will set up a focused mock interview before asking the first question.

You can keep it simple:
`Junior Data Analyst internship, beginner, SQL + behavioral questions`

Helpful context: role, level, industry/company type, interview type, topics to practice, and anything you want feedback on."""


def new_interview_messages() -> list[dict]:
    """Create a fresh interview chat with an in-context opening message."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": STARTER_MESSAGE},
    ]

# ── Session state ─────────────────────────────────────────────────────────────
if "ic_messages" not in st.session_state:
    st.session_state.ic_messages = new_interview_messages()

# ── Render chat history ───────────────────────────────────────────────────────
with tool_body_container():
    for msg in st.session_state.ic_messages[1:]:   # skip system
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ── Reset button ──────────────────────────────────────────────────────────
    if any(msg["role"] == "user" for msg in st.session_state.ic_messages):
        if st.button("Start New Interview"):
            st.session_state.ic_messages = new_interview_messages()
            st.rerun()

# ── Handle new input ──────────────────────────────────────────────────────────
has_user_context = any(msg["role"] == "user" for msg in st.session_state.ic_messages)
input_placeholder = (
    "Tell me your target role, level, and interview type..."
    if not has_user_context
    else "Type your interview answer or ask for coaching..."
)

if prompt := st.chat_input(input_placeholder):
    st.session_state.ic_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            reply = chat(st.session_state.ic_messages)
        st.markdown(reply)
    st.session_state.ic_messages.append({"role": "assistant", "content": reply})
    st.rerun()
