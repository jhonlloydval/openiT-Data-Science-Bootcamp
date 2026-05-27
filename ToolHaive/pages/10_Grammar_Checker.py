"""
pages/10_Grammar_Checker.py — ToolHive AI

Grammar & Writing Quality Checker.
Paste any text to get grammar corrections, style suggestions, and a
clarity score — without changing the author's voice or meaning.
"""

import streamlit as st
from utils.ui import (
    inject_styles,
    render_navbar,
    render_tool_header,
    render_tool_tip,
    render_output_header,
    render_section_divider,
    tool_body_container,
)
from utils.ollama_client import chat, scoped_system_prompt

st.set_page_config(
    page_title="Grammar Checker Hive — ToolHive AI",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title="Grammar & Writing Checker Hive",
    subtitle="Catch errors, improve clarity, and strengthen your writing",
    cover_class="cv-2",
)

# ── Check modes ───────────────────────────────────────────────────────────────
CHECK_MODES = {
    "Full Check": (
        "Perform a comprehensive grammar, spelling, punctuation, clarity, "
        "and style review."
    ),
    "Grammar & Spelling Only": (
        "Focus exclusively on grammar errors and spelling mistakes. "
        "Do not comment on style or tone."
    ),
    "Clarity & Readability": (
        "Focus on sentence structure, wordiness, passive voice, and how "
        "easy the text is to read. Do not rewrite — highlight problems."
    ),
    "Academic Tone Check": (
        "Evaluate whether the text meets academic writing standards: "
        "formal tone, precise vocabulary, citation-ready structure, "
        "and absence of colloquial language."
    ),
}

TOOL_PROMPT = """You are ToolHive's Grammar & Writing Checker Hive — a precise,
constructive writing quality analyst.

Your job is to help the user improve their writing WITHOUT changing their voice,
meaning, or intended structure.

You are NOT a rewriter. You are a reviewer and advisor.

---

CORE RULES:
- Point out specific errors with their location (quote the problematic phrase).
- Explain WHY each issue is a problem in one short sentence.
- Suggest the corrected version using → notation.
- Do NOT rewrite entire paragraphs.
- Preserve the author's tone and intent.
- If the text is already well-written, say so clearly.

---

RETURN EXACTLY these sections in Markdown:

## Writing Quality Score
Give an overall score from 1–10 with a one-sentence justification.
Format: **Score: X/10** — [reason]

## Grammar & Spelling Issues
List each issue found. If none, write: ✅ No grammar or spelling errors found.
Format per issue:
- ❌ "[quoted text]" → "[corrected text]" — [brief reason]

## Clarity & Style Observations
Bullet list of style-level observations (wordiness, passive voice, vague terms, etc.).
If none, write: ✅ No major clarity issues found.

## Top 3 Improvement Suggestions
Three prioritized, actionable writing tips specific to this text.
Do NOT give generic advice — tie each to something you actually found.

---

STRICT RULES:
- Never invent errors that are not present.
- Never change the meaning of any sentence.
- Keep feedback professional and constructive — not harsh.
- If the selected mode restricts scope, stay strictly within that scope.
"""

SYSTEM_PROMPT = scoped_system_prompt(
    tool_name="Grammar & Writing Checker Hive",
    tool_scope=(
        "Grammar checking, spelling correction, punctuation review, clarity "
        "analysis, style feedback, and academic tone evaluation for "
        "user-provided text."
    ),
    tool_prompt=TOOL_PROMPT,
    refusal_message=(
        "This request is outside the scope of Grammar & Writing Checker Hive. "
        "I can only review and improve grammar, spelling, clarity, and style "
        "for text you provide."
    ),
)


def build_messages(text: str, mode: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Check mode: {mode}\n"
                f"Focus instruction: {CHECK_MODES[mode]}\n\n"
                f"Text to review:\n{text.strip()}"
            ),
        },
    ]


# ── UI ────────────────────────────────────────────────────────────────────────
with tool_body_container():
    render_tool_tip(
        "Paste any text below — essay, email, report, or paragraph. "
        "Choose a check mode and the AI will review it without rewriting your words."
    )

    mode = st.selectbox("Check mode", list(CHECK_MODES.keys()))
    user_text = st.text_area(
        label="Text to check",
        label_visibility="collapsed",
        placeholder="Paste your text here…",
        height=280,
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        run = st.button("Check Writing →", use_container_width=True)
    with col2:
        if st.button("Clear", use_container_width=False):
            st.rerun()

    if run and user_text.strip():
        messages = build_messages(user_text, mode)
        with st.spinner("Reviewing your writing…"):
            result = chat(messages)
        render_section_divider()
        render_output_header("Writing Review")
        st.markdown(result)
    elif run:
        st.warning("Please paste some text first.")
