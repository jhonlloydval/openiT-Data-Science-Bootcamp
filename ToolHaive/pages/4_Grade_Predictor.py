"""
pages/4_Grade_Predictor.py - ToolHaive AI

GradeWise Hive replaces the original grade predictor placeholder.
This file is self-contained: data structures, calculations, dashboard,
grade entry, forecasting chat, and analytics all live here.
"""

from __future__ import annotations

import copy
import json
import math
import uuid
from typing import Optional

import streamlit as st

try:
    import plotly.graph_objects as go
except Exception:  # pragma: no cover - UI fallback only
    go = None

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
    page_title="GradeWise Hive - ToolHaive AI",
    page_icon="GW",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title="GradeWise Hive",
    subtitle="Track grades, calculate risk, forecast required scores, and review academic trends",
    cover_class="cv-4",
)


# ---------------------------------------------------------------------------
# Data model and calculation helpers
# ---------------------------------------------------------------------------

DEFAULT_TERMS = [
    {"id": "prelims", "name": "Prelims", "weight": 0.20},
    {"id": "midterm", "name": "Midterm", "weight": 0.20},
    {"id": "semis", "name": "Semi-Finals", "weight": 0.25},
    {"id": "finals", "name": "Finals", "weight": 0.35},
]

DEFAULT_ASSESSMENTS = [
    {"id": "quiz", "name": "Quiz", "weight": 0.30},
    {"id": "attendance", "name": "Attendance", "weight": 0.10},
    {"id": "project", "name": "Project", "weight": 0.30},
    {"id": "exam", "name": "Exam", "weight": 0.30},
]

COLORS = {
    "ink": "#0A1628",
    "navy": "#003973",
    "blue": "#0056A3",
    "sky": "#7AB1E3",
    "cream": "#E5E5BE",
    "cream_light": "#F5F5E8",
    "muted": "#6B7A96",
    "line": "rgba(0,56,115,0.12)",
    "green": "#1C9B73",
    "amber": "#C98316",
    "orange": "#D86C20",
    "red": "#C83F4A",
}


def _uid() -> str:
    return str(uuid.uuid4())[:8]


def create_subject(name: str, passing_grade: float = 75.0) -> dict:
    return {
        "id": _uid(),
        "name": name,
        "passing_grade": float(passing_grade),
        "terms": [
            {
                **term,
                "assessments": [{**assessment, "items": []} for assessment in DEFAULT_ASSESSMENTS],
            }
            for term in DEFAULT_TERMS
        ],
    }


def add_assessment_item(
    subject: dict,
    term_id: str,
    assessment_id: str,
    item_name: str,
    total: float,
    score: float,
) -> dict:
    updated = copy.deepcopy(subject)
    for term in updated["terms"]:
        if term["id"] != term_id:
            continue
        for assessment in term["assessments"]:
            if assessment["id"] == assessment_id:
                assessment["items"].append(
                    {
                        "id": _uid(),
                        "name": item_name,
                        "total": float(total),
                        "score": float(score),
                    }
                )
                return updated
    return updated


def delete_assessment_item(
    subject: dict,
    term_id: str,
    assessment_id: str,
    item_id: str,
) -> dict:
    updated = copy.deepcopy(subject)
    for term in updated["terms"]:
        if term["id"] != term_id:
            continue
        for assessment in term["assessments"]:
            if assessment["id"] == assessment_id:
                assessment["items"] = [
                    item for item in assessment["items"] if item["id"] != item_id
                ]
                return updated
    return updated


