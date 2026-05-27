"""
data/sample_subjects.py — Demo data for testing Gradewise.

Call get_sample_subjects() to load pre-filled subjects.
Edit scores here to simulate different risk scenarios.
"""

import copy
from utils import create_subject


def get_sample_subjects() -> list:
    """
    Returns a list of 4 sample subjects with varying risk levels.
    Designed to demonstrate all dashboard states:
        - Calculus:    Low risk (strong grades)
        - Programming: Moderate risk (average grades)
        - Physics:     High risk (below-average)
        - Electronics: Critical risk (very low scores)
    """

    def fill_scores(subject, score_map: dict) -> dict:
        """
        Fill in scores from a nested dict:
        score_map = { term_id: { assessment_id: score } }
        """
        s = copy.deepcopy(subject)
        for term in s["terms"]:
            term_scores = score_map.get(term["id"], {})
            for a in term["assessments"]:
                if a["id"] in term_scores:
                    a["score"] = term_scores[a["id"]]
        return s

    # ── Calculus: Strong student, low risk ────────────────────────────────────
    calculus = fill_scores(
        create_subject("Calculus", passing_grade=75),
        {
            "prelims": {"quiz": 92, "attendance": 100, "project": 88, "exam": 90},
            "midterm": {"quiz": 88, "attendance": 100, "project": 91, "exam": 93},
            # Semi-finals and Finals not yet taken
        },
    )

    # ── Programming: Decent grades, moderate risk ─────────────────────────────
    programming = fill_scores(
        create_subject("Programming", passing_grade=75),
        {
            "prelims": {"quiz": 80, "attendance": 95, "project": 82, "exam": 78},
            "midterm": {"quiz": 75, "attendance": 90, "project": 77, "exam": 76},
            "semis":   {"quiz": 72, "attendance": 88, "project": 74, "exam": None},
        },
    )

    # ── Physics: Struggling, high risk ────────────────────────────────────────
    physics = fill_scores(
        create_subject("Physics", passing_grade=75),
        {
            "prelims": {"quiz": 68, "attendance": 80, "project": 70, "exam": 65},
            "midterm": {"quiz": 64, "attendance": 75, "project": 68, "exam": 62},
        },
    )

    # ── Electronics: Critical risk ────────────────────────────────────────────
    electronics = fill_scores(
        create_subject("Electronics", passing_grade=75),
        {
            "prelims": {"quiz": 55, "attendance": 70, "project": 60, "exam": 58},
            "midterm": {"quiz": 52, "attendance": 65, "project": 57, "exam": 50},
            "semis":   {"quiz": 54, "attendance": 68, "project": 59, "exam": 53},
        },
    )

    return [calculus, programming, physics, electronics]
