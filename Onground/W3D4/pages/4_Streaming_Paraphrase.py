import streamlit as st
import requests
import json

st.set_page_config(page_title="Streaming Paraphrase", layout="wide", page_icon="✦")

st.markdown("""
<style>
.header { background: #0f2744; padding: 24px 28px; border-radius: 14px; margin-bottom: 22px; }
.header h1 { font-size: 1.6rem; color: #fff; font-weight: 700; margin: 0 0 4px; }
.header p  { color: #93b8d8; font-size: 0.88rem; margin: 0; }
.tip { background: #eef4ff; border: 1px solid #bed0ff; border-radius: 10px;
       padding: 14px 16px; font-size: 0.85rem; color: #1a3a6b; margin-bottom: 16px; }
.card  { background: #fff; border: 1px solid #e2eaf4; border-radius: 14px; padding: 22px; margin-bottom: 16px; }
.slabel { font-size: 0.72rem; font-weight: 700; color: #4a6785;
          text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
  <h1>✦ Page 4 — Streaming Paraphrase</h1>
  <p>Watch the paraphrased text appear word by word in real time.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="tip">📖 <strong>What this page teaches:</strong> How <code>stream: True</code> changes the response — instead of waiting for the full answer, you get chunks and update a placeholder as each one arrives.</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are an expert paraphrasing assistant. "
            "Rewrite the user's text completely while preserving all meaning and intent. "
            "Return only the paraphrased text, no explanation."
        )}
    ]

col1, col2 = st.columns([3, 1])
with col1:
    show_chunks = st.checkbox("Show raw stream chunks (debug mode)", value=False)
with col2:
    if st.button("🗑 Clear", use_container_width=True):
        del st.session_state.messages
        st.rerun()

for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Paste text to paraphrase…")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    payload = {
        "model": "llama3.2",
        "messages": st.session_state.messages,
        "stream": True
    }

    with st.chat_message("assistant"):
        placeholder = st.empty()

    complete_response = ""

    with requests.post("http://localhost:11434/api/chat", json=payload, stream=True) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)

                if show_chunks:
                    st.write(chunk)

                token = chunk.get("message", {}).get("content", "")
                complete_response += token
                placeholder.markdown(complete_response + "▌")

    placeholder.markdown(complete_response)
    st.session_state.messages.append({"role": "assistant", "content": complete_response})

st.markdown("---")
st.markdown("""
**Activity 1:** Enable "Show raw stream chunks" — what does each chunk look like? Where is the token text inside it?

**Activity 2:** How is the chunk structure different from the non-streaming response on Page 1?

**Activity 3:** The `▌` cursor at the end simulates typing. Remove it — what changes about the feel?
""")