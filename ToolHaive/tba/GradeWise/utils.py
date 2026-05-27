"""
utils.py — Core grade computation and data structures.

Grading model:
    Subject → Terms → Assessment Categories → Items (individual scored tasks)

Each item has: name, total (max score), score → percentage auto-computed.
Category grade = weighted average of item percentages.
Term grade     = weighted average of category grades.
Subject grade  = weighted average of term grades.
"""

import uuid
import copy
from typing import Optional
from probability_model import calc_pass_probability

# ── Default Structure ──────────────────────────────────────────────────────────
# Weights must sum to 1.0 within each group.

DEFAULT_TERMS = [
    {"id": "prelims", "name": "Prelims",     "weight": 0.20},
    {"id": "midterm", "name": "Midterm",     "weight": 0.20},
    {"id": "semis",   "name": "Semi-Finals", "weight": 0.25},
    {"id": "finals",  "name": "Finals",      "weight": 0.35},
]

DEFAULT_ASSESSMENTS = [
    {"id": "quiz",       "name": "Quiz",       "weight": 0.30},
    {"id": "attendance", "name": "Attendance", "weight": 0.10},
    {"id": "project",    "name": "Project",    "weight": 0.30},
    {"id": "exam",       "name": "Exam",       "weight": 0.30},
]


def _uid() -> str:
    return str(uuid.uuid4())[:8]


# ── Constructors ───────────────────────────────────────────────────────────────

def create_subject(name: str, passing_grade: float = 75.0) -> dict:
    """Create a fresh subject with empty assessment items."""
    return {
        "id":            _uid(),
        "name":          name,
        "passing_grade": passing_grade,
        "terms": [
            {
                **term,
                "assessments": [
                    {**a, "items": []}
                    for a in DEFAULT_ASSESSMENTS
                ],
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
    """Return a new subject with the item appended (non-mutating)."""
    s = copy.deepcopy(subject)
    for term in s["terms"]:
        if term["id"] == term_id:
            for a in term["assessments"]:
                if a["id"] == assessment_id:
                    a["items"].append({
                        "id":    _uid(),
                        "name":  item_name,
                        "total": total,
                        "score": score,
                    })
    return s


def delete_assessment_item(
    subject: dict,
    term_id: str,
    assessment_id: str,
    item_id: str,
) -> dict:
    """Return a new subject with the item removed (non-mutating)."""
    s = copy.deepcopy(subject)
    for term in s["terms"]:
        if term["id"] == term_id:
            for a in term["assessments"]:
                if a["id"] == assessment_id:
                    a["items"] = [i for i in a["items"] if i["id"] != item_id]
    return s


# ── Grade Computation ──────────────────────────────────────────────────────────

def item_percentage(item: dict) -> Optional[float]:
    """Percentage score for a single assessment item (0–100)."""
    if item["total"] <= 0:
        return None
    return (item["score"] / item["total"]) * 100


def calc_assessment_grade(assessment: dict) -> Optional[float]:
    """
    Category grade = average percentage across all items.
    Returns None if no items entered.
    """
    items = assessment.get("items", [])
    if not items:
        return None
    total_possible = sum(i["total"] for i in items)
    total_earned   = sum(i["score"] for i in items)
    if total_possible == 0:
        return None
    return (total_earned / total_possible) * 100


def calc_term_grade(assessments: list) -> Optional[float]:
    """
    Term grade = weighted average of category grades.
    Only categories with items contribute; weight is normalized.
    """
    weighted_sum = 0.0
    total_weight = 0.0
    for a in assessments:
        grade = calc_assessment_grade(a)
        if grade is None:
            continue
        weighted_sum += grade * a["weight"]
        total_weight += a["weight"]
    if total_weight == 0:
        return None
    return weighted_sum / total_weight


def calc_subject_analytics(subject: dict) -> dict:
    """
    Compute all analytics for a subject. Returns:
        terms           – list of term dicts with computed 'grade'
        scored_terms    – subset with non-None grades
        completed_w     – fraction of weight scored (0–1)
        remaining_w     – 1 − completed_w
        earned_pts      – sum(term_grade × term_weight) for scored terms
        current_grade   – normalized running average
        trend           – grade delta between last two scored terms
        probability     – passing probability (None if no scores)
    """
    terms = [
        {**t, "grade": calc_term_grade(t["assessments"])}
        for t in subject["terms"]
    ]
    scored      = [t for t in terms if t["grade"] is not None]
    completed_w = sum(t["weight"] for t in scored)
    remaining_w = round(1.0 - completed_w, 10)
    earned_pts  = sum(t["grade"] * t["weight"] for t in scored)
    current_grade = (earned_pts / completed_w) if completed_w > 0 else None

    trend = 0.0
    if len(scored) >= 2:
        trend = scored[-1]["grade"] - scored[-2]["grade"]

    probability = None
    if current_grade is not None:
        probability = calc_pass_probability(
            earned_pts=earned_pts,
            passing_grade=subject["passing_grade"],
            remaining_weight=remaining_w,
            trend=trend,
        )

    return {
        "terms":         terms,
        "scored_terms":  scored,
        "completed_w":   completed_w,
        "remaining_w":   remaining_w,
        "earned_pts":    earned_pts,
        "current_grade": current_grade,
        "trend":         trend,
        "probability":   probability,
    }


def forecast_required_score(
    earned_pts: float,
    target_grade: float,
    remaining_weight: float,
) -> dict:
    """Min average score needed in remaining weight to reach target."""
    if remaining_weight <= 0:
        return {"required_score": None, "achievable": False, "note": "No remaining weight."}
    req = (target_grade - earned_pts) / remaining_weight
    note = (
        "Target already achieved! 🎉" if req <= 0
        else f"Requires {req:.1f}/100 — may not be achievable." if req > 100
        else f"Need {req:.1f} average in remaining {remaining_weight*100:.0f}%."
    )
    return {"required_score": round(req, 1), "achievable": req <= 100, "note": note}


# ── Risk & Display Helpers ─────────────────────────────────────────────────────

def get_risk_info(probability: Optional[float]) -> dict:
    if probability is None:
        return {"level": "—",        "color": "#64748b", "bg": "#1e2d3a"}
    if probability >= 75:
        return {"level": "Low",      "color": "#22d3a0", "bg": "#0d2e26"}
    if probability >= 50:
        return {"level": "Moderate", "color": "#f59e0b", "bg": "#2a1f0a"}
    if probability >= 25:
        return {"level": "High",     "color": "#fb923c", "bg": "#2a1608"}
    return     {"level": "Critical", "color": "#f87171", "bg": "#2a0d0d"}


def fmt(value: Optional[float], decimals: int = 1) -> str:
    return "—" if value is None else f"{value:.{decimals}f}"


def pct(weight: float) -> str:
    return f"{round(weight * 100)}%"


def gwa_to_grade(score: float) -> str:
    for threshold, gwa in [(97,"1.00"),(94,"1.25"),(91,"1.50"),(88,"1.75"),
                            (85,"2.00"),(82,"2.25"),(79,"2.50"),(76,"2.75"),(75,"3.00")]:
        if score >= threshold:
            return gwa
    return "5.00"


def grade_color(score: Optional[float], passing: float = 75.0) -> str:
    if score is None:
        return "#64748b"
    if score >= passing:
        return "#22d3a0"
    if score >= passing - 5:
        return "#f59e0b"
    return "#f87171"