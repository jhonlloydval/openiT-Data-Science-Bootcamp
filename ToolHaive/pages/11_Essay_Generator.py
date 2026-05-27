"""
pages/11_Essay_Generator.py — ToolHive AI

Essay & Content Generator.
Given a topic, tone, essay type, and optional reference context,
generate a well-structured draft the user can refine further.
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
    page_title="Essay Generator Hive — ToolHive AI",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title="Essay & Content Generator Hive",
    subtitle="Turn a topic into a structured draft — ready to refine",
    cover_class="cv-3",
)

# ── Config options ────────────────────────────────────────────────────────────
ESSAY_TYPES = {
    "Argumentative": (
        "Build a clear position with a claim, supporting arguments, "
        "counterargument acknowledgment, and a conclusion."
    ),
    "Expository": (
        "Explain the topic clearly and factually with a logical structure. "
        "No personal opinion — inform the reader."
    ),
    "Analytical": (
        "Break the topic into its components and examine relationships, "
        "causes, or implications. Go beyond surface-level description."
    ),
    "Reflective": (
        "Write in first person. Explore personal insight, lesson learned, "
        "or growth related to the topic."
    ),
    "Compare & Contrast": (
        "Identify two subjects from the topic, compare similarities, "
        "contrast differences, and draw a conclusion."
    ),
    "Blog Post / Article": (
        "Write in an engaging, readable tone for a general audience. "
        "Use a hook intro, clear body sections, and a closing call-to-action or takeaway."
    ),
}

TONES = [
    "Academic",
    "Formal",
    "Conversational",
    "Persuasive",
    "Simplified / Plain",
    "Creative",
]

LENGTHS = {
    "Short (~300 words)": 300,
    "Medium (~600 words)": 600,
    "Long (~1000 words)": 1000,
}

TOOL_PROMPT = """You are ToolHive's Essay & Content Generator Hive — a skilled academic
and professional writing assistant.

Your job is to produce a well-structured, coherent draft based on the user's
topic, essay type, tone, and optional reference context.

This is a DRAFT, not a final product. The user will revise it.

---

CORE RULES:
- Follow the essay type structure EXACTLY as instructed.
- Match the tone precisely — do not mix tones.
- If reference context is provided, use it to inform content. Do not fabricate facts.
- If no context is provided, write from general knowledge.
- Hit the approximate word count. Do not pad or cut severely.
- Never add a note saying "this is a draft" — just write the draft.

---

ESSAY STRUCTURE RULE:
Always include:
1. A clear title
2. An introduction with a hook and thesis/purpose statement
3. Well-developed body sections with logical flow
4. A conclusion that wraps up without introducing new ideas

Use Markdown headers for sections. Do not add meta-commentary.

---

STRICT RULES:
- Do NOT lecture the user about academic integrity.
- Do NOT add disclaimers about AI writing.
- Do NOT generate harmful, misleading, or fabricated factual claims.
- If the topic is too vague, make a reasonable scope decision and state it
  as the first sentence of the introduction (e.g., "This essay focuses on X
  aspect of [topic]").
"""

SYSTEM_PROMPT = scoped_system_prompt(
    tool_name="Essay & Content Generator Hive",
    tool_scope=(
        "Essay drafting, structured content generation, blog post writing, "
        "argumentative and expository writing, and academic draft creation "
        "from user-provided topics and optional reference material."
    ),
    tool_prompt=TOOL_PROMPT,
    refusal_message=(
        "This request is outside the scope of Essay & Content Generator Hive. "
        "I can only generate essay drafts and structured content from topics "
        "you provide."
    ),
)


def build_messages(
    topic: str,
    essay_type: str,
    tone: str,
    length_label: str,
    context: str,
) -> list[dict]:
    word_count = LENGTHS[length_label]
    type_guide = ESSAY_TYPES[essay_type]
    context_block = (
        f"\n\nReference context provided by user (use as source material):\n{context.strip()}"
        if context.strip()
        else "\n\nNo reference context provided — write from general knowledge."
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Topic: {topic.strip()}\n"
                f"Essay type: {essay_type}\n"
                f"Essay type guidance: {type_guide}\n"
                f"Tone: {tone}\n"
                f"Target length: approximately {word_count} words"
                f"{context_block}"
            ),
        },
    ]


# ── UI ────────────────────────────────────────────────────────────────────────
with tool_body_container():
    render_tool_tip(
        "Enter a topic, choose your essay type and tone, then optionally paste "
        "reference notes or text for the AI to draw from. The output is a starting draft — "
        "edit and refine it as needed."
    )

    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input(
            "Essay topic",
            placeholder="e.g. The impact of social media on student mental health",
        )
        essay_type = st.selectbox("Essay type", list(ESSAY_TYPES.keys()))
    with col2:
        tone = st.selectbox("Tone", TONES)
        length_label = st.selectbox("Approximate length", list(LENGTHS.keys()))

    context = st.text_area(
        "Reference notes or context (optional)",
        placeholder=(
            "Paste any source material, notes, key points, or text you want the AI to use. "
            "Leave blank to generate from general knowledge."
        ),
        height=160,
    )

    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        run = st.button("Generate Essay →", use_container_width=True)
    with col_btn2:
        if st.button("Clear", use_container_width=False):
            st.rerun()

    if run and topic.strip():
        messages = build_messages(topic, essay_type, tone, length_label, context)
        with st.spinner("Drafting your essay…"):
            result = chat(messages)
        render_section_divider()
        render_output_header(f"{essay_type} Essay Draft — {tone} Tone")
        st.markdown(result)
    elif run:
        st.warning("Please enter an essay topic first.")
