"""
pages/2_Document_Summarizer.py - ToolHive AI

Single-turn document summarizer. Integrated from the TBA summarizer contribution
and adapted to the shared ToolHive UI/model flow.

Assigned to: Iris
"""

import streamlit as st
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container
from utils.ollama_client import chat, scoped_system_prompt

st.set_page_config(
    page_title="Doc Summarizer Hive — ToolHive AI",
    page_icon="📄", layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title    = "Document Summarizer Hive",
    subtitle = "Turn pasted text into summaries, bullet points, or key takeaways",
    cover_class = "cv-2",
)

SUMMARY_STYLES = {
    "Structured Summary": """Return exactly these sections:

## Summary
2-3 sentences capturing the core message.

## Key Points
Bullet list of the most important facts, arguments, or findings.

## Action Items
Bullet list of any recommended actions, next steps, or decisions mentioned.
If there are no action items, write: None identified.""",
    "Short Summary": """Return exactly one concise paragraph of 3-5 sentences.
Capture the central message, main supporting points, and any important conclusion.
Do not use bullets.""",
    "Bullet Points": """Return 5-8 bullet points.
Each bullet should be specific, non-repetitive, and faithful to the source text.
Do not add a separate introduction or conclusion.""",
    "Key Takeaways": """Return exactly these sections:

## Key Takeaways
3-6 bullets covering the most useful insights.

## Why It Matters
1-2 sentences explaining the practical significance.

## Remember
One short sentence naming the single most important point.""",
}

TOOL_PROMPT = TOOL_PROMPT = """You are ToolHive's Document Summarizer Hive, a high-fidelity text compression and extraction system.

Your primary goal is to accurately reduce and restructure text WITHOUT changing meaning.

You are NOT an explainer. You are NOT an interpreter. You are a compressor.

---

CORE PRINCIPLE:
Every output must be fully traceable to the source text.
If a statement is not explicitly or directly implied by the text, you MUST NOT include it.

---

STRICT RULES:
You MUST:
- Only use information explicitly present in the input text
- Preserve meaning, tone, and level of certainty
- Merge repetition without adding new interpretation
- Keep names, numbers, dates, and claims unchanged
- Reflect uncertainty when the source is unclear

You MUST NOT:
- Add background knowledge or external context
- Infer causes, motivations, or implications not stated
- Reframe opinions as facts
- Introduce new categories, themes, or conclusions
- “Improve” the text beyond compression and clarity

---

STYLE CONTROL RULE:
Follow the selected summary style EXACTLY.
Do not mix formats or add extra sections.

If the format requires bullets, use only bullets.
If it requires paragraphs, use only paragraphs.

Do not improvise structure even if the text suggests it.

---

HANDLING UNCLEAR INPUT:
If the input is:
- vague
- contradictory
- low-information
- purely opinion-based

Then:
- Do NOT fill gaps
- Preserve ambiguity
- Clearly reflect uncertainty in wording (without adding analysis)

---

INFORMATION PRIORITY RULE:
Prioritize:
1. Explicit facts
2. Direct claims
3. Clearly stated conclusions
4. Only then minimal implied meaning (strictly necessary for coherence)

---

SAFETY & NEUTRALITY:
- Do not generate new instructions or advice not present in the source.
- Do not amplify harmful content; summarize it at a neutral, high level.
- Do not claim external verification or knowledge.

---

OUTPUT RULE:
- Return ONLY the formatted summary.
- No commentary, no introduction, no explanation, no meta text.
"""

SYSTEM_PROMPT = scoped_system_prompt(
    tool_name="Document Summarizer Hive",
    tool_scope="Summarizing, condensing, extracting key points, and identifying action items from user-provided documents or pasted text.",
    tool_prompt=TOOL_PROMPT,
    refusal_message="This request is outside the scope of Document Summarizer Hive. I can only summarize, condense, and extract key points from user-provided text.",
)


def build_messages(text: str, summary_style: str) -> list[dict]:
    """Create the model message list for the selected summary format."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Selected summary style: {summary_style}\n\n"
                f"Required output format:\n{SUMMARY_STYLES[summary_style]}\n\n"
                "Text to summarize:\n"
                f"{text.strip()}"
            ),
        },
    ]

# ── UI ────────────────────────────────────────────────────────────────────────
with tool_body_container():
    st.markdown("#### Paste your document or text below")
    summary_style = st.selectbox("Summary type", list(SUMMARY_STYLES.keys()))
    user_text = st.text_area(
        label       = "Document text",
        label_visibility = "collapsed",
        placeholder = "Paste an article, report, email, research paper, or any text here…",
        height      = 280,
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        run = st.button("Summarize →", use_container_width=True)
    with col2:
        if st.button("Clear", use_container_width=False):
            st.rerun()

    if run and user_text.strip():
        messages = build_messages(user_text, summary_style)
        with st.spinner("Analyzing…"):
            result = chat(messages)
        st.markdown(result)
    elif run:
        st.warning("Please paste some text first.")