def item_percentage(item: dict) -> Optional[float]:
    total = float(item.get("total", 0))
    if total <= 0:
        return None
    return float(item.get("score", 0)) / total * 100


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
    logistic_midpoint = passing_grade
    base_probability = 100 / (1 + math.exp((required_average - logistic_midpoint) / 7.5))
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
        for term in subject["terms"]
    ]
    scored_terms = [term for term in terms if term["grade"] is not None]
    completed_w = sum(float(term["weight"]) for term in scored_terms)
    remaining_w = round(1.0 - completed_w, 10)
    earned_pts = sum(float(term["grade"]) * float(term["weight"]) for term in scored_terms)
    current_grade = earned_pts / completed_w if completed_w > 0 else None

    trend = 0.0
    if len(scored_terms) >= 2:
        trend = float(scored_terms[-1]["grade"]) - float(scored_terms[-2]["grade"])

    probability = None
    if current_grade is not None:
        probability = calc_pass_probability(
            earned_pts=earned_pts,
            passing_grade=float(subject["passing_grade"]),
            remaining_weight=remaining_w,
            trend=trend,
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
        note = "Target is already mathematically reached. Maintain steady performance."
    elif required <= 100:
        note = f"Needs {required:.1f}/100 average across the remaining {pct(remaining_weight)}."
    else:
        note = f"Needs {required:.1f}/100, which is above the maximum possible score."
    return {
        "required_score": round(required, 1),
        "achievable": required <= 100,
        "note": note,
    }


def explain_probability(
    earned_pts: float,
    passing_grade: float,
    remaining_weight: float,
    probability: Optional[int],
) -> str:
    if probability is None:
        return "No scored terms yet, so the probability cannot be computed."

    gap = passing_grade - earned_pts
    if remaining_weight <= 0:
        if earned_pts >= passing_grade:
            return "All terms are completed and the passing grade has been reached."
        return "All terms are completed, but the passing grade was not reached."

    if gap <= 0:
        return f"Already ahead by {abs(gap):.1f} points before the remaining work."

    if probability <= 2:
        max_possible = earned_pts + remaining_weight * 100
        return f"Even perfect remaining scores would only reach {max_possible:.1f}."

    required = gap / remaining_weight
    return f"Needs at least {required:.1f}/100 average in the remaining {pct(remaining_weight)}."


def get_risk_info(probability: Optional[int]) -> dict:
    if probability is None:
        return {"level": "No data", "color": COLORS["muted"], "bg": "rgba(107,122,150,0.09)"}
    if probability >= 75:
        return {"level": "Low", "color": COLORS["green"], "bg": "rgba(28,155,115,0.10)"}
    if probability >= 50:
        return {"level": "Moderate", "color": COLORS["amber"], "bg": "rgba(201,131,22,0.12)"}
    if probability >= 25:
        return {"level": "High", "color": COLORS["orange"], "bg": "rgba(216,108,32,0.12)"}
    return {"level": "Critical", "color": COLORS["red"], "bg": "rgba(200,63,74,0.12)"}


def grade_color(score: Optional[float], passing: float = 75.0) -> str:
    if score is None:
        return COLORS["muted"]
    if score >= passing:
        return COLORS["green"]
    if score >= passing - 5:
        return COLORS["amber"]
    return COLORS["red"]


def fmt(value: Optional[float], decimals: int = 1) -> str:
    return "-" if value is None else f"{value:.{decimals}f}"


def pct(weight: float) -> str:
    return f"{round(weight * 100)}%"


def gwa_to_grade(score: Optional[float]) -> str:
    if score is None:
        return "-"
    for threshold, gwa in [
        (97, "1.00"),
        (94, "1.25"),
        (91, "1.50"),
        (88, "1.75"),
        (85, "2.00"),
        (82, "2.25"),
        (79, "2.50"),
        (76, "2.75"),
        (75, "3.00"),
    ]:
        if score >= threshold:
            return gwa
    return "5.00"


def trend_label(trend: float) -> str:
    if trend > 5:
        return "Improving"
    if trend < -5:
        return "Declining"
    return "Stable"


def _safe(value) -> str:
    return escape_html(value)


def get_sample_subjects() -> list[dict]:
    def filled_subject(name: str, scores: dict, passing: float = 75.0) -> dict:
        subject = create_subject(name, passing)
        for term in subject["terms"]:
            term_scores = scores.get(term["id"], {})
            for assessment in term["assessments"]:
                score = term_scores.get(assessment["id"])
                if score is not None:
                    assessment["items"].append(
                        {
                            "id": _uid(),
                            "name": f"{assessment['name']} score",
                            "total": 100.0,
                            "score": float(score),
                        }
                    )
        return subject

    return [
        filled_subject(
            "Calculus",
            {
                "prelims": {"quiz": 92, "attendance": 100, "project": 88, "exam": 90},
                "midterm": {"quiz": 88, "attendance": 100, "project": 91, "exam": 93},
            },
        ),
        filled_subject(
            "Programming",
            {
                "prelims": {"quiz": 80, "attendance": 95, "project": 82, "exam": 78},
                "midterm": {"quiz": 75, "attendance": 90, "project": 77, "exam": 76},
                "semis": {"quiz": 72, "attendance": 88, "project": 74},
            },
        ),
        filled_subject(
            "Physics",
            {
                "prelims": {"quiz": 68, "attendance": 80, "project": 70, "exam": 65},
                "midterm": {"quiz": 64, "attendance": 75, "project": 68, "exam": 62},
            },
        ),
        filled_subject(
            "Electronics",
            {
                "prelims": {"quiz": 55, "attendance": 70, "project": 60, "exam": 58},
                "midterm": {"quiz": 52, "attendance": 65, "project": 57, "exam": 50},
                "semis": {"quiz": 54, "attendance": 68, "project": 59, "exam": 53},
            },
        ),
    ]


def init_state() -> None:
    if "gradewise_subjects" not in st.session_state:
        st.session_state.gradewise_subjects = []
    if "gradewise_active_subject_idx" not in st.session_state:
        st.session_state.gradewise_active_subject_idx = 0
    if "gradewise_chat_history" not in st.session_state:
        st.session_state.gradewise_chat_history = []


def subjects() -> list[dict]:
    return st.session_state.gradewise_subjects


def clamp_active_index() -> None:
    if not subjects():
        st.session_state.gradewise_active_subject_idx = 0
        return
    st.session_state.gradewise_active_subject_idx = max(
        0,
        min(st.session_state.gradewise_active_subject_idx, len(subjects()) - 1),
    )


def load_samples() -> None:
    st.session_state.gradewise_subjects = get_sample_subjects()
    st.session_state.gradewise_active_subject_idx = 0
    st.session_state.gradewise_chat_history = []


# Keep a legacy alias for the standalone Forecasting Hive and older sessions.
init_state()
st.session_state.subjects = st.session_state.gradewise_subjects


# ---------------------------------------------------------------------------
# AI forecasting prompt
# ---------------------------------------------------------------------------

GRADEWISE_TOOL_PROMPT = """You are GradeWise Hive, an academic forecasting assistant.

You receive calculated grade analytics from the app. Use those numbers exactly.
Do not invent scores, subjects, weights, or probabilities. If a value is missing,
say it is missing and explain what the student should enter next.

Default grading context:
- Prelims: 20%
- Midterm: 20%
- Semi-Finals: 25%
- Finals: 35%
- Passing grade is subject-specific, usually 75.

Respond in this exact structure:

## Direct Answer
Answer the student's question in 2-4 sentences using the available numbers.

## Calculations Used
List the relevant formulas or computed values. Keep this short and transparent.

## Risk Signals
Name the strongest positive signal and strongest risk signal.

## Next Action
Give exactly 3 practical actions, ordered by priority.

Rules:
- Be warm but not motivational filler.
- Never guarantee a final grade.
- Use "likely", "at risk", or "mathematically needs" when appropriate.
- If the request asks for a score needed to pass or hit a target, compute it from earned points and remaining weight.
- If the student has no entered scores, ask them to add at least one scored item first.
"""

GRADEWISE_SYSTEM_PROMPT = scoped_system_prompt(
    tool_name="GradeWise Hive",
    tool_scope=(
        "Academic grade tracking, weighted grade calculations, passing risk, "
        "required-score forecasting, subject prioritization, and study planning."
    ),
    tool_prompt=GRADEWISE_TOOL_PROMPT,
    refusal_message=(
        "This request is outside the scope of GradeWise Hive. I can only help "
        "with academic grade tracking, grade forecasting, and study planning."
    ),
)


def build_forecast_summary() -> list[dict]:
    summary = []
    for subject in subjects():
        analytics = calc_subject_analytics(subject)
        required = forecast_required_score(
            analytics["earned_pts"],
            float(subject["passing_grade"]),
            analytics["remaining_w"],
        )
        summary.append(
            {
                "subject": subject["name"],
                "passing_grade": subject["passing_grade"],
                "current_grade": (
                    round(analytics["current_grade"], 1)
                    if analytics["current_grade"] is not None
                    else None
                ),
                "earned_points": round(analytics["earned_pts"], 2),
                "completed_weight_pct": round(analytics["completed_w"] * 100),
                "remaining_weight_pct": round(analytics["remaining_w"] * 100),
                "passing_probability": analytics["probability"],
                "risk_level": get_risk_info(analytics["probability"])["level"],
                "trend": round(analytics["trend"], 1),
                "trend_label": trend_label(analytics["trend"]),
                "required_average_to_pass": required["required_score"],
                "required_average_note": required["note"],
                "terms": [
                    {
                        "name": term["name"],
                        "weight_pct": round(float(term["weight"]) * 100),
                        "grade": round(term["grade"], 1) if term["grade"] is not None else None,
                    }
                    for term in analytics["terms"]
                ],
            }
        )
    return summary


def run_gradewise_ai(user_message: str) -> str:
    messages = [
        {"role": "system", "content": GRADEWISE_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                "Calculated GradeWise data:\n"
                f"{json.dumps(build_forecast_summary(), indent=2)}\n\n"
                f"Student question: {user_message}"
            ),
        },
    ]
    return chat(messages)


