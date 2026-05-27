"""
pages/dashboard.py — Main Dashboard

EDIT SECTIONS are clearly marked. Each is self-contained.
Current layout:
  Row 1 — Summary metrics (all subjects)
  Row 2 — Active subject detail cards
  Row 3 — Term progress chart
  Row 4 — All subjects risk table
  Row 5 — Alert banner
"""

import streamlit as st
import plotly.graph_objects as go

from styles import page_header, metric_card, risk_badge, grade_bar, COLORS
from utils import calc_subject_analytics, get_risk_info, fmt, pct, gwa_to_grade, grade_color


def render():
    page_header("🏠 Dashboard", "Your academic overview at a glance.")

    if not st.session_state.subjects:
        st.info(
            "No subjects loaded. Go to **Grade Entry** to add subjects, "
            "or click **📋 Sample** in the sidebar to load demo data.",
            icon="🎓",
        )
        return

    subjects  = st.session_state.subjects
    analytics = [calc_subject_analytics(s) for s in subjects]

    # ══════════════════════════════════════════════════════════════════
    # EDIT SECTION 1 — Top summary row
    # ══════════════════════════════════════════════════════════════════
    graded_subjects = [(s, a) for s, a in zip(subjects, analytics) if a["current_grade"] is not None]
    n_passing = sum(1 for s, a in graded_subjects if a["current_grade"] >= s["passing_grade"])
    avg_prob  = (
        sum(a["probability"] for _, a in graded_subjects if a["probability"] is not None)
        / max(len(graded_subjects), 1)
    ) if graded_subjects else None
    at_risk = sum(1 for a in analytics if a["probability"] is not None and a["probability"] < 50)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Subjects",    len(subjects))
    c2.metric("Subjects Passing",  f"{n_passing} / {len(graded_subjects)}" if graded_subjects else "—")
    c3.metric("Avg Pass Probability", f"{avg_prob:.0f}%" if avg_prob is not None else "—")
    c4.metric("At-Risk Subjects",  at_risk,
              delta=f"{at_risk} need attention" if at_risk else "All clear",
              delta_color="inverse")

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════
    # EDIT SECTION 2 — Active subject detail cards
    # ══════════════════════════════════════════════════════════════════
    idx  = st.session_state.active_subject_idx
    subj = subjects[idx]
    ana  = analytics[idx]
    risk = get_risk_info(ana["probability"])

    st.markdown(f"#### {subj['name']}")
    st.caption(
        f"Passing: **{subj['passing_grade']}** · "
        f"Completed: **{pct(ana['completed_w'])}** · "
        f"Remaining: **{pct(ana['remaining_w'])}**"
    )

    d1, d2, d3, d4 = st.columns(4)

    with d1:
        cg = ana["current_grade"]
        metric_card(
            "Current Grade", fmt(cg),
            sub="✓ Passing" if cg and cg >= subj["passing_grade"] else "⚠ Below passing",
            color=grade_color(cg, subj["passing_grade"]),
        )
    with d2:
        metric_card(
            "Pass Probability",
            f"{ana['probability']}%" if ana["probability"] is not None else "—",
            sub=f"{risk['level']} Risk",
            color=risk["color"],
        )
    with d3:
        if ana["remaining_w"] > 0 and ana["earned_pts"] is not None:
            req = (subj["passing_grade"] - ana["earned_pts"]) / ana["remaining_w"]
            metric_card(
                "Required Score", fmt(req),
                sub="Already passing 🎉" if req <= 0 else (
                    "Hard — requires > 100" if req > 100 else
                    f"Avg needed in remaining {pct(ana['remaining_w'])}"
                ),
                color=COLORS["green"] if req <= 0 else (COLORS["red"] if req > 100 else COLORS["amber"]),
            )
        else:
            metric_card("Required Score", "—", sub="No remaining weight", color=COLORS["muted"])
    with d4:
        metric_card(
            "GWA Equivalent",
            gwa_to_grade(ana["current_grade"]) if ana["current_grade"] else "—",
            sub="Based on current grade",
            color=COLORS["dim"],
        )

    # Probability bar
    if ana["probability"] is not None:
        st.markdown(
            f'<div style="margin:4px 0 16px">'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:5px">'
            f'<span style="font-size:12px;color:{COLORS["muted"]}">Passing Likelihood</span>'
            f'<span style="font-size:12px;font-weight:600;color:{risk["color"]}">{ana["probability"]}% — {risk["level"]}</span>'
            f'</div>{grade_bar(ana["probability"], risk["color"], 8)}</div>',
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════════
    # EDIT SECTION 3 — Term progress chart
    # Swap for line chart or radar by changing the figure type.
    # ══════════════════════════════════════════════════════════════════
    scored = [(t["name"], t["grade"]) for t in ana["terms"] if t["grade"] is not None]
    if scored:
        names, grades = zip(*scored)
        fig = go.Figure(go.Bar(
            x=list(names), y=list(grades),
            marker_color=[COLORS["green"] if g >= subj["passing_grade"] else COLORS["red"] for g in grades],
            text=[f"{g:.1f}" for g in grades], textposition="outside",
            textfont=dict(color=COLORS["text"], size=12),
        ))
        fig.add_hline(y=subj["passing_grade"], line_dash="dot", line_color=COLORS["amber"],
                      annotation_text=f"Passing: {subj['passing_grade']}",
                      annotation_font_color=COLORS["amber"])
        fig.update_layout(
            plot_bgcolor=COLORS["surface2"], paper_bgcolor=COLORS["surface1"],
            font_color=COLORS["text"], font_family="Outfit", height=240,
            margin=dict(l=0, r=0, t=20, b=0),
            yaxis=dict(range=[50, 107], gridcolor=COLORS["border"]),
            xaxis=dict(showgrid=False), showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════
    # EDIT SECTION 4 — All-subjects risk table
    # ══════════════════════════════════════════════════════════════════
    st.markdown("#### All Subjects")

    cols = [3, 2, 2, 2, 2]
    header = st.columns(cols)
    for col, label in zip(header, ["Subject", "Grade", "Probability", "Risk", "Remaining"]):
        col.markdown(
            f"<span style='font-size:10px;color:{COLORS['muted']};text-transform:uppercase;letter-spacing:.08em'>{label}</span>",
            unsafe_allow_html=True,
        )

    for i, (s, a) in enumerate(zip(subjects, analytics)):
        ri  = get_risk_info(a["probability"])
        cg  = a["current_grade"]
        row = st.columns(cols)
        row[0].markdown(f"{'**◈ ' if i == idx else ''}{s['name']}{'**' if i == idx else ''}")
        row[1].markdown(
            f"<span style='font-family:JetBrains Mono,monospace;font-weight:700;color:{grade_color(cg, s['passing_grade'])}'>{fmt(cg)}</span>",
            unsafe_allow_html=True,
        )
        row[2].markdown(
            f"<span style='color:{ri['color']};font-weight:600'>{a['probability']}%</span>" if a["probability"] else "—",
            unsafe_allow_html=True,
        )
        row[3].markdown(risk_badge(ri["level"]), unsafe_allow_html=True)
        row[4].markdown(
            f"<span style='color:{COLORS['dim']}'>{pct(a['remaining_w'])}</span>",
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════════
    # EDIT SECTION 5 — Alert banner
    # ══════════════════════════════════════════════════════════════════
    st.markdown("---")
    critical = [s["name"] for s, a in zip(subjects, analytics)
                if a.get("probability") and a["probability"] < 25]

    if critical:
        names_str = ", ".join(critical)
        st.error(
            f"🚨 **Critical:** {names_str} {'has' if len(critical)==1 else 'have'} < 25% passing probability. "
            "Prioritize these now.",
            icon="⚠️",
        )
    elif at_risk:
        st.warning(
            f"📌 {at_risk} subject(s) at moderate-to-high risk. "
            "Check **Forecasting** for what scores you need.",
            icon="📋",
        )
    elif graded_subjects:
        st.success(
            "✅ All subjects have passing probability above 50%. Keep it up!",
            icon="🎓",
        )