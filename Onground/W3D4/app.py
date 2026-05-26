import streamlit as st

st.set_page_config(page_title="QuillBot", layout="wide", page_icon="✦")

st.markdown("""
<style>
.header { background: #0f2744; padding: 32px 36px; border-radius: 16px; margin-bottom: 28px; }
.header h1 { font-size: 2.2rem; color: #fff; font-weight: 700; margin: 0 0 6px; }
.header p  { color: #93b8d8; font-size: 1rem; margin: 0; }
.pills { display: flex; gap: 8px; margin-top: 14px; flex-wrap: wrap; }
.pill  { background: rgba(255,255,255,0.12); color: #d4e8f7; padding: 5px 14px;
         border-radius: 999px; font-size: 0.82rem; border: 1px solid rgba(255,255,255,0.2); }
.grid  { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-top: 24px; }
.card  { background: #fff; border: 1px solid #e2eaf4; border-radius: 14px; padding: 22px; }
.card h3 { color: #0f2744; font-size: 1rem; margin: 0 0 8px; }
.card p  { color: #52667a; font-size: 0.85rem; margin: 0; line-height: 1.6; }
.badge { display: inline-block; background: #eef4ff; color: #1a56a0; font-size: 0.75rem;
         padding: 3px 10px; border-radius: 999px; margin-bottom: 10px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
  <h1>✦ QuillBot</h1>
  <p>AI writing assistant powered by llama3.2 — running locally via Ollama</p>
  <div class="pills">
    <span class="pill">Paraphrase</span>
    <span class="pill">Grammar check</span>
    <span class="pill">AI review</span>
    <span class="pill">Summarize</span>
    <span class="pill">Expand</span>
    <span class="pill">Translate</span>
    <span class="pill">Streaming</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### Pages")
st.markdown("""
<div class="grid">
  <div class="card">
    <div class="badge">Page 1</div>
    <h3>Basic Paraphrase</h3>
    <p>Send a paraphrase request and inspect the raw JSON response from llama3.2.</p>
  </div>
  <div class="card">
    <div class="badge">Page 2</div>
    <h3>Chat UI</h3>
    <p>Explore Streamlit's chat UI components using a grammar check assistant.</p>
  </div>
  <div class="card">
    <div class="badge">Page 3</div>
    <h3>Conversation</h3>
    <p>Multi-turn writing assistant that remembers your edits across the session.</p>
  </div>
  <div class="card">
    <div class="badge">Page 4</div>
    <h3>Streaming Paraphrase</h3>
    <p>Watch the paraphrased text stream in word by word in real time.</p>
  </div>
  <div class="card">
    <div class="badge">Page 5</div>
    <h3>Tool Call — Translate</h3>
    <p>See how llama3.2 uses a tool call to route text to a translation function.</p>
  </div>
  <div class="card">
    <div class="badge">Page 6</div>
    <h3>Tool Call — Summarize & Expand</h3>
    <p>Two-tool setup: the model decides whether to summarize or expand your text.</p>
  </div>
  <div class="card">
    <div class="badge">Page 7</div>
    <h3>Full QuillBot</h3>
    <p>The complete writing assistant — all 6 features, streaming, tone, and download.</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("Make sure Ollama is running at `http://localhost:11434` with `llama3.2` pulled before using any page.")