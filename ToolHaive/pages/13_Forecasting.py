"""
pages/13_Forecasting.py - ToolHive AI

Standalone Forecasting Hive. It can use GradeWise session data when present,
or run a manual academic forecast from entered grade progress.
"""

from __future__ import annotations

import json
import math
from typing import Optional

import streamlit as st

from utils.ollama_client import chat, scoped_system_prompt
from utils.ui import (
    escape_html,
    inject_styles,
    render_html,
    render_navbar,
    render_tool_header,
    tool_body_container,
)


st.set_page_config(
    page_title="Forecasting Hive - ToolHive AI",
    page_icon="FC",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title="Forecasting Hive",
    subtitle="Forecast required scores, risk, and next academic priorities",
    cover_class="cv-6",
)


COLORS = {
    "ink": "#0A1628",
    "navy": "#003973",
    "blue": "#0056A3",
    "sky": "#7AB1E3",
    "cream": "#E5E5BE",
    "muted": "#6B7A96",
    "green": "#1C9B73",
    "amber": "#C98316",
    "orange": "#D86C20",
    "red": "#C83F4A",
}


def _safe(value) -> str:
    return escape_html(value)


def fmt(value: Optional[float], decimals: int = 1) -> str:
    return "-" if value is None else f"{value:.{decimals}f}"


def pct(weight: float) -> str:
    return f"{round(weight * 100)}%"


def calc_assessment_grade(assessment: dict) -> Optional[float]:
    items = assessment.get("items", [])
    if not items:
        return None
    total_possible = sum(float(item.get("total", 0)) for item in items)
    total_earned = sum(float(item.get("score", 0)) for item in items)
    if total_possible <= 0:
        return None
    return total_earned / total_possible * 100


def calc_term_grade(assessments: list[dict]) -> Optional[float]:
    weighted_sum = 0.0
    total_weight = 0.0
    for assessment in assessments:
        grade = calc_assessment_grade(assessment)
        if grade is None:
            continue
        weighted_sum += grade * float(assessment.get("weight", 0))
        total_weight += float(assessment.get("weight", 0))
    if total_weight <= 0:
        return None
    return weighted_sum / total_weight


def calc_pass_probability(
    earned_pts: float,
    passing_grade: float,
    remaining_weight: float,
    trend: float = 0.0,
) -> int:
    if remaining_weight <= 0:
        return 97 if earned_pts >= passing_grade else 3
    max_possible_final = earned_pts + remaining_weight * 100
    if max_possible_final < passing_grade:
        return 2
    gap = passing_grade - earned_pts
    if gap <= 0:
        boost = min(8.0, (trend / 10.0) * 4.0)
        return min(99, round(91 + boost))
    required_average = gap / remaining_weight
    base_probability = 100 / (1 + math.exp((required_average - passing_grade) / 7.5))
    trend_adjustment = max(-12.0, min(12.0, trend * 0.8))
    probability = base_probability + trend_adjustment
    if required_average <= passing_grade - 20:
        probability = max(probability, 92)
    elif required_average <= passing_grade - 10:
        probability = max(probability, 82)
    return int(max(2, min(99, round(probability))))


def calc_subject_analytics(subject: dict) -> dict:
    terms = [
        {**term, "grade": calc_term_grade(term["assessments"])}
        for term in subject.get("terms", [])
    ]
    scored_terms = [term for term in terms if term["grade"] is not None]
    completed_w = sum(float(term.get("weight", 0)) for term in scored_terms)
    remaining_w = round(1.0 - completed_w, 10)
    earned_pts = sum(float(term["grade"]) * float(term.get("weight", 0)) for term in scored_terms)
    current_grade = earned_pts / completed_w if completed_w > 0 else None
    trend = 0.0
    if len(scored_terms) >= 2:
        trend = float(scored_terms[-1]["grade"]) - float(scored_terms[-2]["grade"])
    probability = None
    if current_grade is not None:
        probability = calc_pass_probability(
            earned_pts,
            float(subject.get("passing_grade", 75)),
            remaining_w,
            trend,
        )
    return {
        "terms": terms,
        "scored_terms": scored_terms,
        "completed_w": completed_w,
        "remaining_w": remaining_w,
        "earned_pts": earned_pts,
        "current_grade": current_grade,
        "trend": trend,
        "probability": probability,
    }


