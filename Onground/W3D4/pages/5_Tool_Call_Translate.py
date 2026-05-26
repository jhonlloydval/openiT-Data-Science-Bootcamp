import streamlit as st
import requests
import json

st.set_page_config(page_title="Tool Call — Translate", layout="wide", page_icon="✦")

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
.result { background: #f7fafd; border: 1.5px solid #b8d4f0; border-radius: 12px;
          padding: 18px; line-height: 1.8; color: #0f1f33; font-size: 0.97rem; white-space: pre-wrap; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
  <h1>✦ Page 5 — Tool Call: Translate</h1>
  <p>llama3.2 uses a tool call to route your text to a translate function.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="tip">📖 <strong>What this page teaches:</strong> How the model decides to call a tool instead of answering directly — and how you parse the tool call arguments and run the function yourself.</div>', unsafe_allow_html=True)

# ── Language options ──────────────────────────────────────────────────────────
LANGUAGES = [
    "Spanish", "French", "German", "Japanese", "Chinese",
    "Filipino (Tagalog)", "Cebuano", "Ilocano"
]

# ── Tool definition ───────────────────────────────────────────────────────────
tools = [
    {
        "type": "function",
        "function": {
            "name": "translate_text",
            "description": "Translate the given text into the specified target language.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to translate"
                    },
                    "target_language": {
                        "type": "string",
                        "description": "The language to translate into (e.g. Spanish, French, Filipino)"
                    }
                },
                "required": ["text", "target_language"]
            }
        }
    }
]

# ── Translate function (calls llama3.2 to do the actual translation) ──────────
def translate_text(params):
    text            = params["text"]
    target_language = params["target_language"]
    payload = {
        "model": "llama3.2",
        "messages": [
            {"role": "system", "content": f"You are a professional translator. Translate the user's text into {target_language}. Return only the translated text, nothing else."},
            {"role": "user",   "content": text}
        ],
        "stream": False
    }
    response = requests.post("http://localhost:11434/api/chat", json=payload)
    return response.json()["message"]["content"]

# ── UI ────────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">Text to translate</div>', unsafe_allow_html=True)
    text = st.text_area("text", height=140,
        placeholder="Paste any text you want to translate…",
        label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">Target language</div>', unsafe_allow_html=True)
    target_lang = st.selectbox("lang", LANGUAGES, label_visibility="collapsed")
    show_raw = st.checkbox("Show tool call JSON")
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("Translate via Tool Call", use_container_width=True, type="primary") and text:
    with st.spinner("llama3.2 is generating a tool call…"):
        payload = {
            "model": "llama3.2",
            "messages": [
                {"role": "user", "content": f"Please translate the following text into {target_lang}:\n\n{text}"}
            ],
            "tools": tools,
            "stream": False
        }
        response = requests.post("http://localhost:11434/api/chat", json=payload)
        data    = response.json()
        message = data["message"]

    if show_raw:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="slabel">Raw response from llama3.2</div>', unsafe_allow_html=True)
        st.json(data)
        st.markdown('</div>', unsafe_allow_html=True)

    if message.get("tool_calls"):
        raw_args = message["tool_calls"][0]["function"]["arguments"]

        # Parse args safely
        obj = {}
        for key, value in raw_args.items():
            if isinstance(value, str):
                try:    obj[key] = json.loads(value)
                except: obj[key] = value
            else:
                obj[key] = value

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="slabel">Parsed tool call arguments</div>', unsafe_allow_html=True)
        st.json(obj)
        st.markdown('</div>', unsafe_allow_html=True)

        with st.spinner(f"Translating into {target_lang}…"):
            result = translate_text(obj)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="slabel">Translation → {target_lang}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result">{result}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button("⬇ Download translation", data=result,
                           file_name="translation.txt", mime="text/plain")
    else:
        # Model answered directly
        with st.chat_message("assistant"):
            st.markdown(message["content"])

st.markdown("---")
st.markdown("""
**Activity 1:** Enable "Show tool call JSON" — find where the tool name and arguments are in the response.

**Activity 2:** What happens if you ask something unrelated, like "What is the capital of France?" Does the model still call the tool?

**Activity 3:** Add a second tool called `detect_language` that takes just `text` as input. When would the model choose one tool over the other?
""")