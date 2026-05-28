"""
pages/12_Quiz_Flashcard_Generator.py — ToolHaive AI

Quiz & Flashcard Generator.
Paste notes or a document excerpt and get quiz questions or flashcards
ready for studying or classroom use.
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
    page_title="Quiz & Flashcard Generator Hive — ToolHaive AI",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title="Quiz & Flashcard Generator Hive",
    subtitle="Turn notes into quiz questions or flashcards — instantly",
    cover_class="cv-4",
)

# ── Output modes ──────────────────────────────────────────────────────────────
OUTPUT_MODES = {
    "Multiple Choice Quiz": (
        "Generate multiple choice questions with 4 options (A–D). "
        "Mark the correct answer clearly. Mix easy and harder questions."
    ),
    "True / False Quiz": (
        "Generate True/False questions from the text. "
        "After each question, state the answer and a one-sentence explanation."
    ),
    "Short Answer Quiz": (
        "Generate open-ended short answer questions. "
        "After each question, provide the model answer in 1–3 sentences."
    ),
    "Flashcards (Term → Definition)": (
        "Generate flashcards. Each card has a TERM on the front and a "
        "clear DEFINITION or explanation on the back. "
        "Format: **Term:** [term] | **Definition:** [definition]"
    ),
    "Flashcards (Question → Answer)": (
        "Generate flashcards in question-and-answer format. "
        "Format: **Q:** [question] | **A:** [answer]"
    ),
}

DIFFICULTY_LEVELS = {
    "Mixed (recommended)": (
        "Include a range: roughly 30% easy recall, 40% medium application, "
        "30% harder analysis or inference."
    ),
    "Easy — Recall": (
        "Focus on direct recall of facts, terms, and definitions stated "
        "explicitly in the text."
    ),
    "Medium — Understanding": (
        "Ask questions that require understanding relationships, "
        "causes, or implications within the text."
    ),
    "Hard — Analysis": (
        "Ask questions that require the student to infer, compare, evaluate, "
        "or apply ideas from the text."
    ),
}

QUANTITY_OPTIONS = ["5", "8", "10", "15", "20"]

TOOL_PROMPT = """You are ToolHaive's Quiz & Flashcard Generator Hive — a precise
educational content creator for students and educators.

Your job is to convert user-provided notes or text into high-quality quiz
questions or flashcards for study purposes.

---

CORE RULES:
- All questions and flashcards must be GROUNDED in the provided text.
- Do NOT invent facts not present in the source material.
- Do NOT repeat the same concept in multiple questions.
- Make questions specific — avoid vague or trick questions.
- Every question must have a clear, unambiguous correct answer.
- Number all items sequentially (1, 2, 3…).

---

QUALITY RULES:
- For multiple choice: all distractors (wrong options) must be plausible.
- For flashcards: definitions must be concise but complete.
- For short answer: model answers must be accurate and brief.
- Avoid questions answerable without reading the text (e.g., common sense).

---

FORMAT RULES:
- Follow the selected output format EXACTLY.
- Use the specified difficulty distribution.
- Hit the requested quantity exactly.
- Use Markdown. Keep output clean and easy to read.

---

STRICT RULES:
- Do NOT add commentary, introductions, or meta-text.
- Do NOT generate harmful, misleading, or fabricated content.
- If the input text is too short for the requested quantity,
  generate as many unique questions as possible and note the limitation.
"""

SYSTEM_PROMPT = scoped_system_prompt(
    tool_name="Quiz & Flashcard Generator Hive",
    tool_scope=(
        "Quiz question generation, flashcard creation, multiple choice, "
        "true/false, short answer, and term-definition card creation "
        "from user-provided notes or text."
    ),
    tool_prompt=TOOL_PROMPT,
    refusal_message=(
        "This request is outside the scope of Quiz & Flashcard Generator Hive. "
        "I can only generate quiz questions and flashcards from notes or text "
        "you provide."
    ),
)


def build_messages(
    text: str,
    output_mode: str,
    difficulty: str,
    quantity: str,
) -> list[dict]:
    mode_guide = OUTPUT_MODES[output_mode]
    diff_guide = DIFFICULTY_LEVELS[difficulty]
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Output mode: {output_mode}\n"
                f"Format instruction: {mode_guide}\n\n"
                f"Difficulty: {difficulty}\n"
                f"Difficulty instruction: {diff_guide}\n\n"
                f"Quantity: {quantity} items\n\n"
                f"Source notes / text:\n{text.strip()}"
            ),
        },
    ]


# ── UI ────────────────────────────────────────────────────────────────────────
with tool_body_container():
    render_tool_tip(
        "Paste your notes, a textbook excerpt, or any study material below. "
        "Choose a quiz format, difficulty, and how many items you want."
    )

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        output_mode = st.selectbox("Output format", list(OUTPUT_MODES.keys()))
    with col2:
        difficulty = st.selectbox("Difficulty", list(DIFFICULTY_LEVELS.keys()))
    with col3:
        quantity = st.selectbox("Number of items", QUANTITY_OPTIONS, index=2)

    user_text = st.text_area(
        label="Notes or source text",
        label_visibility="collapsed",
        placeholder=(
            "Paste your notes, lecture summary, textbook excerpt, "
            "or any study material here…"
        ),
        height=300,
    )

    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        run = st.button("Generate →", use_container_width=True)
    with col_btn2:
        if st.button("Clear", use_container_width=False):
            st.rerun()

    if run and user_text.strip():
        messages = build_messages(user_text, output_mode, difficulty, quantity)
        with st.spinner(f"Generating {quantity} {output_mode.lower()}…"):
            result = chat(messages)
        render_section_divider()
        render_output_header(f"{output_mode} — {difficulty}")
        st.markdown(result)
    elif run:
        st.warning("Please paste some notes or source text first.")
