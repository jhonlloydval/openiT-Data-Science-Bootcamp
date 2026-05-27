"""
pages/3_Document_Paraphraser.py - ToolHive AI

Integrated from the TBA paraphraser contribution and adapted to the shared
ToolHive UI/model flow.

Assigned to: Iris
"""

import streamlit as st
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container
from utils.ollama_client import chat, scoped_system_prompt

st.set_page_config(
    page_title="Doc Paraphraser Hive — ToolHive AI",
    page_icon="✏️", layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title    = "Document Paraphraser Hive",
    subtitle = "Rewrite text in a clearer tone while preserving meaning",
    cover_class = "cv-3",
)

TONE_GUIDES = {
    "Academic": (
        "Use scholarly, precise language suitable for essays, reports, and "
        "research writing. Keep claims measured and evidence-aware."
    ),
    "Formal": (
        "Use polished professional language suitable for official, corporate, "
        "or administrative documents."
    ),
    "Casual": (
        "Use natural, friendly language that sounds like a clear conversation "
        "with a peer while staying respectful."
    ),
    "Simplified": (
        "Use plain language, shorter sentences, and common words. Preserve the "
        "same facts and level of detail without talking down to the reader."
    ),
}

TOOL_PROMPT = TOOL_PROMPT = TOOL_PROMPT = """You are a sharp, no-nonsense fact-checking analyst.
When given a claim, headline, or article excerpt, you analyze it critically
and give the user a clear, honest assessment they can actually use.

Your analysis must always include:

**Verdict** — one of: Likely True / Likely False / Misleading / Unverifiable
Give a direct 2-3 sentence explanation of WHY. Be specific to the claim.

**What makes this credible or not**
Talk about the language used, whether sources are named, whether the claim
is specific or vague, whether it follows logic, and whether emotional
manipulation is present. Be direct and concrete.

**Red Flags**
Call out specific suspicious elements in plain language.
If none exist, say so clearly.

**What to check next**
Give 2-3 specific, actionable steps the user can take to verify this themselves.
Name the TYPE of source (e.g. CDC website, court records, official press release)
but do not fabricate links.

Tone rules:
- Sound like a smart, trusted analyst — not a legal document
- Be direct. Avoid filler phrases like "it is worth noting that"
- If a claim is clearly false or manipulative, say so plainly
- Keep total response under 300 words unless the claim is very complex
- Never start a section with a disclaimer about your own limitations
"""

SYSTEM_PROMPT = scoped_system_prompt(
    tool_name="Document Paraphraser Hive",
    tool_scope="Paraphrasing, rewriting, clarifying, improving tone, and editing user-provided text while preserving meaning.",
    tool_prompt=TOOL_PROMPT,
    refusal_message="This request is outside the scope of Document Paraphraser Hive. I can only paraphrase, rewrite, and improve user-provided text.",
)


def build_messages(text: str, tone: str) -> list[dict]:
    """Create the model message list for a meaning-preserving paraphrase."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Selected tone: {tone}\n"
                f"Tone guide: {TONE_GUIDES[tone]}\n\n"
                "Text to paraphrase:\n"
                f"{text.strip()}"
            ),
        },
    ]


with tool_body_container():
    tone = st.selectbox("Select output tone", list(TONE_GUIDES.keys()))
    user_text = st.text_area(
        label            = "Your text",
        label_visibility = "collapsed",
        placeholder      = "Paste the text you want to paraphrase…",
        height           = 260,
    )

    run = st.button("Paraphrase →", use_container_width=False)
    if run and user_text.strip():
        messages = build_messages(user_text, tone)
        with st.spinner(f"Rewriting in {tone} tone…"):
            result = chat(messages)
        st.markdown(f"**{tone} version:**")
        st.markdown(result)
    elif run:
        st.warning("Please paste some text first.")
