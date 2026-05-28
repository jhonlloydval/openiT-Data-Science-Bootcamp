"""pages/7_Fact_Checker.py - ToolHaive AI."""

import streamlit as st
from utils.ollama_client import chat, scoped_system_prompt
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container
from utils.rag import retrieve, ingest_text, collection_exists

st.set_page_config(
    page_title="Fact Checker Hive — ToolHaive AI",
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

# ── RAG collection name ───────────────────────────────────────────────────────
RAG_COLLECTION = "fact_checker"

TOOL_PROMPT = """You are a strict media literacy and credibility analysis assistant.

Your role is NOT to verify truth directly or claim access to real-time facts.
Instead, you evaluate the credibility, structure, and reliability of a claim using observable signals.

You must be careful, skeptical, and uncertainty-aware. Never present speculation as fact.

If information is missing or unverifiable, explicitly state uncertainty.

If reference material is provided under "Retrieved reference context", use it to
ground your analysis. If it contradicts the claim, say so explicitly. If it supports
the claim, note that. If it is not relevant, ignore it — do not force a connection.

---

Return EXACTLY the following sections in Markdown:

## Credibility Assessment
Classify the claim as one of:
- Likely Reliable
- Unclear / Insufficient Information
- Likely Misleading

Then provide a 1–2 sentence justification grounded only in reasoning signals (not external verification).

Do NOT state or imply you "checked" facts externally.

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


def build_messages(user_text: str) -> list[dict]:
    """Build the message list, augmenting the system prompt with RAG context if available."""
    context = retrieve(RAG_COLLECTION, user_text, top_k=3)

    if context:
        augmented_system = (
            SYSTEM_PROMPT
            + "\n\n---\n\nRetrieved reference context (use to ground your analysis):\n"
            + context
        )
    else:
        augmented_system = SYSTEM_PROMPT

    return [
        {"role": "system", "content": augmented_system},
        {"role": "user",   "content": user_text},
    ]


# ── UI ────────────────────────────────────────────────────────────────────────
with tool_body_container():

    # ── RAG: reference document ingestion (collapsible) ───────────────────────
    with st.expander(
        "Reference documents"
        + (" ✅ active" if collection_exists(RAG_COLLECTION) else " — none loaded"),
        expanded=False,
    ):
        st.caption(
            "Paste any reference text (articles, fact sheets, source documents) for the "
            "AI to use when checking claims. Each paste is added to the knowledge base."
        )
        ref_text   = st.text_area(
            "Reference text",
            placeholder="Paste a source document, article body, or reference material here…",
            height=160,
            key="fc_ref_text",
        )
        ref_doc_id = st.text_input(
            "Document label",
            placeholder="e.g. who_covid_brief, climate_report_2024",
            key="fc_ref_doc_id",
        )
        col_ingest, col_clear = st.columns([1, 1])
        if col_ingest.button("Add to knowledge base", key="fc_ingest"):
            if ref_text.strip() and ref_doc_id.strip():
                with st.spinner("Embedding and storing…"):
                    try:
                        n = ingest_text(RAG_COLLECTION, ref_text.strip(), ref_doc_id.strip())
                        st.success(f"Ingested {n} chunks from '{ref_doc_id}'.")
                    except Exception as e:
                        st.error(f"Ingestion failed: {e}")
            else:
                st.warning("Paste some text and enter a document label first.")

    # ── Main claim input ──────────────────────────────────────────────────────
    user_text = st.text_area(
        "Claim, headline, or article excerpt",
        placeholder="Paste a headline, social media claim, or article excerpt here...",
        height=260,
    )

    run = st.button("Analyze Credibility ->")
    if run and user_text.strip():
        messages = build_messages(user_text)
        with st.spinner("Reviewing credibility signals..."):
            result = chat(messages)
        st.markdown(result)
    elif run:
        st.warning("Please paste a claim or excerpt first.")