# ---------------------------------------------------------------------------
# UI styling
# ---------------------------------------------------------------------------

render_html(
    """
<style>
.gw-shell {
  width: 100%;
}
.gw-intro {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(280px, 0.65fr);
  gap: 20px;
  align-items: stretch;
  margin-bottom: 24px;
}
.gw-intro-main,
.gw-intro-side,
.gw-panel {
  background: rgba(255,255,255,0.86);
  border: 1px solid rgba(0,56,115,0.11);
  border-radius: 16px;
  box-shadow: 0 18px 42px rgba(0,56,115,0.07);
}
.gw-intro-main {
  padding: 24px;
  background:
    linear-gradient(135deg,rgba(255,255,255,0.96),rgba(245,245,232,0.84)),
    linear-gradient(135deg,rgba(0,57,115,0.08),rgba(122,177,227,0.12));
}
.gw-kicker {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--navy-mid);
  margin-bottom: 8px;
}
.gw-title {
  font-family: var(--font-display);
  font-size: clamp(24px, 4vw, 38px);
  font-weight: 800;
  letter-spacing: 0;
  color: var(--ink);
  line-height: 1.05;
}
.gw-copy {
  color: var(--ink-muted);
  font-size: 14px;
  line-height: 1.7;
  margin-top: 10px;
  max-width: 760px;
}
.gw-intro-side {
  padding: 20px;
}
.gw-side-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 11px 0;
  border-bottom: 1px solid rgba(0,56,115,0.08);
}
.gw-side-row:last-child {
  border-bottom: 0;
}
.gw-side-label {
  font-size: 12px;
  color: var(--ink-muted);
}
.gw-side-value {
  font-family: var(--font-mono);
  font-size: 13px;
  color: var(--ink);
  font-weight: 600;
  white-space: nowrap;
}
.gw-metric-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin: 16px 0 22px;
}
.gw-metric {
  background: white;
  border: 1px solid rgba(0,56,115,0.10);
  border-radius: 14px;
  padding: 16px;
  min-height: 112px;
}
.gw-metric-label {
  font-family: var(--font-mono);
  font-size: 9px;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: var(--ink-muted);
}
.gw-metric-value {
  font-family: var(--font-display);
  font-size: 30px;
  font-weight: 800;
  color: var(--ink);
  margin-top: 8px;
  line-height: 1;
}
.gw-metric-sub {
  color: var(--ink-muted);
  font-size: 12px;
  line-height: 1.5;
  margin-top: 8px;
}
.gw-section-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin: 24px 0 12px;
}
.gw-section-title h3 {
  font-family: var(--font-display);
  font-size: 18px;
  margin: 0;
  color: var(--ink);
}
.gw-section-note {
  color: var(--ink-muted);
  font-size: 12px;
  line-height: 1.5;
}
.gw-table {
  overflow: hidden;
  border: 1px solid rgba(0,56,115,0.10);
  border-radius: 14px;
  background: white;
}
.gw-row {
  display: grid;
  grid-template-columns: 1.5fr repeat(4, 1fr);
  gap: 12px;
  align-items: center;
  padding: 13px 16px;
  border-bottom: 1px solid rgba(0,56,115,0.07);
}
.gw-row:last-child {
  border-bottom: 0;
}
.gw-head {
  background: rgba(0,56,115,0.04);
  font-family: var(--font-mono);
  font-size: 9px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--ink-muted);
}
.gw-subject-name {
  font-weight: 700;
  color: var(--ink);
}
.gw-mono {
  font-family: var(--font-mono);
  font-size: 12px;
}
.gw-pill {
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
.gw-empty {
  background: white;
  border: 1px dashed rgba(0,86,163,0.25);
  border-radius: 16px;
  padding: 28px;
  color: var(--ink-muted);
  line-height: 1.7;
}
.gw-item-head {
  display: grid;
  grid-template-columns: 2fr 0.8fr 0.8fr 0.9fr 0.7fr;
  gap: 10px;
  padding: 9px 0 6px;
  font-family: var(--font-mono);
  font-size: 9px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--ink-muted);
  border-bottom: 1px solid rgba(0,56,115,0.08);
}
.gw-chat-empty {
  border: 1px solid rgba(0,56,115,0.10);
  background:
    linear-gradient(135deg,rgba(255,255,255,0.94),rgba(245,245,232,0.78)),
    linear-gradient(135deg,rgba(0,57,115,0.05),rgba(122,177,227,0.10));
  border-radius: 16px;
  padding: 26px;
  color: var(--ink-muted);
  line-height: 1.7;
  margin-bottom: 16px;
}
.gw-chat-bubble {
  border-radius: 14px;
  padding: 14px 16px;
  margin: 10px 0;
  border: 1px solid rgba(0,56,115,0.10);
  line-height: 1.65;
}
.gw-chat-user {
  background: rgba(0,86,163,0.07);
}
.gw-chat-ai {
  background: white;
}
.gw-chat-label {
  font-family: var(--font-mono);
  font-size: 9px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--navy-mid);
  margin-bottom: 6px;
}
.gw-risk-card {
  background: white;
  border: 1px solid rgba(0,56,115,0.10);
  border-radius: 14px;
  padding: 16px;
  margin-bottom: 12px;
}
.gw-risk-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}
.gw-bar {
  height: 8px;
  border-radius: 99px;
  background: rgba(10,22,40,0.08);
  overflow: hidden;
  margin-top: 12px;
}
.gw-bar span {
  display: block;
  height: 100%;
  border-radius: inherit;
}
@media (max-width: 980px) {
  .gw-intro {
    grid-template-columns: 1fr;
  }
  .gw-metric-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .gw-row {
    grid-template-columns: 1.3fr repeat(2, 1fr);
  }
  .gw-row > :nth-child(4),
  .gw-row > :nth-child(5) {
    display: none;
  }
}
@media (max-width: 620px) {
  .gw-metric-grid {
    grid-template-columns: 1fr;
  }
  .gw-row {
    grid-template-columns: 1fr;
  }
  .gw-row > * {
    min-width: 0;
  }
  .gw-head {
    display: none;
  }
}
</style>
"""
)


