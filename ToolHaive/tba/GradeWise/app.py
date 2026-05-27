"""
Gradewise — Intelligent Academic Performance Tracking
Run: streamlit run app.py
"""

import importlib
import streamlit as st
from styles import apply_styles
from data.sample_subjects import get_sample_subjects

PAGES = {
    "🏠  Dashboard":    "pages.dashboard",
    "📝  Grade Entry":  "pages.grade_entry",
    "🔮  Forecasting":  "pages.forecasting",
    "🎲  Simulator":    "pages.simulator",
    "🎯  Goal Planner": "pages.goal_planner",
    "📊  Analytics":    "pages.analytics",
}


def init_session():
    defaults = {
        "subjects":           [],
        "active_subject_idx": 0,
        "chat_history":       [],
        "api_key":            "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="gw-logo">grade<span>wise</span></div>'
            '<div class="gw-tagline">Academic Intelligence</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="gw-divider"></div>', unsafe_allow_html=True)

        selected = st.radio("nav", list(PAGES.keys()), label_visibility="collapsed")

        st.markdown('<div class="gw-divider"></div>', unsafe_allow_html=True)

        # ── Subject selector ───────────────────────────────────────────────────
        if st.session_state.subjects:
            st.markdown('<p class="sidebar-label">Active Subject</p>', unsafe_allow_html=True)
            names = [s["name"] for s in st.session_state.subjects]
            idx   = min(st.session_state.active_subject_idx, len(names) - 1)
            chosen = st.selectbox("subject", names, index=idx, label_visibility="collapsed")
            st.session_state.active_subject_idx = names.index(chosen)
            st.caption(f"{len(st.session_state.subjects)} subject(s) loaded")
        else:
            st.markdown(
                '<div class="sidebar-empty">No subjects yet.<br>Go to Grade Entry to get started.</div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div class="gw-divider"></div>', unsafe_allow_html=True)

        # ── Sample data / clear ───────────────────────────────────────────────
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📋 Sample", use_container_width=True, help="Load demo data"):
                st.session_state.subjects = get_sample_subjects()
                st.session_state.active_subject_idx = 0
                st.session_state.chat_history = []
                st.rerun()
        with c2:
            if st.button("🗑️ Clear", use_container_width=True, help="Remove all data"):
                st.session_state.subjects = []
                st.session_state.active_subject_idx = 0
                st.session_state.chat_history = []
                st.rerun()

        st.markdown('<div class="gw-divider"></div>', unsafe_allow_html=True)

        # ── API Key ────────────────────────────────────────────────────────────
        st.markdown('<p class="sidebar-label">API Key <span style="opacity:.5">(AI features)</span></p>', unsafe_allow_html=True)
        key_input = st.text_input(
            "api_key", type="password",
            value=st.session_state.api_key,
            placeholder="gsk_... or sk-ant-...",
            label_visibility="collapsed",
        )
        if key_input:
            st.session_state.api_key = key_input
        if st.session_state.api_key:
            st.success("Key saved ✓", icon="🔑")

        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
        st.caption("Gradewise v1.0 · All data is session-local.")

    return selected


def main():
    st.set_page_config(
        page_title="Gradewise",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_styles()
    init_session()
    selected = render_sidebar()
    importlib.import_module(PAGES[selected]).render()


if __name__ == "__main__":
    main()