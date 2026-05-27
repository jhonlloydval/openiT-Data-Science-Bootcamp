"""
pages/4_Grade_Predictor.py — ToolHive AI
Assigned to: Iris
"""

import streamlit as st
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container
from utils.ollama_client import chat

st.set_page_config(
    page_title="Grade Predictor — ToolHive AI",
    page_icon="📊", layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title    = "Grade Predictor",
    subtitle = "Estimate your academic performance from study habits",
    cover_class = "cv-4",
)

SYSTEM_PROMPT = """You are an academic performance advisor. Based on the student's inputs below,
predict their academic performance and provide actionable advice.

Output format — use exactly these sections:

## Predicted Performance Band
State one of: Excellent / Good / Needs Improvement — and a brief one-sentence rationale.

## Analysis
2–3 sentences explaining which factors most influence the prediction.

## 3 Personalized Improvement Recommendations
Numbered list of 3 specific, actionable recommendations tailored to the student's profile."""

# ── Inputs ────────────────────────────────────────────────────────────────────
with tool_body_container():
    col1, col2 = st.columns(2)
    with col1:
        study_hours  = st.slider("Study hours per week", 0, 40, 10)
        attendance   = st.slider("Attendance rate (%)", 0, 100, 80)
        past_grade   = st.number_input("Past average grade (%)", 0.0, 100.0, 75.0, step=0.5)
    with col2:
        completion   = st.slider("Assignment completion rate (%)", 0, 100, 85)
        engagement   = st.slider("Self-assessed engagement (1 = low, 10 = high)", 1, 10, 6)

    if st.button("Predict Performance →"):
        user_message = (
            f"Study hours per week: {study_hours}\n"
            f"Attendance rate: {attendance}%\n"
            f"Past average grade: {past_grade}%\n"
            f"Assignment completion rate: {completion}%\n"
            f"Self-assessed engagement: {engagement}/10"
        )
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ]
        with st.spinner("Calculating prediction…"):
            result = chat(messages)
        st.markdown(result)