# ---------------------------------------------------------------------------
# Shared rendering helpers
# ---------------------------------------------------------------------------

def metric_card(label: str, value: str, sub: str, color: str | None = None) -> str:
    value_color = color or COLORS["ink"]
    return f"""
    <div class="gw-metric">
      <div class="gw-metric-label">{_safe(label)}</div>
      <div class="gw-metric-value" style="color:{value_color};">{_safe(value)}</div>
      <div class="gw-metric-sub">{_safe(sub)}</div>
    </div>
    """


def risk_pill(risk: dict) -> str:
    return (
        f'<span class="gw-pill" style="color:{risk["color"]};'
        f'background:{risk["bg"]};">{_safe(risk["level"])}</span>'
    )


def render_intro() -> None:
    total_subjects = len(subjects())
    analytics = [calc_subject_analytics(subject) for subject in subjects()]
    graded = [a for a in analytics if a["current_grade"] is not None]
    avg_grade = (
        sum(float(a["current_grade"]) for a in graded) / len(graded)
        if graded
        else None
    )
    highest_risk = "-"
    if graded:
        ranked = sorted(
            zip(subjects(), analytics),
            key=lambda pair: pair[1]["probability"] if pair[1]["probability"] is not None else 101,
        )
        highest_risk = ranked[0][0]["name"]

    render_html(
        f"""
        <div class="gw-intro">
          <div class="gw-intro-main">
            <div class="gw-kicker">Academic Intelligence</div>
            <div class="gw-title">GradeWise</div>
            <div class="gw-copy">
              Manage subjects, enter itemized scores, calculate weighted grades,
              and forecast what each course needs next. Built into ToolHaive's
              local AI workflow with transparent grade math.
            </div>
          </div>
          <div class="gw-intro-side">
            <div class="gw-side-row">
              <span class="gw-side-label">Subjects tracked</span>
              <span class="gw-side-value">{total_subjects}</span>
            </div>
            <div class="gw-side-row">
              <span class="gw-side-label">Average current grade</span>
              <span class="gw-side-value">{fmt(avg_grade)}</span>
            </div>
            <div class="gw-side-row">
              <span class="gw-side-label">Highest priority</span>
              <span class="gw-side-value">{_safe(highest_risk)}</span>
            </div>
          </div>
        </div>
        """
    )


def render_no_subjects(key_suffix: str) -> None:
    render_html(
        """
        <div class="gw-empty">
          Add a subject in the Grade Entry tab to begin. You can also load a
          demo set to preview the dashboard, forecasting, and analytics.
        </div>
        """
    )
    if st.button("Load Demo Subjects", key=f"gw_load_demo_empty_{key_suffix}"):
        load_samples()
        st.rerun()


def plotly_available() -> bool:
    if go is None:
        st.warning("Plotly is not installed, so charts are hidden.")
        return False
    return True


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

