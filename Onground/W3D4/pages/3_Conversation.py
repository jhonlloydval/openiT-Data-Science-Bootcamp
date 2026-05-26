import streamlit as st
import requests

st.set_page_config(page_title="Conversation", layout="wide", page_icon="✦")

st.markdown("""
<style>
.header { background: #0f2744; padding: 24px 28px; border-radius: 14px; margin-bottom: 22px; }
.header h1 { font-size: 1.6rem; color: #fff; font-weight: 700; margin: 0 0 4px; }
.header p  { color: #93b8d8; font-size: 0.88rem; margin: 0; }
.tip { background: #eef4ff; border: 1px solid #bed0ff; border-radius: 10px;
       padding: 14px 16px; font-size: 0.85rem; color: #1a3a6b; margin-bottom: 16px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
  <h1>✦ Page 3 — Conversation</h1>
  <p>A multi-turn writing assistant that remembers your edits across the session.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="tip">📖 <strong>What this page teaches:</strong> How <code>st.session_state</code> keeps a conversation history so the model remembers what was said earlier in the same session.</div>', unsafe_allow_html=True)

# Session state — initialize with writing assistant system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are QuillBot, an expert writing assistant. "
            "You can paraphrase, fix grammar, summarize, expand, and improve text. "
            "Remember the full conversation so the user can ask follow-up edits like "
            "'make that more formal' or 'now shorten it'. "
            "Always return clean, polished text."
        )}
    ]

# Render conversation history (skip system message)
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Paste text to improve, or ask a follow-up like 'make it shorter'…")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    payload = {
        "model": "llama3.2",
        "messages": st.session_state.messages,
        "stream": False
    }

    with st.spinner("QuillBot is thinking…"):
        response = requests.post("http://localhost:11434/api/chat", json=payload)
        reply = response.json()["message"]["content"]

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

st.markdown("---")
st.markdown("""
**Try this flow:**
1. Paste a paragraph and ask QuillBot to paraphrase it
2. Then say *"make it more formal"*
3. Then say *"now summarize it in one sentence"*

The model remembers all previous edits because the full `messages` list is sent every time.

**Activity:** What happens if you click the browser refresh? Why does the history disappear?
""")

if st.button("🗑 Clear conversation"):
    del st.session_state.messages
    st.rerun()