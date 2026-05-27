"""pages/10_General_AI.py - ToolHive AI."""

import streamlit as st
from utils.ollama_client import MODEL, MODEL_OPTIONS, chat
from utils.ui import inject_styles, render_html, render_navbar, render_tool_header

st.set_page_config(
    page_title="HAIVE — ToolHive AI",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_navbar(active="dashboard")
render_tool_header(
    title="HAIVE",
    subtitle="Your hive for open-ended ideas, drafts, study, and problem solving",
    cover_class="cv-1",
)

render_html("""
<style>
.st-key-haive-main {
  max-width: 1180px; margin: 0 auto; padding: 28px 48px 120px;
  background: var(--cream-light); min-height: calc(100vh - 200px);
}
.st-key-haive-model-bar {
  background: rgba(255,255,255,0.86);
  border: 1px solid rgba(0,56,115,0.1);
  border-radius: 16px; padding: 18px 20px; margin-bottom: 24px;
  box-shadow: 0 18px 42px rgba(0,56,115,0.08);
}
.haive-model-kicker {
  font-family: var(--font-mono); font-size: 9px; letter-spacing: 0.16em;
  text-transform: uppercase; color: var(--ink-muted); margin-bottom: 10px;
}
.haive-model-locks {
  display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px;
}
.haive-model-pill {
  display: inline-flex; align-items: center; gap: 8px; padding: 7px 10px;
  border-radius: 999px; border: 1px solid rgba(0,56,115,0.12);
  background: rgba(10,22,40,0.04); color: rgba(42,58,92,0.5);
  font-family: var(--font-mono); font-size: 9px; letter-spacing: 0.06em;
  text-transform: uppercase; pointer-events: none;
}
.haive-model-pill span {
  border-left: 1px solid rgba(0,56,115,0.14); padding-left: 8px;
  color: rgba(42,58,92,0.38);
}
.haive-empty-state {
  border: 1px solid rgba(0,56,115,0.1);
  background:
    linear-gradient(135deg,rgba(255,255,255,0.88),rgba(255,255,255,0.64)),
    linear-gradient(135deg,rgba(0,57,115,0.06),rgba(122,177,227,0.1));
  border-radius: 18px; padding: 34px; margin-top: 10px;
}
.haive-empty-title {
  font-family: var(--font-display); font-size: 28px; font-weight: 800;
  color: var(--ink); letter-spacing: 0; line-height: 1.1;
}
.haive-empty-sub {
  color: var(--ink-muted); font-size: 14px; line-height: 1.7;
  max-width: 620px; margin-top: 10px;
}
.haive-prompts {
  display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; margin-top: 24px;
}
.haive-prompt {
  border: 1px solid rgba(0,56,115,0.1); background: white; border-radius: 12px;
  padding: 14px; color: var(--ink-mid); font-size: 12px; line-height: 1.45;
}
.haive-prompt strong {
  display: block; font-family: var(--font-mono); font-size: 9px;
  letter-spacing: 0.12em; text-transform: uppercase; color: var(--navy-mid);
  margin-bottom: 6px;
}
.st-key-haive-main [data-testid="stChatMessage"] {
  background: rgba(255,255,255,0.74);
  border: 1px solid rgba(0,56,115,0.08);
  border-radius: 16px; padding: 10px 16px; margin-bottom: 12px;
}
.st-key-haive-main [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
  background: rgba(0,86,163,0.06);
}
.st-key-haive-model-bar .stButton button {
  width: 100%;
}
@media (max-width: 900px) {
  .st-key-haive-main { padding: 22px 22px 110px; }
  .haive-prompts { grid-template-columns: repeat(2,1fr); }
}
@media (max-width: 560px) {
  .haive-prompts { grid-template-columns: 1fr; }
}
</style>
""")

available_models = [
    model_id
    for model_id, option in MODEL_OPTIONS.items()
    if option.get("status") == "available"
]
tba_models = [
    model_id
    for model_id, option in MODEL_OPTIONS.items()
    if option.get("status") != "available"
]

if "general_ai_messages" not in st.session_state:
    st.session_state.general_ai_messages = []

prompt = st.chat_input("Ask HAIVE anything...")
if prompt:
    st.session_state.general_ai_messages.append({"role": "user", "content": prompt})


def model_label(model_id: str) -> str:
    option = MODEL_OPTIONS.get(model_id, {})
    label = str(option.get("label") or model_id)
    if option.get("default"):
        return f"{label} (Default)"
    return label


locked_model_html = "".join(
    f"""
    <div class="haive-model-pill">
      {MODEL_OPTIONS[model_id].get("label", model_id)}
      <span>🔒 Coming Soon</span>
    </div>
    """
    for model_id in tba_models
)

with st.container(key="haive-main"):
    with st.container(key="haive-model-bar"):
        model_col, action_col = st.columns([4, 1.1], vertical_alignment="bottom")
        with model_col:
            render_html('<div class="haive-model-kicker">Active model</div>')
            selected_model = st.segmented_control(
                "Model",
                options=available_models,
                default=MODEL,
                format_func=model_label,
                label_visibility="collapsed",
            ) or MODEL
            if locked_model_html:
                render_html(f'<div class="haive-model-locks">{locked_model_html}</div>')
        with action_col:
            if st.button(
                "Clear Chat",
                disabled=not bool(st.session_state.general_ai_messages),
                use_container_width=True,
            ):
                st.session_state.general_ai_messages = []
                st.rerun()

    for msg in st.session_state.general_ai_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt:
        with st.chat_message("assistant"):
            with st.spinner("HAIVE is thinking..."):
                reply = chat(st.session_state.general_ai_messages, model=selected_model)
            st.markdown(reply)
        st.session_state.general_ai_messages.append({"role": "assistant", "content": reply})
        st.rerun()

    if not st.session_state.general_ai_messages:
        render_html("""
        <div class="haive-empty-state">
          <div class="haive-empty-title">What should HAIVE help shape today?</div>
          <div class="haive-empty-sub">
            Start with a question, a rough idea, a messy draft, a concept to study,
            or a problem you want to think through.
          </div>
          <div class="haive-prompts">
            <div class="haive-prompt"><strong>Draft</strong>Turn my notes into a polished announcement.</div>
            <div class="haive-prompt"><strong>Learn</strong>Explain this topic step by step with examples.</div>
            <div class="haive-prompt"><strong>Plan</strong>Create a practical study or project roadmap.</div>
            <div class="haive-prompt"><strong>Think</strong>Help me compare options and decide what to do next.</div>
          </div>
        </div>
        """)
