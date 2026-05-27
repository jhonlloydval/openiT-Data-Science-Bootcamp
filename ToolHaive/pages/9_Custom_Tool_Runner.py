"""pages/9_Custom_Tool_Runner.py - ToolHive AI."""

import json
import os
import re

import streamlit as st
from utils.ollama_client import chat
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container

st.set_page_config(
    page_title="Custom Tool Builder - ToolHive AI",
    page_icon="➕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title="Custom Tool Builder",
    subtitle="Create and run your own prompt-powered assistant",
    cover_class="cv-8",
)

CUSTOM_TOOLS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "custom_tools.json")
CATEGORY_OPTIONS = ["professional", "academic", "education", "wellness", "media", "custom"]


def load_custom_tools() -> list[dict]:
    try:
        if os.path.exists(CUSTOM_TOOLS_PATH):
            with open(CUSTOM_TOOLS_PATH) as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
    except Exception:
        return []
    return []


def save_custom_tools(tools: list[dict]) -> None:
    os.makedirs(os.path.dirname(CUSTOM_TOOLS_PATH), exist_ok=True)
    with open(CUSTOM_TOOLS_PATH, "w") as f:
        json.dump(tools, f, indent=2)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "custom_tool"


with tool_body_container():
    build_tab, run_tab = st.tabs(["Build Tool", "Run Custom Tool"])

    with build_tab:
        with st.form("custom_tool_form"):
            name = st.text_input("Tool name", placeholder="e.g. Email Tone Rewriter")
            description = st.text_area(
                "Description",
                placeholder="What does this assistant help the user do?",
                height=90,
            )
            target_user = st.text_input("Target user", placeholder="e.g. students, HR staff, small business owners")
            category = st.selectbox("Category", CATEGORY_OPTIONS, index=len(CATEGORY_OPTIONS) - 1)
            system_prompt = st.text_area(
                "System prompt",
                placeholder="Define the assistant role, rules, and response format...",
                height=180,
            )
            input_placeholder = st.text_area(
                "Input placeholder",
                placeholder="Tell the user what to paste or describe...",
                height=80,
            )
            output_format = st.text_area(
                "Output format instruction",
                placeholder="e.g. Return sections for Summary, Recommendations, and Next Steps.",
                height=100,
            )
            submitted = st.form_submit_button("Save Custom Tool")

        if submitted:
            if name.strip() and system_prompt.strip():
                tools = load_custom_tools()
                tool_id = slugify(name)
                tools.append({
                    "id": tool_id,
                    "name": name.strip(),
                    "desc": description.strip() or "A custom prompt-powered assistant.",
                    "user": target_user.strip() or "User-created assistant",
                    "cat": category,
                    "cat_label": category.title(),
                    "turn": "single",
                    "cover": "cv-8",
                    "page": "/Custom_Tool_Runner",
                    "system_prompt": system_prompt.strip(),
                    "input_placeholder": input_placeholder.strip() or "Enter your request...",
                    "output_format": output_format.strip(),
                })
                save_custom_tools(tools)
                st.success("Custom tool saved. It will appear in the Tools Library.")
            else:
                st.warning("Tool name and system prompt are required.")

    with run_tab:
        custom_tools = load_custom_tools()
        if not custom_tools:
            st.info("No custom tools saved yet. Build one in the first tab.")
        else:
            tool_names = [tool.get("name", f"Custom Tool {i + 1}") for i, tool in enumerate(custom_tools)]
            selected_name = st.selectbox("Choose a custom tool", tool_names)
            selected_tool = custom_tools[tool_names.index(selected_name)]
            user_input = st.text_area(
                "Input",
                placeholder=selected_tool.get("input_placeholder", "Enter your request..."),
                height=220,
            )
            if st.button("Run Custom Tool ->"):
                if user_input.strip():
                    system_prompt = selected_tool.get("system_prompt", "")
                    output_format = selected_tool.get("output_format", "")
                    if output_format:
                        system_prompt = f"{system_prompt}\n\nOutput format:\n{output_format}"
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input},
                    ]
                    with st.spinner("Running custom tool..."):
                        result = chat(messages)
                    st.markdown(result)
                else:
                    st.warning("Please enter input for the selected custom tool.")
