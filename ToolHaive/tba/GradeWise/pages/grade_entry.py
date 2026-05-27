"""
pages/grade_entry.py — Grade Entry

Excel-like grading sheet. Each assessment category (Quiz, Attendance, etc.)
holds individual scored items. Grades compute automatically at every level.

Layout:
    Term (Prelims 20%)
    └── Category (Quiz 30%)
        ├── Item table: Name | Total | Score | %
        ├── [+ Add item] form
        └── Category grade (auto-computed)
"""

import streamlit as st

from styles import page_header, COLORS, grade_bar
from utils import (
    create_subject,
    add_assessment_item,
    delete_assessment_item,
    calc_assessment_grade,
    calc_term_grade,
    item_percentage,
    fmt, pct, grade_color,
)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _pct_color(pct_val: Optional[float], passing: float) -> str:
    from utils import grade_color
    return grade_color(pct_val, passing)


# ── Sub-renders ────────────────────────────────────────────────────────────────

def _render_item_table(assessment: dict, term_id: str, subj_idx: int, passing: float):
    """Render the item table + add-item form for one assessment category."""
    items = assessment.get("items", [])

    # ── Table ──────────────────────────────────────────────────────────────────
    if items:
        # Header
        st.markdown(
            f"""<div class="ge-table-header">
                <span>Item</span><span>Total</span><span>Score</span>
                <span>Percentage</span><span></span>
            </div>""",
            unsafe_allow_html=True,
        )
        for item in items:
            pct_val = item_percentage(item)
            col_pct = grade_color(pct_val, passing) if pct_val is not None else COLORS["muted"]
            pct_str = f"{pct_val:.1f}%" if pct_val is not None else "—"

            c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 0.5])
            c1.markdown(f"<span style='font-size:13px;font-weight:500'>{item['name']}</span>", unsafe_allow_html=True)
            c2.markdown(f"<span style='font-family:JetBrains Mono,monospace;font-size:13px;color:{COLORS['dim']}'>{item['total']:.0f}</span>", unsafe_allow_html=True)
            c3.markdown(f"<span style='font-family:JetBrains Mono,monospace;font-size:13px;color:{COLORS['text']}'>{item['score']:.0f}</span>", unsafe_allow_html=True)
            c4.markdown(f"<span style='font-family:JetBrains Mono,monospace;font-size:13px;font-weight:600;color:{col_pct}'>{pct_str}</span>", unsafe_allow_html=True)
            if c5.button("✕", key=f"del_{item['id']}", help="Delete this item"):
                subject = st.session_state.subjects[subj_idx]
                updated = delete_assessment_item(subject, term_id, assessment["id"], item["id"])
                st.session_state.subjects[subj_idx] = updated
                st.rerun()
    else:
        st.markdown(
            f"<div style='font-size:12px;color:{COLORS['muted']};padding:8px 0'>No items yet. Add one below.</div>",
            unsafe_allow_html=True,
        )

    # ── Category grade summary ─────────────────────────────────────────────────
    cat_grade = calc_assessment_grade(assessment)
    if cat_grade is not None:
        color = grade_color(cat_grade, passing)
        pct_filled = min(100, cat_grade)
        st.markdown(
            f"<div class='ge-category-grade'>"
            f"<span>Category Grade:</span>"
            f"<b style='color:{color}'>{cat_grade:.1f}</b>"
            f"<div style='flex:1;height:5px;background:{COLORS['surface3']};border-radius:99px;overflow:hidden'>"
            f"<div style='width:{pct_filled}%;height:100%;background:{color};border-radius:99px'></div>"
            f"</div></div>",
            unsafe_allow_html=True,
        )

    # ── Add-item form ──────────────────────────────────────────────────────────
    form_key = f"add_{st.session_state.subjects[subj_idx]['id']}_{term_id}_{assessment['id']}"
    with st.form(form_key, clear_on_submit=True):
        fi1, fi2, fi3, fi4 = st.columns([3, 1, 1, 1])
        item_name  = fi1.text_input("Name",  placeholder=f"{assessment['name']} 1", label_visibility="collapsed")
        total_pts  = fi2.number_input("Total", min_value=1.0, value=20.0, step=1.0, label_visibility="collapsed")
        score_pts  = fi3.number_input("Score", min_value=0.0, value=0.0,  step=0.5, label_visibility="collapsed")
        submitted  = fi4.form_submit_button(f"+ Add", use_container_width=True)

        # Column labels (first row only, as reference)
        st.markdown(
            f"<div style='display:flex;gap:8px;font-size:10px;color:{COLORS['muted']};margin-top:-8px'>"
            f"<span style='flex:3'>Name</span><span style='flex:1'>Total</span>"
            f"<span style='flex:1'>Score</span><span style='flex:1'></span></div>",
            unsafe_allow_html=True,
        )

        if submitted:
            if not item_name.strip():
                st.error("Enter an item name.", icon="⚠️")
            elif score_pts > total_pts:
                st.error("Score cannot exceed total.", icon="⚠️")
            else:
                subject = st.session_state.subjects[subj_idx]
                updated = add_assessment_item(
                    subject, term_id, assessment["id"],
                    item_name.strip(), total_pts, score_pts,
                )
                st.session_state.subjects[subj_idx] = updated
                st.rerun()