def render_dashboard() -> None:
    if not subjects():
        render_no_subjects("dashboard")
        return

    clamp_active_index()
    analytics = [calc_subject_analytics(subject) for subject in subjects()]
    graded = [
        (subject, analysis)
        for subject, analysis in zip(subjects(), analytics)
        if analysis["current_grade"] is not None
    ]
    passing_count = sum(
        1 for subject, analysis in graded if analysis["current_grade"] >= subject["passing_grade"]
    )
    avg_probability = (
        sum(analysis["probability"] for _, analysis in graded if analysis["probability"] is not None)
        / len(graded)
        if graded
        else None
    )
    at_risk = sum(
        1
        for analysis in analytics
        if analysis["probability"] is not None and analysis["probability"] < 50
    )

    render_html(
        '<div class="gw-metric-grid">'
        + metric_card("Total subjects", str(len(subjects())), "Courses currently tracked")
        + metric_card(
            "Passing now",
            f"{passing_count}/{len(graded)}" if graded else "-",
            "Based on current weighted grade",
            COLORS["green"] if passing_count == len(graded) and graded else COLORS["ink"],
        )
        + metric_card(
            "Avg pass probability",
            f"{avg_probability:.0f}%" if avg_probability is not None else "-",
            "Weighted-distance forecast",
            COLORS["blue"],
        )
        + metric_card(
            "At-risk subjects",
            str(at_risk),
            "Below 50% pass probability",
            COLORS["red"] if at_risk else COLORS["green"],
        )
        + "</div>"
    )

    names = [subject["name"] for subject in subjects()]
    active_idx = min(st.session_state.gradewise_active_subject_idx, len(names) - 1)
    selected = st.selectbox(
        "Active subject",
        names,
        index=active_idx,
        key="gw_dashboard_subject",
    )
    subject_idx = names.index(selected)
    st.session_state.gradewise_active_subject_idx = subject_idx
    subject = subjects()[subject_idx]
    analysis = calc_subject_analytics(subject)
    risk = get_risk_info(analysis["probability"])
    required = forecast_required_score(
        analysis["earned_pts"],
        float(subject["passing_grade"]),
        analysis["remaining_w"],
    )

    render_html(
        f"""
        <div class="gw-section-title">
          <h3>{_safe(subject["name"])}</h3>
          <div class="gw-section-note">
            Passing: {fmt(subject["passing_grade"])} |
            Completed: {pct(analysis["completed_w"])} |
            Remaining: {pct(analysis["remaining_w"])}
          </div>
        </div>
        <div class="gw-metric-grid">
          {metric_card("Current grade", fmt(analysis["current_grade"]), "Normalized across scored terms", grade_color(analysis["current_grade"], subject["passing_grade"]))}
          {metric_card("Pass probability", f'{analysis["probability"]}%' if analysis["probability"] is not None else "-", f'{risk["level"]} risk', risk["color"])}
          {metric_card("Required to pass", fmt(required["required_score"]), required["note"], COLORS["amber"] if required["achievable"] else COLORS["red"])}
          {metric_card("GWA equivalent", gwa_to_grade(analysis["current_grade"]), "Approximate PH-style equivalent")}
        </div>
        """
    )

    if analysis["probability"] is not None:
        render_html(
            f"""
            <div class="gw-risk-card">
              <div class="gw-risk-top">
                <div>
                  <div class="gw-kicker">Passing Likelihood</div>
                  <div style="font-weight:700;color:var(--ink);">
                    {explain_probability(analysis["earned_pts"], subject["passing_grade"], analysis["remaining_w"], analysis["probability"])}
                  </div>
                </div>
                {risk_pill(risk)}
              </div>
              <div class="gw-bar">
                <span style="width:{analysis["probability"]}%;background:{risk["color"]};"></span>
              </div>
            </div>
            """
        )

    scored = [(term["name"], term["grade"]) for term in analysis["terms"] if term["grade"] is not None]
    if scored and plotly_available():
        term_names, grades = zip(*scored)
        fig = go.Figure(
            go.Bar(
                x=list(term_names),
                y=list(grades),
                marker_color=[
                    grade_color(grade, subject["passing_grade"]) for grade in grades
                ],
                text=[f"{grade:.1f}" for grade in grades],
                textposition="outside",
            )
        )
        fig.add_hline(
            y=subject["passing_grade"],
            line_dash="dot",
            line_color=COLORS["amber"],
            annotation_text=f"Passing: {subject['passing_grade']}",
        )
        fig.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=24, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.72)",
            font=dict(family="DM Sans", color=COLORS["ink"]),
            yaxis=dict(range=[0, 105], gridcolor="rgba(0,56,115,0.10)"),
            xaxis=dict(showgrid=False),
            showlegend=False,
        )
        st.plotly_chart(fig, width="stretch")

    render_all_subjects_table(analytics)


def render_all_subjects_table(analytics: list[dict]) -> None:
    rows = [
        """
        <div class="gw-row gw-head">
          <div>Subject</div><div>Grade</div><div>Probability</div><div>Risk</div><div>Remaining</div>
        </div>
        """
    ]
    for subject, analysis in zip(subjects(), analytics):
        risk = get_risk_info(analysis["probability"])
        probability = f"{analysis['probability']}%" if analysis["probability"] is not None else "-"
        rows.append(
            f"""
            <div class="gw-row">
              <div class="gw-subject-name">{_safe(subject["name"])}</div>
              <div class="gw-mono" style="color:{grade_color(analysis["current_grade"], subject["passing_grade"])};">{fmt(analysis["current_grade"])}</div>
              <div class="gw-mono" style="color:{risk["color"]};">{probability}</div>
              <div>{risk_pill(risk)}</div>
              <div class="gw-mono">{pct(analysis["remaining_w"])}</div>
            </div>
            """
        )

    render_html(
        f"""
        <div class="gw-section-title">
          <h3>All Subjects</h3>
          <div class="gw-section-note">Risk is based on remaining weight, earned points, and trend.</div>
        </div>
        <div class="gw-table">{''.join(rows)}</div>
        """
    )


# ---------------------------------------------------------------------------
# Grade entry
# ---------------------------------------------------------------------------