def forecast_required_score(
    earned_pts: float,
    target_grade: float,
    remaining_weight: float,
) -> dict:
    if remaining_weight <= 0:
        return {
            "required_score": None,
            "achievable": earned_pts >= target_grade,
            "note": "No remaining grade weight is available.",
        }
    required = (target_grade - earned_pts) / remaining_weight
    if required <= 0:
        note = "Target is already mathematically reached."
    elif required <= 100:
        note = f"Needs {required:.1f}/100 average in the remaining {pct(remaining_weight)}."
    else:
        note = f"Needs {required:.1f}/100, which is above the maximum possible score."
    return {
        "required_score": round(required, 1),
        "achievable": required <= 100,
        "note": note,
    }


def risk_info(probability: Optional[int]) -> dict:
    if probability is None:
        return {"level": "No data", "color": COLORS["muted"], "bg": "rgba(107,122,150,0.09)"}
    if probability >= 75:
        return {"level": "Low", "color": COLORS["green"], "bg": "rgba(28,155,115,0.10)"}
    if probability >= 50:
        return {"level": "Moderate", "color": COLORS["amber"], "bg": "rgba(201,131,22,0.12)"}
    if probability >= 25:
        return {"level": "High", "color": COLORS["orange"], "bg": "rgba(216,108,32,0.12)"}
    return {"level": "Critical", "color": COLORS["red"], "bg": "rgba(200,63,74,0.12)"}


def trend_label(trend: float) -> str:
    if trend > 5:
        return "Improving"
    if trend < -5:
        return "Declining"
    return "Stable"


FORECASTING_TOOL_PROMPT = """You are Forecasting Hive, a careful academic forecasting assistant.

You receive calculated forecasting context from the app. Use the numbers exactly.
Never invent subjects, grades, probabilities, or weights. If the data is
insufficient, state what is missing and what the student should enter.

You specialize in:
- Required average scores for remaining grade weight
- Passing risk and target-grade feasibility
- Priority ordering across subjects
- Practical study allocation based on calculated risk

Respond in this exact structure:

## Forecast
Give the direct answer using the calculated values.

## Why
Explain the calculation in plain language. Include formulas only when useful.

## Priority
State the highest-priority subject or action and why.

## Action Plan
Give exactly 3 practical next steps.

Rules:
- Do not guarantee outcomes.
- Do not use generic motivational filler.
- Do not recommend studying every subject equally unless the data supports it.
- If a required score is above 100, say the target is mathematically unreachable under the current entered data.
- Keep the answer concise and specific.
"""

SYSTEM_PROMPT = scoped_system_prompt(
    tool_name="Forecasting Hive",
    tool_scope=(
        "Academic forecasting, required-score calculation, passing probability, "
        "target-grade feasibility, grade risk analysis, and study priority planning."
    ),
    tool_prompt=FORECASTING_TOOL_PROMPT,
    refusal_message=(
        "This request is outside the scope of Forecasting Hive. I can only help "
        "with academic grade forecasting, required scores, and study priorities."
    ),
)