def _render_term(term: dict, subj_idx: int, passing: float):
    """Render one term as an expander with all its assessment categories."""
    term_grade = calc_term_grade(term["assessments"])
    grade_str  = f"{term_grade:.1f}" if term_grade is not None else "—"
    has_items  = any(a.get("items") for a in term["assessments"])

    with st.expander(
        f"**{term['name']}** — {pct(term['weight'])} weight   |   Grade: **{grade_str}**",
        expanded=has_items,
    ):
        for assessment in term["assessments"]:
            # Assessment category header
            cat_grade = calc_assessment_grade(assessment)
            cat_color = grade_color(cat_grade, passing) if cat_grade is not None else COLORS["muted"]
            cat_label = f"{cat_grade:.1f}" if cat_grade is not None else "—"

            st.markdown(
                f"<div style='display:flex;align-items:center;justify-content:space-between;"
                f"border-bottom:1px solid {COLORS['border']};padding-bottom:6px;margin:14px 0 8px'>"
                f"<span style='font-weight:600;font-size:14px'>{assessment['name']}</span>"
                f"<span style='font-size:11px;color:{COLORS['muted']}'>{pct(assessment['weight'])} &nbsp; "
                f"<span style='font-family:JetBrains Mono,monospace;color:{cat_color};font-weight:700'>{cat_label}</span></span>"
                f"</div>",
                unsafe_allow_html=True,
            )

            _render_item_table(assessment, term["id"], subj_idx, passing)

        # ── Term grade footer ──────────────────────────────────────────────────
        if term_grade is not None:
            t_color = grade_color(term_grade, passing)
            st.markdown("---")
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:12px;padding:4px 0'>"
                f"<span style='font-size:12px;color:{COLORS['muted']}'>Term Grade</span>"
                f"<div style='flex:1'>{grade_bar(term_grade, t_color, 6)}</div>"
                f"<span style='font-family:JetBrains Mono,monospace;font-size:18px;font-weight:700;color:{t_color}'>"
                f"{term_grade:.1f}</span></div>",
                unsafe_allow_html=True,
            )


# ── Main Render ────────────────────────────────────────────────────────────────

def render():
    page_header("📝 Grade Entry", "Enter scores for each assessment item.")

    tab_manage, tab_scores = st.tabs(["➕ Manage Subjects", "📊 Enter Scores"])

    # ══════════════════════════════════════════════════════════════════
    # TAB 1 — Manage subjects (add / remove)
    # ══════════════════════════════════════════════════════════════════
    with tab_manage:
        st.markdown("#### Add Subject")
        with st.form("add_subject_form", clear_on_submit=True):
            c1, c2, c3 = st.columns([3, 1.5, 1.5])
            name    = c1.text_input("Subject Name", placeholder="e.g. Mathematics, Physics…")
            passing = c2.number_input("Passing Grade", min_value=0.0, max_value=100.0, value=75.0, step=0.5)
            c3.markdown("<br>", unsafe_allow_html=True)
            submitted = c3.form_submit_button("➕ Add", use_container_width=True)

            if submitted:
                if not name.strip():
                    st.error("Enter a subject name.")
                elif any(s["name"].lower() == name.strip().lower() for s in st.session_state.subjects):
                    st.error(f'"{name.strip()}" already exists.')
                else:
                    st.session_state.subjects.append(create_subject(name.strip(), passing))
                    st.success(f'Added "{name.strip()}"', icon="✓")
                    st.rerun()

        if st.session_state.subjects:
            st.markdown("---")
            st.markdown("#### Your Subjects")
            header = st.columns([3, 2, 2, 1])
            for col, label in zip(header, ["Subject", "Passing Grade", "Terms Scored", ""]):
                col.markdown(
                    f"<span style='font-size:10px;color:{COLORS['muted']};text-transform:uppercase;letter-spacing:.08em'>{label}</span>",
                    unsafe_allow_html=True,
                )
            for i, s in enumerate(st.session_state.subjects):
                row = st.columns([3, 2, 2, 1])
                row[0].markdown(f"**{s['name']}**")
                row[1].markdown(f"<span style='color:{COLORS['amber']}'>{s['passing_grade']}</span>", unsafe_allow_html=True)
                scored = sum(1 for t in s["terms"] if any(a.get("items") for a in t["assessments"]))
                row[2].markdown(f"{scored} / {len(s['terms'])} terms")
                if row[3].button("🗑️", key=f"del_subj_{s['id']}"):
                    st.session_state.subjects.pop(i)
                    st.session_state.active_subject_idx = max(0, min(
                        st.session_state.active_subject_idx, len(st.session_state.subjects) - 1
                    ))
                    st.rerun()
        else:
            st.info("No subjects yet. Add one above.", icon="📚")

    # ══════════════════════════════════════════════════════════════════
    # TAB 2 — Score entry (item-based, Excel-like)
    # ══════════════════════════════════════════════════════════════════
    with tab_scores:
        if not st.session_state.subjects:
            st.info("Add subjects first in the 'Manage Subjects' tab.", icon="📚")
            return

        names = [s["name"] for s in st.session_state.subjects]
        sel   = st.selectbox(
            "Subject", names,
            index=min(st.session_state.active_subject_idx, len(names) - 1),
        )
        subj_idx = names.index(sel)
        st.session_state.active_subject_idx = subj_idx
        subject = st.session_state.subjects[subj_idx]

        st.caption(
            f"Passing grade: **{subject['passing_grade']}** — "
            "Enter individual scored items. Grades compute automatically."
        )
        st.markdown("")

        for term in subject["terms"]:
            _render_term(term, subj_idx, subject["passing_grade"])

        st.markdown("")
        st.success("✓ All changes are saved automatically.", icon="💾")


# Fix missing Optional import
from typing import Optional