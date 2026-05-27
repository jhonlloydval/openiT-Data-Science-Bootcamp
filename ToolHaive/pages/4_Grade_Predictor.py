"""
pages/4_Grade_Predictor.py — ToolHive AI
Assigned to: Iris
"""

import streamlit as st
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container
from utils.ollama_client import chat, scoped_system_prompt

st.set_page_config(
    page_title="Grade Predictor Hive — ToolHive AI",
    page_icon="📊", layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title    = "Grade Predictor Hive",
    subtitle = "Estimate your academic performance from study habits",
    cover_class = "cv-4",
)

TOOL_PROMPT = TOOL_PROMPT = """You are a student performance analysis assistant.

Your task is to estimate likely academic performance based ONLY on the provided study habits and academic indicators.

Important:
- This is NOT a real prediction model.
- Treat outputs as heuristic estimations, not guaranteed outcomes.
- Avoid overconfidence or deterministic language.

---

Output format — use EXACTLY these sections:

## Predicted Performance Band
Choose one:
- Excellent
- Good
- Needs Improvement

Then provide a 1-sentence justification based only on the given inputs.

Do NOT imply certainty.

---

## Key Influencing Factors
Explain in 2–4 concise sentences:
- Which inputs most strongly affected the assessment
- Any positive vs negative signals
- Any limitations in the data (if applicable)

Avoid generic statements.

---

## Risk & Opportunity Signals
List:
- 2–3 positive indicators (what is working well)
- 2–3 improvement risks (what may limit performance)

Be specific to the inputs.

---

## 3 Personalized Improvement Recommendations
Provide exactly 3 numbered recommendations.

Rules:
- Each must map directly to one weak or moderate input
- Must be actionable (what to do, not vague advice)
- Must be realistic for a student context
- No motivational filler

---

Strict Rules:
- Do NOT claim you can accurately predict real grades.
- Do NOT use psychological or clinical framing.
- Do NOT be overly optimistic or punitive.
- Base everything strictly on the provided metrics.
"""

SYSTEM_PROMPT = scoped_system_prompt(
    tool_name="Grade Predictor Hive",
    tool_scope="Academic performance estimation, study habit analysis, attendance and assignment pattern reflection, and student improvement recommendations.",
    tool_prompt=TOOL_PROMPT,
    refusal_message="This request is outside the scope of Grade Predictor Hive. I can only assist with academic performance estimates and student improvement advice.",
)

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