def render_grade_entry() -> None:
    manage_tab, scores_tab = st.tabs(["Manage Subjects", "Enter Scores"])

    with manage_tab:
        render_html(
            """
            <div class="gw-section-title">
              <h3>Add Subject</h3>
              <div class="gw-section-note">Default term weights follow Prelims, Midterm, Semi-Finals, and Finals.</div>
            </div>
            """
        )
        with st.form("gw_add_subject_form", clear_on_submit=True):
            c1, c2, c3 = st.columns([2.5, 1, 1], vertical_alignment="bottom")
            name = c1.text_input("Subject name", placeholder="e.g. Data Structures")
            passing = c2.number_input(
                "Passing grade",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
                step=0.5,
            )
            submitted = c3.form_submit_button("Add Subject", width="stretch")
            if submitted:
                cleaned = name.strip()
                if not cleaned:
                    st.error("Enter a subject name.")
                elif any(subject["name"].lower() == cleaned.lower() for subject in subjects()):
                    st.error(f'"{cleaned}" already exists.')
                else:
                    st.session_state.gradewise_subjects.append(create_subject(cleaned, passing))
                    st.session_state.subjects = st.session_state.gradewise_subjects
                    st.success(f'Added "{cleaned}".')
                    st.rerun()

        action_1, action_2 = st.columns([1, 4])
        with action_1:
            if st.button("Load Demo Subjects", key="gw_load_demo_manage", width="stretch"):
                load_samples()
                st.rerun()
        with action_2:
            st.caption("Demo subjects replace the current GradeWise list.")

        if not subjects():
            render_no_subjects("manage")
        else:
            render_html(
                """
                <div class="gw-section-title">
                  <h3>Your Subjects</h3>
                  <div class="gw-section-note">Deleting a subject removes its entered scores from this session.</div>
                </div>
                """
            )
            header = st.columns([2.4, 1, 1, 0.8])
            for col, label in zip(header, ["Subject", "Passing", "Terms scored", ""]):
                col.caption(label)
            for idx, subject in enumerate(list(subjects())):
                analysis = calc_subject_analytics(subject)
                row = st.columns([2.4, 1, 1, 0.8], vertical_alignment="center")
                row[0].markdown(f"**{_safe(subject['name'])}**", unsafe_allow_html=True)
                row[1].markdown(fmt(subject["passing_grade"]))
                row[2].markdown(f"{len(analysis['scored_terms'])} / {len(subject['terms'])}")
                if row[3].button("Delete", key=f"gw_delete_subject_{subject['id']}"):
                    st.session_state.gradewise_subjects.pop(idx)
                    clamp_active_index()
                    st.session_state.subjects = st.session_state.gradewise_subjects
                    st.rerun()

    with scores_tab:
        if not subjects():
            render_no_subjects("scores")
            return

        names = [subject["name"] for subject in subjects()]
        active_idx = min(st.session_state.gradewise_active_subject_idx, len(names) - 1)
        selected = st.selectbox(
            "Subject",
            names,
            index=active_idx,
            key="gw_score_subject",
        )
        subject_idx = names.index(selected)
        st.session_state.gradewise_active_subject_idx = subject_idx
        subject = subjects()[subject_idx]
        st.caption(
            f"Passing grade: {fmt(subject['passing_grade'])}. Enter scored items; "
            "term, category, and final analytics update automatically."
        )

        for term in subject["terms"]:
            render_term(term, subject_idx, float(subject["passing_grade"]))


def render_term(term: dict, subject_idx: int, passing_grade: float) -> None:
    term_grade = calc_term_grade(term["assessments"])
    grade_label = fmt(term_grade)
    has_items = any(assessment.get("items") for assessment in term["assessments"])
    with st.expander(
        f"{term['name']} - {pct(term['weight'])} weight | Grade: {grade_label}",
        expanded=has_items,
    ):
        for assessment in term["assessments"]:
            category_grade = calc_assessment_grade(assessment)
            category_color = grade_color(category_grade, passing_grade)
            render_html(
                f"""
                <div class="gw-section-title" style="margin:16px 0 8px;">
                  <h3 style="font-size:15px;">{_safe(assessment["name"])}</h3>
                  <div class="gw-section-note">
                    Weight: {pct(assessment["weight"])} |
                    Grade:
                    <span class="gw-mono" style="color:{category_color};font-weight:700;">
                      {fmt(category_grade)}
                    </span>
                  </div>
                </div>
                """
            )
            render_item_table(assessment, term["id"], subject_idx, passing_grade)

        if term_grade is not None:
            color = grade_color(term_grade, passing_grade)
            render_html(
                f"""
                <div class="gw-risk-card" style="margin-top:16px;">
                  <div class="gw-risk-top">
                    <div>
                      <div class="gw-kicker">Term Grade</div>
                      <div class="gw-metric-value" style="font-size:24px;color:{color};">{fmt(term_grade)}</div>
                    </div>
                    <div class="gw-section-note">{term["name"]} contributes {pct(term["weight"])} of the final grade.</div>
                  </div>
                  <div class="gw-bar">
                    <span style="width:{min(100, max(0, term_grade))}%;background:{color};"></span>
                  </div>
                </div>
                """
            )


def render_item_table(
    assessment: dict,
    term_id: str,
    subject_idx: int,
    passing_grade: float,
) -> None:
    items = assessment.get("items", [])
    if items:
        render_html(
            """
            <div class="gw-item-head">
              <div>Item</div><div>Total</div><div>Score</div><div>Percent</div><div></div>
            </div>
            """
        )
        for item in items:
            item_pct = item_percentage(item)
            color = grade_color(item_pct, passing_grade)
            row = st.columns([2.0, 0.8, 0.8, 0.9, 0.7], vertical_alignment="center")
            row[0].markdown(_safe(item["name"]), unsafe_allow_html=True)
            row[1].markdown(f"`{item['total']:.1f}`")
            row[2].markdown(f"`{item['score']:.1f}`")
            row[3].markdown(
                f"<span class='gw-mono' style='font-weight:700;color:{color};'>{fmt(item_pct)}%</span>",
                unsafe_allow_html=True,
            )
            if row[4].button("Remove", key=f"gw_remove_{item['id']}"):
                current_subject = subjects()[subject_idx]
                st.session_state.gradewise_subjects[subject_idx] = delete_assessment_item(
                    current_subject,
                    term_id,
                    assessment["id"],
                    item["id"],
                )
                st.session_state.subjects = st.session_state.gradewise_subjects
                st.rerun()
    else:
        st.caption("No items yet for this category.")

    form_key = f"gw_add_{subjects()[subject_idx]['id']}_{term_id}_{assessment['id']}"
    with st.form(form_key, clear_on_submit=True):
        c1, c2, c3, c4 = st.columns([2.4, 1, 1, 0.9], vertical_alignment="bottom")
        item_name = c1.text_input(
            "Item name",
            placeholder=f"{assessment['name']} 1",
            key=f"{form_key}_name",
        )
        total_points = c2.number_input(
            "Total",
            min_value=0.5,
            max_value=10000.0,
            value=100.0,
            step=0.5,
            key=f"{form_key}_total",
        )
        score_points = c3.number_input(
            "Score",
            min_value=0.0,
            max_value=10000.0,
            value=0.0,
            step=0.5,
            key=f"{form_key}_score",
        )
        submitted = c4.form_submit_button("Add", width="stretch")
        if submitted:
            cleaned = item_name.strip()
            if not cleaned:
                st.error("Enter an item name.")
            elif score_points > total_points:
                st.error("Score cannot exceed total points.")
            else:
                current_subject = subjects()[subject_idx]
                st.session_state.gradewise_subjects[subject_idx] = add_assessment_item(
                    current_subject,
                    term_id,
                    assessment["id"],
                    cleaned,
                    total_points,
                    score_points,
                )
                st.session_state.subjects = st.session_state.gradewise_subjects
                st.rerun()