render_html(
    """
<style>
.fc-intro {
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(280px, 0.75fr);
  gap: 18px;
  margin-bottom: 22px;
}
.fc-hero,
.fc-side,
.fc-panel,
.fc-card {
  background: rgba(255,255,255,0.88);
  border: 1px solid rgba(0,56,115,0.11);
  border-radius: 16px;
  box-shadow: 0 18px 42px rgba(0,56,115,0.07);
}
.fc-hero {
  padding: 24px;
  background:
    linear-gradient(135deg,rgba(255,255,255,0.96),rgba(245,245,232,0.84)),
    linear-gradient(135deg,rgba(0,57,115,0.08),rgba(122,177,227,0.12));
}
.fc-kicker {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--navy-mid);
  margin-bottom: 8px;
}
.fc-title {
  font-family: var(--font-display);
  font-size: clamp(24px, 4vw, 38px);
  font-weight: 800;
  letter-spacing: 0;
  line-height: 1.05;
  color: var(--ink);
}
.fc-copy {
  color: var(--ink-muted);
  font-size: 14px;
  line-height: 1.7;
  margin-top: 10px;
}
.fc-side {
  padding: 20px;
}
.fc-side-row {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  padding: 11px 0;
  border-bottom: 1px solid rgba(0,56,115,0.08);
}
.fc-side-row:last-child {
  border-bottom: 0;
}
.fc-side-label {
  color: var(--ink-muted);
  font-size: 12px;
}
.fc-side-value {
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 600;
  color: var(--ink);
  white-space: nowrap;
}
.fc-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin: 16px 0 22px;
}
.fc-card {
  padding: 16px;
  min-height: 112px;
}
.fc-card-label {
  font-family: var(--font-mono);
  font-size: 9px;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: var(--ink-muted);
}
.fc-card-value {
  font-family: var(--font-display);
  font-size: 30px;
  font-weight: 800;
  color: var(--ink);
  line-height: 1;
  margin-top: 8px;
}
.fc-card-sub {
  color: var(--ink-muted);
  font-size: 12px;
  line-height: 1.5;
  margin-top: 8px;
}
.fc-panel {
  padding: 18px;
  margin: 16px 0;
}
.fc-section-title {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 800;
  color: var(--ink);
  margin: 22px 0 10px;
}
.fc-pill {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  border-radius: 999px;
  padding: 5px 10px;
  font-family: var(--font-mono);
  font-size: 9px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  border: 1px solid currentColor;
}
.fc-bubble {
  border-radius: 14px;
  padding: 14px 16px;
  margin: 10px 0;
  border: 1px solid rgba(0,56,115,0.10);
  line-height: 1.65;
}
.fc-user {
  background: rgba(0,86,163,0.07);
}
.fc-ai {
  background: white;
}
.fc-label {
  font-family: var(--font-mono);
  font-size: 9px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--navy-mid);
  margin-bottom: 6px;
}
@media (max-width: 980px) {
  .fc-intro {
    grid-template-columns: 1fr;
  }
  .fc-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
@media (max-width: 620px) {
  .fc-grid {
    grid-template-columns: 1fr;
  }
}
</style>
"""
)


def init_state() -> None:
    if "forecasting_chat_history" not in st.session_state:
        st.session_state.forecasting_chat_history = []


def gradewise_subjects() -> list[dict]:
    linked_subjects = st.session_state.get("gradewise_subjects")
    if linked_subjects:
        return list(linked_subjects)
    legacy_subjects = st.session_state.get("subjects")
    if legacy_subjects:
        return list(legacy_subjects)
    return []


def card(label: str, value: str, sub: str, color: str | None = None) -> str:
    value_color = color or COLORS["ink"]
    return f"""
    <div class="fc-card">
      <div class="fc-card-label">{_safe(label)}</div>
      <div class="fc-card-value" style="color:{value_color};">{_safe(value)}</div>
      <div class="fc-card-sub">{_safe(sub)}</div>
    </div>
    """


def render_intro(data_count: int) -> None:
    source_label = "Connected" if data_count else "Manual-ready"
    render_html(
        f"""
        <div class="fc-intro">
          <div class="fc-hero">
            <div class="fc-kicker">Academic Forecasting</div>
            <div class="fc-title">Forecasting Hive</div>
            <div class="fc-copy">
              Calculate what grade is still needed, test target-grade feasibility,
              and ask the local model for a focused priority plan based on the
              math already computed here.
            </div>
          </div>
          <div class="fc-side">
            <div class="fc-side-row">
              <span class="fc-side-label">GradeWise subjects</span>
              <span class="fc-side-value">{data_count}</span>
            </div>
            <div class="fc-side-row">
              <span class="fc-side-label">Forecast source</span>
              <span class="fc-side-value">{source_label}</span>
            </div>
            <div class="fc-side-row">
              <span class="fc-side-label">Model flow</span>
              <span class="fc-side-value">ToolHive local chat</span>
            </div>
          </div>
        </div>
        """
    )


