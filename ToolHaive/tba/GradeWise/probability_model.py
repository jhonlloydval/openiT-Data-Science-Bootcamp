"""
probability_model.py — Passing Probability Computation

Methodology: Weighted Distance Probability Model with Performance Trend Multiplier

When a panel asks "how do you compute 43% passing probability?":

    "We use a Weighted Distance Probability Model. It computes the ratio of
    grade points still achievable versus grade points still needed to pass,
    adjusted by a performance trend multiplier derived from the student's
    score trajectory across completed terms.

    We chose a rule-based approach over machine learning deliberately —
    we have no historical cohort data, and a transparent deterministic
    formula is more auditable and explainable to the end user."

Formula:
    1. gap        = passing_grade − earned_points
    2. achievable = remaining_weight × 100   (max points still earnable)
    3. raw_prob   = (achievable − gap) / achievable         → clamped [0, 1]
    4. trend_mult = 1 + clamp(trend / 50, −0.20, +0.20)
    5. probability = clamp(raw_prob × trend_mult × 100, 2, 99)

    Special cases:
    - No remaining weight: 97% if already passing, 3% if not
    - Mathematically impossible (even 100 in all remaining ≠ pass): 2%
    - Already enough points to pass: 91–99% (boosted by trend)
"""

from typing import Optional


def calc_pass_probability(
    earned_pts: float,
    passing_grade: float,
    remaining_weight: float,
    trend: float = 0.0,
) -> int:
    """
    Compute passing probability (0–100 integer) using the
    Weighted Distance Probability Model.

    Args:
        earned_pts:       Sum of (term_grade × term_weight) for completed terms.
                          Example: Prelims grade 70 × 0.20 + Midterm 74 × 0.20 = 28.8
        passing_grade:    The minimum final grade required to pass (e.g., 75).
        remaining_weight: Fraction of grade not yet earned (e.g., 0.60 = 60% left).
        trend:            Grade delta between the last two terms (positive = improving).

    Returns:
        Integer probability from 2 to 99.
    """
    # ── Special case: all terms completed ─────────────────────────────────────
    if remaining_weight <= 0:
        return 97 if earned_pts >= passing_grade else 3

    # ── Special case: mathematically impossible to pass ───────────────────────
    max_possible_final = earned_pts + remaining_weight * 100
    if max_possible_final < passing_grade:
        return 2

    # ── Special case: already have enough points ───────────────────────────────
    gap = passing_grade - earned_pts
    if gap <= 0:
        boost = min(8.0, (trend / 10.0) * 4.0)
        return min(99, round(91 + boost))

    # ── Core Weighted Distance formula ────────────────────────────────────────
    max_from_remaining = remaining_weight * 100
    raw = (max_from_remaining - gap) / max_from_remaining        # 0–1 range

    # ── Trend multiplier: ±20% adjustment ─────────────────────────────────────
    trend_mult = 1.0 + max(-0.20, min(0.20, trend / 50.0))

    probability = raw * trend_mult * 100
    return int(max(2, min(99, round(probability))))


def get_trend_label(trend: float) -> str:
    """Convert a trend float to a human-readable label."""
    if trend > 5:
        return "📈 Improving"
    if trend < -5:
        return "📉 Declining"
    return "➡️ Stable"


def explain_probability(
    earned_pts: float,
    passing_grade: float,
    remaining_weight: float,
    probability: int,
) -> str:
    """
    Generate a one-sentence explanation of why the probability is what it is.
    Used in the Risk and Forecasting pages.
    """
    gap = passing_grade - earned_pts
    max_remaining = remaining_weight * 100

    if remaining_weight <= 0:
        if earned_pts >= passing_grade:
            return "All terms completed and passing grade achieved."
        return "All terms completed but did not reach the passing grade."

    if gap <= 0:
        return f"Already ahead by {abs(gap):.1f} points — just needs to maintain performance."

    if probability <= 2:
        return (
            f"Even with perfect scores in the remaining {remaining_weight*100:.0f}%, "
            f"the maximum achievable grade is below {passing_grade}."
        )

    req = gap / remaining_weight
    return (
        f"Needs at least {req:.1f}/100 average in the remaining "
        f"{remaining_weight*100:.0f}% to pass."
    )
