"""pages/13_About.py - ToolHaive AI · About & Limitations."""

import streamlit as st
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container

st.set_page_config(
    page_title="About — ToolHive AI",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="about")
render_tool_header(
    title="About ToolHive AI",
    subtitle="Project background, known limitations, and what comes next",
    cover_class="cv-8",
)

with tool_body_container():

    st.markdown("## Project Background")
    st.markdown("""
    **ToolHive AI** is a capstone project built for the openIT Data Science Bootcamp.
    It is a local, privacy-first AI workspace that runs entirely on your machine via
    [Ollama](https://ollama.com). No data is sent to external servers.

    The app was designed to demonstrate prompt engineering, scoped AI tools,
    model selection, and a custom tool builder — all within a 2-day build window.
    """)

    st.divider()

    st.markdown("## Document Sources")
    st.markdown("""
    | File | Purpose | Format |
    |---|---|---|
    | `ToolHive_Paper.pdf / .docx` | System design, tool taxonomy, workflow architecture | PDF, DOCX |
    | `toolhive_brand_guide.html` | UI visual identity and component design spec | HTML |

    **Preparation process:** These documents were reviewed manually and used to:
    - Define system prompt scope boundaries for each tool
    - Design the Custom Tool Builder schema
    - Inform the tool taxonomy and category structure
    """)

    st.divider()

    st.markdown("## Known Limitations")
    st.markdown("""
    - **No streaming** — responses appear all at once; long outputs feel slow
    - **No document retrieval** — tools use prompt engineering only, not embeddings or semantic search over the source files
    - **Local model quality** — phi4-mini and llama3.2 produce weaker outputs than larger cloud models on complex tasks
    - **No conversation memory across sessions** — chat history resets on page refresh
    - **Custom tools are stored locally** — saved to a JSON file; no cloud persistence or sharing
    - **Locked models** — gemma3, qwen, and cloud models (Claude, Gemini) are planned but not yet integrated
    """)

    st.divider()

    st.markdown("## Next Steps")
    st.markdown("""
    1. **Add streaming** — use Ollama's streaming API so responses render token by token
    2. **Add document retrieval** — embed `ToolHive_Paper.pdf` with `sentence-transformers` and serve a semantic search tool on top of it
    3. **Add conversation memory** — persist chat history to `st.session_state` across tool pages
    4. **Connect cloud models** — integrate Claude or Gemini via API for higher-quality outputs
    5. **Custom tool sharing** — export/import custom tools as JSON so teams can share prompt packs
    """)