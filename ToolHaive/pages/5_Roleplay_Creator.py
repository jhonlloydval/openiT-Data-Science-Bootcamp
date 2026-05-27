"""
pages/5_Roleplay_Creator.py — ToolHive AI
Assigned to: Lloyd
"""

import streamlit as st
from utils.ui import inject_styles, render_navbar, render_tool_header, tool_body_container
from utils.ollama_client import chat, scoped_system_prompt

st.set_page_config(
    page_title="Roleplay Creator Hive — ToolHive AI",
    page_icon="🎭", layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title    = "Roleplay Creator Hive",
    subtitle = "Configure an AI persona · Structured in-character conversation",
    cover_class = "cv-5",
)

# ── Config form (shows only before conversation starts) ───────────────────────
if "rp_started" not in st.session_state:
    st.session_state.rp_started   = False
    st.session_state.rp_messages  = []

if not st.session_state.rp_started:
    with tool_body_container():
        st.markdown("#### Configure your AI character")
        char_name  = st.text_input("Character name",        placeholder="e.g. Marie Curie, a strict hiring manager, a Socratic tutor…")
        char_role  = st.text_input("Role / background",     placeholder="e.g. Nobel Prize-winning physicist, 1890s France")
        char_tone  = st.selectbox("Behavioural tone",       ["Formal & precise", "Encouraging mentor", "Strict & challenging", "Friendly & casual", "Mysterious & cryptic"])
        char_topic = st.text_input("Topic / scenario",      placeholder="e.g. Discuss the discovery of radium")

        if st.button("Start Roleplay →"):
            if char_name and char_role:
                roleplay_prompt = (
                    f"You are {char_name}. Background: {char_role}. "
                    f"Tone: {char_tone}. Topic/scenario: {char_topic or 'open conversation'}. "
                    "Remain in character for the configured roleplay. Do not break character or acknowledge being an AI "
                    "unless the user types exactly: /exit — in which case, step out of character and close the session warmly."
                )
                sys_prompt = scoped_system_prompt(
                    tool_name="Roleplay Creator Hive",
                    tool_scope="Configured roleplay, persona-based learning, interview/customer/training simulations, character practice, and structured scenario conversation.",
                    tool_prompt=roleplay_prompt,
                    refusal_message="This request is outside the scope of Roleplay Creator Hive. I can only assist with the configured roleplay character, scenario, or training conversation.",
                )
                st.session_state.rp_messages = [{"role": "system", "content": sys_prompt}]
                st.session_state.rp_started  = True
                st.rerun()
            else:
                st.warning("Please enter at least a character name and role.")
else:
    prompt = st.chat_input("Speak to the character… (type /exit to end)")
    if prompt:
        if prompt.strip().lower() == "/exit":
            st.session_state.rp_started  = False
            st.session_state.rp_messages  = []
            st.rerun()
        st.session_state.rp_messages.append({"role": "user", "content": prompt})

    # ── Active conversation ───────────────────────────────────────────────────
    with tool_body_container():
        for msg in st.session_state.rp_messages[1:]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt:
            with st.chat_message("assistant"):
                with st.spinner("Thinking…"):
                    reply = chat(st.session_state.rp_messages)
                st.markdown(reply)
            st.session_state.rp_messages.append({"role": "assistant", "content": reply})
            st.rerun()

        if st.button("New Character"):
            st.session_state.rp_started  = False
            st.session_state.rp_messages  = []
            st.rerun()
