"""
pages/analytics.py — Visual Analytics

Charts:
    Grade Trends   — line chart, all subjects across terms
    Subject Detail — gauge + bar chart per subject
    Radar Chart    — weakest assessment category
    Risk Map       — heatmap of all subjects
"""

import streamlit as st
import plotly.graph_objects as go

from styles import page_header, risk_badge, grade_bar, COLORS
from utils import (
    calc_subject_analytics, calc_assessment_grade,
    get_risk_info, fmt, pct, gwa_to_grade, grade_color,
)


def render():
    page_header("📊 Analytics", "Visual breakdown of your academic performance.")

    if not st.session_state.subjects:
        st.info("Add subjects and enter scores in **Grade Entry** first.", icon="📚")
        return

    subjects  = st.session_state.subjects
    analytics = [calc_subject_analytics(s) for s in subjects]

    t1, t2, t3, t4 = st.tabs(["📈 Trends", "🔍 Subject Detail", "🕸️ Radar", "🗺️ Risk Map"])

    # ══════════════════════════════════════════════════════════════════
    # TAB 1 — Grade Trends
    # ══════════════════════════════════════════════════════════════════
    with t1:
        graded = [(s, a) for s, a in zip(subjects, analytics) if a["scored_terms"]]
        if not graded:
            st.info("Enter some scores to see trends.", icon="📊")
        else:
            fig = go.Figure()
            for s, a in graded:
                pts = [(t["name"], round(t["grade"], 1)) for t in a["terms"] if t["grade"] is not None]
                if pts:
                    xs, ys = zip(*pts)
                    fig.add_trace(go.Scatter(
                        x=list(xs), y=list(ys), name=s["name"],
                        mode="lines+markers+text",
                        text=[str(y) for y in ys], textposition="top center",
                        textfont=dict(size=11), marker=dict(size=7), line=dict(width=2.5),
                    ))
            fig.update_layout(
                plot_bgcolor=COLORS["surface2"], paper_bgcolor=COLORS["surface1"],
                font_color=COLORS["text"], font_family="Outfit", height=320,
                margin=dict(l=0, r=0, t=20, b=0),
                yaxis=dict(range=[50, 105], gridcolor=COLORS["border"], title="Grade"),
                xaxis=dict(showgrid=False),
                legend=dict(bgcolor="rgba(0,0,0,0)", font_color=COLORS["dim"]),
            )
            st.plotly_chart(fig, use_container_width=True)

        # Summary table
        st.markdown("---")
        header = st.columns([2, 1, 1, 1, 1, 1])
        for col, lbl in zip(header, ["Subject", "Grade", "GWA", "Probability", "Remaining", "Risk"]):
            col.markdown(f"<span style='font-size:10px;color:{COLORS['muted']};text-transform:uppercase;letter-spacing:.07em'>{lbl}</span>", unsafe_allow_html=True)

        for s, a in zip(subjects, analytics):
            ri  = get_risk_info(a["probability"])
            cg  = a["current_grade"]
            col = grade_color(cg, s["passing_grade"])
            row = st.columns([2, 1, 1, 1, 1, 1])
            row[0].markdown(f"**{s['name']}**")
            row[1].markdown(f"<span style='font-family:JetBrains Mono,monospace;font-weight:700;color:{col}'>{fmt(cg)}</span>", unsafe_allow_html=True)
            row[2].markdown(f"<span style='color:{COLORS['dim']}'>{gwa_to_grade(cg) if cg else '—'}</span>", unsafe_allow_html=True)
            row[3].markdown(f"<span style='color:{ri['color']};font-weight:600'>{a['probability']}%</span>" if a["probability"] else "—", unsafe_allow_html=True)
            row[4].markdown(f"<span style='color:{COLORS['dim']}'>{pct(a['remaining_w'])}</span>", unsafe_allow_html=True)
            row[5].markdown(risk_badge(ri["level"]), unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    # TAB 2 — Subject Detail
    # ══════════════════════════════════════════════════════════════════
    with t2:
        names    = [s["name"] for s in subjects]
        sel      = st.selectbox("Subject", names, index=st.session_state.active_subject_idx, key="an_det")
        idx      = names.index(sel)
        st.session_state.active_subject_idx = idx
        subject  = subjects[idx]
        a        = analytics[idx]
        ri       = get_risk_info(a["probability"])

        st.markdown("---")

        if a["probability"] is not None:
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=a["probability"],
                title={"text": "Passing Probability", "font": {"color": COLORS["text"], "family": "Outfit", "size": 13}},
                number={"suffix": "%", "font": {"color": ri["color"], "family": "JetBrains Mono", "size": 34}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": COLORS["muted"]},
                    "bar": {"color": ri["color"]},
                    "bgcolor": COLORS["surface3"], "bordercolor": COLORS["border"],
                    "steps": [
                        {"range": [0,  25], "color": f"{COLORS['red']}22"},
                        {"range": [25, 50], "color": f"{COLORS['orange']}22"},
                        {"range": [50, 75], "color": f"{COLORS['amber']}22"},
                        {"range": [75,100], "color": f"{COLORS['green']}22"},
                    ],
                    "threshold": {"line": {"color": COLORS["amber"], "width": 2}, "thickness": .75, "value": 75},
                },
            ))
            fig_g.update_layout(
                paper_bgcolor=COLORS["surface1"], font_color=COLORS["text"],
                height=240, margin=dict(l=20, r=20, t=40, b=10),
            )
            st.plotly_chart(fig_g, use_container_width=True)

        scored = [(t["name"], t["grade"]) for t in a["terms"] if t["grade"] is not None]
        if scored:
            ns, gs = zip(*scored)
            fig_b = go.Figure(go.Bar(
                x=list(ns), y=list(gs),
                marker_color=[COLORS["green"] if g >= subject["passing_grade"] else COLORS["red"] for g in gs],
                text=[f"{g:.1f}" for g in gs], textposition="outside",
                textfont=dict(color=COLORS["text"], size=12),
            ))
            fig_b.add_hline(y=subject["passing_grade"], line_dash="dot", line_color=COLORS["amber"])
            fig_b.update_layout(
                plot_bgcolor=COLORS["surface2"], paper_bgcolor=COLORS["surface1"],
                font_color=COLORS["text"], font_family="Outfit", height=240,
                margin=dict(l=0, r=0, t=10, b=0),
                yaxis=dict(range=[50, 108], gridcolor=COLORS["border"]),
                xaxis=dict(showgrid=False), showlegend=False,
            )
            st.plotly_chart(fig_b, use_container_width=True)
        else:
            st.info("No scores yet for this subject.", icon="📊")

    # ══════════════════════════════════════════════════════════════════
    # TAB 3 — Radar (weakest category)
    # ══════════════════════════════════════════════════════════════════
    with t3:
        names = [s["name"] for s in subjects]
        sel   = st.selectbox("Subject", names, index=st.session_state.active_subject_idx, key="an_rad")
        subject = subjects[names.index(sel)]

        # Aggregate category grades across all terms
        totals = {}
        counts = {}
        for term in subject["terms"]:
            for a in term["assessments"]:
                g = calc_assessment_grade(a)
                if g is not None:
                    totals[a["name"]] = totals.get(a["name"], 0) + g
                    counts[a["name"]] = counts.get(a["name"], 0) + 1

        if not totals:
            st.info("Enter scores to generate the radar chart.", icon="📡")
        else:
            labels = list(totals.keys())
            avgs   = [totals[l] / counts[l] for l in labels]
            labels_c = labels + [labels[0]]
            avgs_c   = avgs   + [avgs[0]]

            fig_r = go.Figure()
            fig_r.add_trace(go.Scatterpolar(
                r=avgs_c, theta=labels_c, fill="toself",
                fillcolor=f"{COLORS['accent']}22",
                line_color=COLORS["accent"], name="Avg Category Grade",
                marker=dict(color=COLORS["accent"], size=5),
            ))
            fig_r.add_trace(go.Scatterpolar(
                r=[subject["passing_grade"]] * len(labels_c), theta=labels_c,
                mode="lines", line=dict(color=COLORS["amber"], dash="dot", width=1.5),
                name=f"Passing ({subject['passing_grade']})",
            ))
            fig_r.update_layout(
                polar=dict(
                    bgcolor=COLORS["surface2"],
                    radialaxis=dict(visible=True, range=[0, 100],
                                    gridcolor=COLORS["border"], tickcolor=COLORS["muted"],
                                    color=COLORS["muted"]),
                    angularaxis=dict(color=COLORS["text"]),
                ),
                paper_bgcolor=COLORS["surface1"], font_color=COLORS["text"],
                font_family="Outfit", height=360,
                margin=dict(l=40, r=40, t=30, b=30),
                legend=dict(bgcolor="rgba(0,0,0,0)", font_color=COLORS["dim"]),
                showlegend=True,
            )
            st.plotly_chart(fig_r, use_container_width=True)

            weakest_idx = avgs.index(min(avgs))
            st.warning(
                f"📉 Weakest category: **{labels[weakest_idx]}** — average {avgs[weakest_idx]:.1f}. "
                "Focus here for the biggest grade improvement.",
                icon="🎯",
            )

    # ══════════════════════════════════════════════════════════════════
    # TAB 4 — Risk Map
    # ══════════════════════════════════════════════════════════════════
    with t4:
        graded = [(s, a) for s, a in zip(subjects, analytics) if a["current_grade"] is not None]
        if not graded:
            st.info("Enter scores to generate the risk map.", icon="🗺️")
            return

        for s, a in zip(subjects, analytics):
            ri  = get_risk_info(a["probability"])
            cg  = a["current_grade"]
            prob = a["probability"] or 0
            col = grade_color(cg, s["passing_grade"])

            st.markdown(
                f"""<div style='background:{ri['bg']};border:1px solid {ri['color']}33;
                    border-left:4px solid {ri['color']};border-radius:10px;padding:14px 18px;margin-bottom:10px'>
                    <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px'>
                        <div>
                            <span style='font-weight:700;font-size:15px'>{s['name']}</span>
                            <span style='color:{COLORS['muted']};font-size:11px;margin-left:8px'>Passing: {s['passing_grade']}</span>
                        </div>
                        <div style='display:flex;align-items:center;gap:14px'>
                            <span style='font-family:JetBrains Mono,monospace;font-size:20px;font-weight:700;color:{col}'>{fmt(cg)}</span>
                            <span style='font-size:12px;color:{COLORS['dim']}'>{gwa_to_grade(cg) if cg else '—'}</span>
                            <span style='font-family:JetBrains Mono,monospace;color:{ri["color"]};font-weight:700'>{prob}%</span>
                        </div>
                    </div>
                    {grade_bar(prob, ri['color'], 7)}
                    <div style='display:flex;justify-content:space-between;margin-top:7px'>
                        <span style='font-size:11px;color:{COLORS["muted"]}'>Completed: {pct(a["completed_w"])} · Remaining: {pct(a["remaining_w"])}</span>
                        <span style='font-size:11px;font-weight:600;color:{ri["color"]}'>{ri["level"]} Risk</span>
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )