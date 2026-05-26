import streamlit as st
import requests
import json
import streamlit.components.v1 as components

st.set_page_config(page_title="Basic Paraphrase", layout="wide", page_icon="✦")

st.markdown("""
<style>
.header { background: #0f2744; padding: 24px 28px; border-radius: 14px; margin-bottom: 22px; }
.header h1 { font-size: 1.6rem; color: #fff; font-weight: 700; margin: 0 0 4px; }
.header p  { color: #93b8d8; font-size: 0.88rem; margin: 0; }
.card  { background: #fff; border: 1px solid #e2eaf4; border-radius: 14px; padding: 22px; margin-bottom: 16px; }
.slabel { font-size: 0.72rem; font-weight: 700; color: #4a6785;
          text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }
.tip { background: #eef4ff; border: 1px solid #bed0ff; border-radius: 10px;
       padding: 14px 16px; font-size: 0.85rem; color: #1a3a6b; margin-bottom: 16px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
  <h1>✦ Page 1 — Basic Paraphrase</h1>
  <p>Send a paraphrase request to llama3.2 and inspect the raw JSON response.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="tip">📖 <strong>What this page teaches:</strong> How to build a request payload, send it to Ollama, and find the assistant reply inside the raw JSON response.</div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="slabel">Text to paraphrase</div>', unsafe_allow_html=True)
prompt = st.text_area("input", height=140,
    placeholder="Paste any text here and hit Send to paraphrase it…",
    label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

messages = [
    {"role": "system", "content": "You are an expert paraphrasing assistant. Rewrite the user's text completely while preserving all meaning. Return only the paraphrased text, no explanation."},
    {"role": "user",   "content": f"Paraphrase this text:\n\n{prompt}"}
]

payload = {
    "model": "llama3.2",
    "messages": messages,
    "stream": False
}

if st.button("Send", use_container_width=True, type="primary") and prompt:
    with st.spinner("llama3.2 is paraphrasing…"):
        response = requests.post("http://localhost:11434/api/chat", json=payload)
        components.html(f"<script>console.log({json.dumps(response.json())})</script>", height=0)
        data = response.json()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">Full JSON response (raw)</div>', unsafe_allow_html=True)
    st.json(data)
    st.markdown('</div>', unsafe_allow_html=True)

    # Activity: extract just the reply
    assistant_reply = data["message"]["content"]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">Assistant reply only</div>', unsafe_allow_html=True)
    st.write(assistant_reply)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
**Activity 1:** Look at the raw JSON above. Where exactly is the paraphrased text sitting inside that structure?

**Activity 2:** Change the system prompt to use a different tone — formal, casual, or academic. How does the output change?

**Activity 3:** Try setting `stream: True` in the payload. What happens to the response structure?
""")