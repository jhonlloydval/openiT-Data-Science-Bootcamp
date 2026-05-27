"""pages/14_Sources.py — ToolHive AI · Sources & Document Preparation."""

import os
import streamlit as st
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container

st.set_page_config(
    page_title="Sources — ToolHive AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="sources")
render_tool_header(
    title="Sources & Document Preparation",
    subtitle="Document sources, preparation process, and how they shaped ToolHive AI",
    cover_class="cv-2",
)

with tool_body_container():

    # ── Section 1: What sources were used ─────────────────────────────────────
    st.markdown("### 📄 Document Sources Used")
    st.markdown(
        """
        The following documents were collected and reviewed during the preparation phase of this project.
        They served as the primary knowledge base from which the tool architecture, system prompts,
        and scope boundaries were designed.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            **ToolHive Paper**
            - **Files:** `ToolHive_Paper.pdf`, `ToolHive_Paper.docx`
            - **Type:** Internal design and architecture document
            - **Covers:** System design rationale, tool taxonomy, AI workflow patterns,
              and the overall product vision for ToolHive AI
            - **Used for:** Defining the tool categories, naming conventions,
              and the scope rules encoded into each system prompt
            """
        )

    with col2:
        st.markdown(
            """
            **ToolHive Brand Guide**
            - **File:** `toolhive_brand_guide.html`
            - **Type:** Visual identity and UI specification document
            - **Covers:** Color system, typography, component patterns,
              and layout guidelines for the ToolHive interface
            - **Used for:** Building the CSS design system in `utils/ui.py`,
              including the navbar, tool cards, cover classes, and color tokens
            """
        )

    with col3:
        st.markdown(
            """
            **Ollama Model Documentation**
            - **Source:** [ollama.com/library](https://ollama.com/library)
            - **Type:** External public documentation
            - **Covers:** Available local models, API interface, and streaming support
            - **Used for:** Configuring `utils/ollama_client.py`, selecting
              phi4-mini as the default model, and planning the model selector feature
            """
        )

    st.divider()

    # ── Section 2: Preparation process ────────────────────────────────────────
    st.markdown("### 🔧 Preparation & Ingestion Process")
    st.markdown(
        """
        ToolHive AI uses **prompt-based document distillation** as its ingestion method.
        Rather than embedding documents into a vector store, the team manually reviewed
        each source document and extracted the relevant knowledge directly into structured
        system prompts. This approach was chosen because:

        - It is explainable, auditable, and easy to debug
        - It works reliably with small local models (phi4-mini, llama3.2)
        - It fits a 2-day build window without requiring a retrieval pipeline

        The table below maps each document to the part of the app it informed.
        """
    )

    st.markdown(
        """
        | Source Document | Extracted Into | How It Was Used |
        |---|---|---|
        | `ToolHive_Paper.pdf / .docx` | System prompts, tool scope definitions | Reviewed manually; key rules encoded into `scoped_system_prompt()` for each tool |
        | `toolhive_brand_guide.html` | `utils/ui.py` CSS design system | Parsed visually; color tokens, typography, and layout rules implemented directly |
        | Ollama model docs | `utils/ollama_client.py` | API endpoint, model names, and payload structure sourced from official docs |
        | Bootcamp lesson materials | Tool selection and AI workflow design | Informed the choice of prompt engineering over embeddings for the build window |
        """
    )

    st.divider()

    # ── Section 3: Source expander (quick reference) ───────────────────────────
    with st.expander("📂 View source files in this project"):
        files_dir = os.path.join(os.path.dirname(__file__), "..", "files")
        if os.path.exists(files_dir):
            files = [f for f in os.listdir(files_dir) if not f.startswith(".")]
            if files:
                for fname in sorted(files):
                    fpath = os.path.join(files_dir, fname)
                    size_kb = round(os.path.getsize(fpath) / 1024, 1)
                    st.markdown(f"- `{fname}` — {size_kb} KB")
            else:
                st.info("No files found in /files directory.")
        else:
            st.info("/files directory not found.")

    st.divider()

    # ── Section 4: Data quality & limitations note ─────────────────────────────
    st.markdown("### ⚠️ Data Quality Notes")
    st.markdown(
        """
        - **Coverage:** Sources cover the ToolHive system design and UI only.
          Individual tool knowledge (e.g. interview coaching, grammar checking)
          comes from the base model's pre-trained knowledge, not from retrieved documents.
        - **No real-time data:** ToolHive AI does not connect to the internet.
          All outputs are based on the local model and the system prompts encoded during preparation.
        - **No version tracking:** Document sources are not versioned.
          If the source files are updated, system prompts would need to be manually revised.
        - **Language:** All source documents are in English.
          Model outputs in other languages depend on the selected model's multilingual capability.
        """
    )