def build_gradewise_context(selected_name: str, target_grade: float) -> list[dict]:
    source_subjects = gradewise_subjects()
    if selected_name != "All subjects":
        source_subjects = [
            subject for subject in source_subjects if subject.get("name") == selected_name
        ]
    context = []
    for subject in source_subjects:
        analytics = calc_subject_analytics(subject)
        required = forecast_required_score(
            analytics["earned_pts"],
            target_grade,
            analytics["remaining_w"],
        )
        risk = risk_info(analytics["probability"])
        context.append(
            {
                "source": "GradeWise",
                "subject": subject.get("name", "Untitled"),
                "passing_grade": subject.get("passing_grade", 75),
                "target_grade": target_grade,
                "current_grade": (
                    round(analytics["current_grade"], 1)
                    if analytics["current_grade"] is not None
                    else None
                ),
                "earned_points": round(analytics["earned_pts"], 2),
                "completed_weight_pct": round(analytics["completed_w"] * 100),
                "remaining_weight_pct": round(analytics["remaining_w"] * 100),
                "required_average_for_target": required["required_score"],
                "required_note": required["note"],
                "passing_probability": analytics["probability"],
                "risk_level": risk["level"],
                "trend": round(analytics["trend"], 1),
                "trend_label": trend_label(analytics["trend"]),
            }
        )
    return context


def build_manual_context(
    current_grade: float,
    completed_pct: float,
    target_grade: float,
    passing_grade: float,
    trend: float,
) -> list[dict]:
    completed_weight = completed_pct / 100
    remaining_weight = max(0.0, 1.0 - completed_weight)
    earned_pts = current_grade * completed_weight
    probability = calc_pass_probability(earned_pts, passing_grade, remaining_weight, trend)
    required = forecast_required_score(earned_pts, target_grade, remaining_weight)
    risk = risk_info(probability)
    return [
        {
            "source": "Manual scenario",
            "subject": "Manual forecast",
            "passing_grade": passing_grade,
            "target_grade": target_grade,
            "current_grade": current_grade,
            "earned_points": round(earned_pts, 2),
            "completed_weight_pct": round(completed_pct),
            "remaining_weight_pct": round(remaining_weight * 100),
            "required_average_for_target": required["required_score"],
            "required_note": required["note"],
            "passing_probability": probability,
            "risk_level": risk["level"],
            "trend": trend,
            "trend_label": trend_label(trend),
        }
    ]


def render_context_cards(context: list[dict]) -> None:
    if not context:
        st.info("No forecast context is available yet.")
        return

    if len(context) == 1:
        item = context[0]
        risk = risk_info(item.get("passing_probability"))
        render_html(
            '<div class="fc-grid">'
            + card("Current grade", fmt(item.get("current_grade")), item["subject"], COLORS["blue"])
            + card(
                "Required avg",
                fmt(item.get("required_average_for_target")),
                item.get("required_note", ""),
                COLORS["amber"]
                if (item.get("required_average_for_target") or 0) <= 100
                else COLORS["red"],
            )
            + card(
                "Pass probability",
                f"{item.get('passing_probability')}%",
                f"{risk['level']} risk",
                risk["color"],
            )
            + card(
                "Remaining",
                f"{item.get('remaining_weight_pct')}%",
                f"Completed {item.get('completed_weight_pct')}%",
            )
            + "</div>"
        )
        return

    rows = []
    for item in context:
        risk = risk_info(item.get("passing_probability"))
        required = item.get("required_average_for_target")
        rows.append(
            f"""
            <div class="fc-panel" style="margin:10px 0;">
              <div style="display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;">
                <div>
                  <div style="font-weight:800;color:var(--ink);">{_safe(item["subject"])}</div>
                  <div class="fc-card-sub">{_safe(item.get("required_note", ""))}</div>
                </div>
                <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;">
                  <span class="fc-card-value" style="font-size:20px;">{fmt(item.get("current_grade"))}</span>
                  <span class="fc-card-sub">Needs {fmt(required)}</span>
                  <span class="fc-pill" style="color:{risk["color"]};background:{risk["bg"]};">{risk["level"]}</span>
                </div>
              </div>
            </div>
            """
        )
    render_html("".join(rows))


