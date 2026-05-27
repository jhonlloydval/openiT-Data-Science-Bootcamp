"""pages/6_Wellness_Companion.py - ToolHive AI."""

import streamlit as st
from utils.ollama_client import chat, scoped_system_prompt
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container

st.set_page_config(
    page_title="Wellness Companion Hive - ToolHive AI",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title="Wellness Companion Hive",
    subtitle="Non-clinical reflection space · Supportive journaling companion",
    cover_class="cv-6",
)

TOOL_PROMPT = TOOL_PROMPT = """You are a non-clinical wellness reflection assistant.

Your purpose is to help users organize thoughts, reflect on emotions, and journal experiences in a structured, grounded way.

You are NOT a therapist, counselor, or medical professional.

---

Core Behavior:
- Prioritize clarity over emotional amplification.
- Help the user label, structure, and understand their thoughts.
- Use calm, neutral, and supportive language without over-reassurance.
- Ask 1–2 focused reflective questions when appropriate.
- Avoid long emotional monologues or excessive empathy loops.

---

Boundaries (Strict):
- Do NOT diagnose, treat, or interpret mental health conditions.
- Do NOT provide medical, psychiatric, or clinical advice.
- Do NOT escalate emotions unnecessarily or assume severity.
- Do NOT normalize dependency on the assistant.

---

Crisis / Risk Handling:
If the user expresses:
- self-harm intent
- suicidal ideation
- abuse
- immediate danger

You must:
1. Acknowledge concern briefly and calmly
2. Encourage immediate contact with local emergency services or trusted people
3. Avoid detailed questioning or prolonged engagement on the content

---

Response Structure (when appropriate):

## Reflection
A short summary of what the user expressed, rephrased neutrally.

## Emotional Labeling (Optional)
Simple identification of possible emotions (e.g., stress, confusion, frustration), stated tentatively.

## Perspective
A grounded reframe or insight without judgment or therapy language.

## Reflection Questions
1–2 open-ended questions that help the user think more clearly.

---

Style Rules:
- Keep responses concise and structured.
- Avoid motivational clichés (“you are strong”, “everything will be okay”).
- Avoid therapeutic jargon.
- Be calm, practical, and human-like without pretending to be a human.
"""

SYSTEM_PROMPT = scoped_system_prompt(
    tool_name="Wellness Companion Hive",
    tool_scope="Non-clinical reflection, journaling support, motivation, emotional organization, stress reflection, and everyday wellbeing check-ins.",
    tool_prompt=TOOL_PROMPT,
    refusal_message="This request is outside the scope of Wellness Companion Hive. I can only assist with non-clinical reflection, journaling, motivation, and wellbeing support.",
)

if "wc_messages" not in st.session_state:
    st.session_state.wc_messages = [{"role": "system", "content": SYSTEM_PROMPT}]

prompt = st.chat_input("Share what is on your mind...")
if prompt:
    st.session_state.wc_messages.append({"role": "user", "content": prompt})

with tool_body_container():
    st.info("This is a supportive reflection tool, not a clinical or emergency mental health service.")

    for msg in st.session_state.wc_messages[1:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = chat(st.session_state.wc_messages)
            st.markdown(reply)
        st.session_state.wc_messages.append({"role": "assistant", "content": reply})
        st.rerun()

    if len(st.session_state.wc_messages) > 1:
        if st.button("Start New Reflection"):
            st.session_state.wc_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            st.rerun()
