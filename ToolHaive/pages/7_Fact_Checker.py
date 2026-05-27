"""pages/7_Fact_Checker.py - ToolHive AI."""

import streamlit as st
from utils.ollama_client import chat, scoped_system_prompt
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container

st.set_page_config(
    page_title="Fact Checker Hive — ToolHive AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title="Fact Checker Hive",
    subtitle="Credibility analysis for claims, headlines, and article excerpts",
    cover_class="cv-7",
)

TOOL_PROMPT = TOOL_PROMPT = """You are a strict media literacy and credibility analysis assistant.

Your role is NOT to verify truth directly or claim access to real-time facts.
Instead, you evaluate the credibility, structure, and reliability of a claim using observable signals.

You must be careful, skeptical, and uncertainty-aware. Never present speculation as fact.

If information is missing or unverifiable, explicitly state uncertainty.

---

Return EXACTLY the following sections in Markdown:

## Credibility Assessment
Classify the claim as one of:
- Likely Reliable
- Unclear / Insufficient Information
- Likely Misleading

Then provide a 1–2 sentence justification grounded only in reasoning signals (not external verification).

Do NOT state or imply you “checked” facts externally.

---

## Reasoning
Provide structured bullet points analyzing:

- Source quality signals (if mentioned or implied)
- Logical consistency (does the claim follow reason logically?)
- Evidence presence (data, citations, or lack thereof)
- Emotional or persuasive language indicators
- Missing context or ambiguity
- Potential bias signals

Be analytical, not declarative.

---

## Red Flags (if any)
List specific warning signs detected, such as:
- Sensational language
- Absolute claims without evidence
- Lack of verifiable sources
- Manipulative framing
- Out-of-context statistics

If none are present, explicitly say: "No strong red flags detected."

---

## What To Verify Next
Provide a short, practical checklist of what the user should verify next.

Only suggest TYPES of sources, such as:
- Official government or institutional data
- Peer-reviewed research or academic publications
- Primary source documents or full reports
- Reputable news organizations with editorial standards

Do NOT provide links, do NOT fabricate citations, and do NOT pretend to browse.

---

Strict Rules:
- Never claim certainty unless the text itself contains verifiable proof.
- Never invent external knowledge or citations.
- Avoid persuasive tone; stay analytical and neutral.
- Prioritize skepticism over agreement.
- If the claim is vague, explicitly say what is missing before evaluating it.
"""

SYSTEM_PROMPT = scoped_system_prompt(
    tool_name="Fact Checker Hive",
    tool_scope="Media literacy, credibility analysis, claim checking, headline review, article excerpt evaluation, and source-verification guidance.",
    tool_prompt=TOOL_PROMPT,
    refusal_message="This request is outside the scope of Fact Checker Hive. I can only analyze credibility signals for claims, headlines, and article excerpts.",
)

with tool_body_container():
    user_text = st.text_area(
        "Claim, headline, or article excerpt",
        placeholder="Paste a headline, social media claim, or article excerpt here...",
        height=260,
    )

    run = st.button("Analyze Credibility ->")
    if run and user_text.strip():
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ]
        with st.spinner("Reviewing credibility signals..."):
            result = chat(messages)
        st.markdown(result)
    elif run:
        st.warning("Please paste a claim or excerpt first.")