def run_forecast_ai(question: str, context: list[dict]) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                "Calculated forecasting context:\n"
                f"{json.dumps(context, indent=2)}\n\n"
                f"User question: {question}"
            ),
        },
    ]
    return chat(messages)


QUICK_PROMPTS = [
    "What is the required score to reach my target?",
    "Which subject should I prioritize first?",
    "Is my target grade still realistic?",
    "Create a one-week study priority plan.",
]


def render_chat(context: list[dict]) -> None:
    render_html('<div class="fc-section-title">Ask Forecasting Hive</div>')
    prompt_cols = st.columns(4)
    for col, prompt in zip(prompt_cols, QUICK_PROMPTS):
        if col.button(prompt, key=f"fc_quick_{prompt}", width="stretch"):
            send_message(prompt, context)
            st.rerun()

    for message in st.session_state.forecasting_chat_history:
        role_class = "fc-user" if message["role"] == "user" else "fc-ai"
        label = "You" if message["role"] == "user" else "Forecasting Hive"
        render_html(
            f"""
            <div class="fc-bubble {role_class}">
              <div class="fc-label">{label}</div>
              <div>{_safe(message["content"]).replace(chr(10), "<br>")}</div>
            </div>
            """
        )

    input_col, ask_col, clear_col = st.columns([5, 1, 1], vertical_alignment="bottom")
    question = input_col.text_input(
        "Forecast question",
        placeholder="Ask about required scores, risk, targets, or priorities...",
        label_visibility="collapsed",
        key="fc_question",
    )
    if ask_col.button("Ask", width="stretch"):
        if question.strip():
            send_message(question.strip(), context)
            st.rerun()
        st.warning("Enter a question first.")
    if clear_col.button("Clear", width="stretch"):
        st.session_state.forecasting_chat_history = []
        st.rerun()


def send_message(question: str, context: list[dict]) -> None:
    st.session_state.forecasting_chat_history.append({"role": "user", "content": question})
    with st.spinner("Forecasting Hive is calculating and drafting..."):
        try:
            reply = run_forecast_ai(question, context)
        except Exception as exc:
            reply = f"Error: {exc}"
    st.session_state.forecasting_chat_history.append({"role": "assistant", "content": reply})


init_state()
gradewise_count = len(gradewise_subjects())

with tool_body_container():
    render_intro(gradewise_count)

    source_options = ["Manual scenario"]
    if gradewise_count:
        source_options.insert(0, "GradeWise data")

    source = st.segmented_control(
        "Forecast source",
        options=source_options,
        default=source_options[0],
    )

    context: list[dict]
    if source == "GradeWise data":
        names = ["All subjects"] + [subject["name"] for subject in gradewise_subjects()]
        col1, col2 = st.columns([2, 1])
        selected_name = col1.selectbox("Subject scope", names)
        target_grade = col2.number_input(
            "Target grade",
            min_value=0.0,
            max_value=100.0,
            value=75.0,
            step=0.5,
        )
        context = build_gradewise_context(selected_name, target_grade)
    else:
        col1, col2 = st.columns(2)
        with col1:
            current_grade = st.number_input(
                "Current running grade",
                min_value=0.0,
                max_value=100.0,
                value=78.0,
                step=0.5,
            )
            completed_pct = st.slider("Completed grade weight", 0.0, 100.0, 40.0, 5.0)
        with col2:
            passing_grade = st.number_input(
                "Passing grade",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
                step=0.5,
            )
            target_grade = st.number_input(
                "Target grade",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
                step=0.5,
                key="fc_manual_target",
            )
            trend = st.slider(
                "Recent trend",
                min_value=-30.0,
                max_value=30.0,
                value=0.0,
                step=1.0,
                help="Positive means recent scores are improving; negative means declining.",
            )
        context = build_manual_context(
            current_grade,
            completed_pct,
            target_grade,
            passing_grade,
            trend,
        )

    render_html('<div class="fc-section-title">Forecast Summary</div>')
    render_context_cards(context)
    render_chat(context)