# ---------------------------------------------------------------------------
# Forecasting chat
# ---------------------------------------------------------------------------

QUICK_PROMPTS = [
    "What score do I need to pass all subjects?",
    "Which subject is most at risk and why?",
    "Predict my final grade if I maintain this performance.",
    "Give me a study priority plan.",
]


def render_forecasting() -> None:
    if not subjects():
        render_no_subjects("forecasting")
        return

    if not st.session_state.gradewise_chat_history:
        render_html(
            """
            <div class="gw-chat-empty">
              Ask GradeWise about required scores, risk, target grades, or which
              subject deserves attention first. The answer uses the calculated
              grades from your entered subjects.
            </div>
            """
        )

    if len(st.session_state.gradewise_chat_history) < 2:
        q_cols = st.columns(4)
        for col, prompt in zip(q_cols, QUICK_PROMPTS):
            if col.button(prompt, key=f"gw_quick_{prompt}", width="stretch"):
                send_forecast_message(prompt)
                st.rerun()

    for message in st.session_state.gradewise_chat_history:
        role_class = "gw-chat-user" if message["role"] == "user" else "gw-chat-ai"
        label = "You" if message["role"] == "user" else "GradeWise AI"
        render_html(
            f"""
            <div class="gw-chat-bubble {role_class}">
              <div class="gw-chat-label">{label}</div>
              <div>{_safe(message["content"]).replace(chr(10), "<br>")}</div>
            </div>
            """
        )

    input_col, send_col, clear_col = st.columns([5, 1, 1], vertical_alignment="bottom")
    user_input = input_col.text_input(
        "Ask about your grades",
        placeholder="Ask about risks, required scores, target grades, or study priority...",
        key="gw_forecast_input",
        label_visibility="collapsed",
    )
    if send_col.button("Ask", width="stretch"):
        if user_input.strip():
            send_forecast_message(user_input.strip())
            st.rerun()
        st.warning("Enter a question first.")
    if clear_col.button("Clear", width="stretch"):
        st.session_state.gradewise_chat_history = []
        st.rerun()


def send_forecast_message(message: str) -> None:
    st.session_state.gradewise_chat_history.append({"role": "user", "content": message})
    with st.spinner("GradeWise is calculating and drafting a response..."):
        try:
            reply = run_gradewise_ai(message)
        except Exception as exc:
            reply = f"Error: {exc}"
    st.session_state.gradewise_chat_history.append({"role": "assistant", "content": reply})


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------

def render_analytics() -> None:
    if not subjects():
        render_no_subjects("analytics")
        return

    trends_tab, detail_tab, categories_tab, risk_tab = st.tabs(
        ["Trends", "Subject Detail", "Category Radar", "Risk Map"]
    )

    with trends_tab:
        render_trends()
    with detail_tab:
        render_subject_detail()
    with categories_tab:
        render_category_radar()
    with risk_tab:
        render_risk_map()


def render_trends() -> None:
    if not plotly_available():
        return
    fig = go.Figure()
    any_points = False
    for subject in subjects():
        analysis = calc_subject_analytics(subject)
        points = [
            (term["name"], round(term["grade"], 1))
            for term in analysis["terms"]
            if term["grade"] is not None
        ]
        if not points:
            continue
        any_points = True
        x_values, y_values = zip(*points)
        fig.add_trace(
            go.Scatter(
                x=list(x_values),
                y=list(y_values),
                name=subject["name"],
                mode="lines+markers+text",
                text=[str(value) for value in y_values],
                textposition="top center",
                marker=dict(size=8),
                line=dict(width=2.6),
            )
        )

    if not any_points:
        st.info("Enter scores to see trend lines.")
        return

    fig.update_layout(
        height=340,
        margin=dict(l=10, r=10, t=28, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.78)",
        font=dict(family="DM Sans", color=COLORS["ink"]),
        yaxis=dict(range=[0, 105], gridcolor="rgba(0,56,115,0.10)", title="Grade"),
        xaxis=dict(showgrid=False),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig, width="stretch")


def render_subject_detail() -> None:
    if not plotly_available():
        return
    names = [subject["name"] for subject in subjects()]
    selected = st.selectbox(
        "Subject",
        names,
        index=min(st.session_state.gradewise_active_subject_idx, len(names) - 1),
        key="gw_detail_subject",
    )
    subject = subjects()[names.index(selected)]
    analysis = calc_subject_analytics(subject)
    risk = get_risk_info(analysis["probability"])

    if analysis["probability"] is not None:
        fig_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=analysis["probability"],
                title={"text": "Passing Probability"},
                number={"suffix": "%", "font": {"color": risk["color"], "size": 34}},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": risk["color"]},
                    "bgcolor": "rgba(255,255,255,0.8)",
                    "steps": [
                        {"range": [0, 25], "color": "rgba(200,63,74,0.12)"},
                        {"range": [25, 50], "color": "rgba(216,108,32,0.12)"},
                        {"range": [50, 75], "color": "rgba(201,131,22,0.12)"},
                        {"range": [75, 100], "color": "rgba(28,155,115,0.12)"},
                    ],
                    "threshold": {
                        "line": {"color": COLORS["amber"], "width": 2},
                        "thickness": 0.75,
                        "value": 75,
                    },
                },
            )
        )
        fig_gauge.update_layout(
            height=260,
            margin=dict(l=16, r=16, t=42, b=12),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color=COLORS["ink"]),
        )
        st.plotly_chart(fig_gauge, width="stretch")

    scored = [
        (term["name"], term["grade"])
        for term in analysis["terms"]
        if term["grade"] is not None
    ]
    if not scored:
        st.info("No scores yet for this subject.")
        return

    term_names, grades = zip(*scored)
    fig_bar = go.Figure(
        go.Bar(
            x=list(term_names),
            y=list(grades),
            marker_color=[grade_color(grade, subject["passing_grade"]) for grade in grades],
            text=[f"{grade:.1f}" for grade in grades],
            textposition="outside",
        )
    )
    fig_bar.add_hline(y=subject["passing_grade"], line_dash="dot", line_color=COLORS["amber"])
    fig_bar.update_layout(
        height=270,
        margin=dict(l=10, r=10, t=24, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.78)",
        font=dict(family="DM Sans", color=COLORS["ink"]),
        yaxis=dict(range=[0, 105], gridcolor="rgba(0,56,115,0.10)"),
        xaxis=dict(showgrid=False),
        showlegend=False,
    )
    st.plotly_chart(fig_bar, width="stretch")


def render_category_radar() -> None:
    if not plotly_available():
        return
    names = [subject["name"] for subject in subjects()]
    selected = st.selectbox(
        "Subject",
        names,
        index=min(st.session_state.gradewise_active_subject_idx, len(names) - 1),
        key="gw_radar_subject",
    )
    subject = subjects()[names.index(selected)]

    totals: dict[str, float] = {}
    counts: dict[str, int] = {}
    for term in subject["terms"]:
        for assessment in term["assessments"]:
            grade = calc_assessment_grade(assessment)
            if grade is None:
                continue
            totals[assessment["name"]] = totals.get(assessment["name"], 0.0) + grade
            counts[assessment["name"]] = counts.get(assessment["name"], 0) + 1

    if not totals:
        st.info("Enter scores to generate a category radar chart.")
        return

    labels = list(totals.keys())
    values = [totals[label] / counts[label] for label in labels]
    closed_labels = labels + [labels[0]]
    closed_values = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=closed_values,
            theta=closed_labels,
            fill="toself",
            fillcolor="rgba(0,86,163,0.14)",
            line_color=COLORS["blue"],
            marker=dict(color=COLORS["blue"], size=6),
            name="Average category grade",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=[subject["passing_grade"]] * len(closed_labels),
            theta=closed_labels,
            mode="lines",
            line=dict(color=COLORS["amber"], dash="dot", width=2),
            name=f"Passing ({subject['passing_grade']})",
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(255,255,255,0.78)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(0,56,115,0.10)"),
            angularaxis=dict(color=COLORS["ink"]),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=COLORS["ink"]),
        height=380,
        margin=dict(l=32, r=32, t=28, b=28),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig, width="stretch")

    weakest_idx = values.index(min(values))
    st.warning(
        f"Weakest category: {labels[weakest_idx]} at {values[weakest_idx]:.1f}. "
        "Prioritize this category first."
    )


def render_risk_map() -> None:
    analytics = [calc_subject_analytics(subject) for subject in subjects()]
    if not any(analysis["current_grade"] is not None for analysis in analytics):
        st.info("Enter scores to generate the risk map.")
        return

    for subject, analysis in zip(subjects(), analytics):
        risk = get_risk_info(analysis["probability"])
        probability = analysis["probability"] or 0
        grade = analysis["current_grade"]
        render_html(
            f"""
            <div class="gw-risk-card" style="background:{risk["bg"]};border-left:4px solid {risk["color"]};">
              <div class="gw-risk-top">
                <div>
                  <div class="gw-subject-name">{_safe(subject["name"])}</div>
                  <div class="gw-section-note">
                    Passing: {fmt(subject["passing_grade"])} |
                    Completed: {pct(analysis["completed_w"])} |
                    Remaining: {pct(analysis["remaining_w"])}
                  </div>
                </div>
                <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;justify-content:flex-end;">
                  <span class="gw-mono" style="font-size:18px;font-weight:700;color:{grade_color(grade, subject["passing_grade"])};">{fmt(grade)}</span>
                  <span class="gw-mono">{gwa_to_grade(grade)}</span>
                  <span class="gw-mono" style="font-weight:700;color:{risk["color"]};">{probability}%</span>
                  {risk_pill(risk)}
                </div>
              </div>
              <div class="gw-bar">
                <span style="width:{probability}%;background:{risk["color"]};"></span>
              </div>
              <div class="gw-section-note" style="margin-top:10px;">
                {explain_probability(analysis["earned_pts"], subject["passing_grade"], analysis["remaining_w"], analysis["probability"])}
              </div>
            </div>
            """
        )


# ---------------------------------------------------------------------------
# Page render
# ---------------------------------------------------------------------------

with tool_body_container():
    render_html('<div class="gw-shell">')
    render_intro()
    dashboard_tab, entry_tab, forecasting_tab, analytics_tab = st.tabs(
        ["Dashboard", "Grade Entry", "Forecasting", "Analytics"]
    )
    with dashboard_tab:
        render_dashboard()
    with entry_tab:
        render_grade_entry()
    with forecasting_tab:
        render_forecasting()
    with analytics_tab:
        render_analytics()
    render_html("</div>")
