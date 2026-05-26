import streamlit as st
import requests
import json

st.set_page_config(page_title="Tool Call — Summarize & Expand", layout="wide", page_icon="✦")

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
.badge-sum  { background: #eef4ff; color: #1a56a0; font-size: 0.78rem; padding: 3px 10px; border-radius: 999px; font-weight: 600; }
.badge-exp  { background: #f0fdf4; color: #166534; font-size: 0.78rem; padding: 3px 10px; border-radius: 999px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
  <h1>✦ Page 6 — Tool Call: Summarize & Expand</h1>
  <p>Two-tool setup — llama3.2 decides whether to summarize or expand your text.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="tip">📖 <strong>What this page teaches:</strong> When the model has multiple tools, it picks the right one based on context. You can see which tool it chose and inspect the arguments it passed.</div>', unsafe_allow_html=True)

# ── Tool definitions ──────────────────────────────────────────────────────────
tools = [
    {
        "type": "function",
        "function": {
            "name": "summarize_text",
            "description": "Condense the given text into a shorter summary while keeping the key points.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text":   {"type": "string", "description": "The text to summarize"},
                    "length": {"type": "string", "enum": ["one sentence", "short paragraph", "bullet points"],
                               "description": "How short the summary should be"}
                },
                "required": ["text", "length"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "expand_text",
            "description": "Expand or elaborate on the given text, adding more detail and depth.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text":  {"type": "string", "description": "The text to expand"},
                    "style": {"type": "string", "enum": ["detailed", "academic", "storytelling"],
                              "description": "The style to use when expanding"}
                },
                "required": ["text", "style"]
            }
        }
    }
]

# ── Tool functions ────────────────────────────────────────────────────────────
def summarize_text(params):
    text   = params["text"]
    length = params.get("length", "short paragraph")
    payload = {
        "model": "llama3.2",
        "messages": [
            {"role": "system", "content": f"You are an expert at summarizing text. Summarize the following text as a {length}. Return only the summary, nothing else."},
            {"role": "user",   "content": text}
        ],
        "stream": False
    }
    return requests.post("http://localhost:11434/api/chat", json=payload).json()["message"]["content"]

def expand_text(params):
    text  = params["text"]
    style = params.get("style", "detailed")
    payload = {
        "model": "llama3.2",
        "messages": [
            {"role": "system", "content": f"You are an expert writer. Expand and elaborate on the following text in a {style} style, adding depth and detail. Return only the expanded text."},
            {"role": "user",   "content": text}
        ],
        "stream": False
    }
    return requests.post("http://localhost:11434/api/chat", json=payload).json()["message"]["content"]

def dispatch_tool(tool_name, params):
    if tool_name == "summarize_text":
        return summarize_text(params), "summarize"
    elif tool_name == "expand_text":
        return expand_text(params), "expand"
    return "Tool not found.", "unknown"

# ── UI ────────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">Your text</div>', unsafe_allow_html=True)
    text = st.text_area("text", height=160,
        placeholder="Paste text and tell the model what to do, e.g. 'Summarize this' or 'Expand this into a full paragraph'…",
        label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">Instruction</div>', unsafe_allow_html=True)
    instruction = st.selectbox("instruction", [
        "Summarize this as one sentence",
        "Summarize this as bullet points",
        "Summarize this as a short paragraph",
        "Expand this with more detail",
        "Expand this in an academic style",
        "Expand this as a story",
    ], label_visibility="collapsed")
    show_raw = st.checkbox("Show tool call JSON")
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("Run Tool Call", use_container_width=True, type="primary") and text:
    with st.spinner("llama3.2 is choosing a tool…"):
        payload = {
            "model": "llama3.2",
            "messages": [
                {"role": "system", "content": "You are QuillBot. You have two tools: summarize_text and expand_text. Choose the correct one based on the user's instruction and call it with appropriate parameters."},
                {"role": "user",   "content": f"{instruction}:\n\n{text}"}
            ],
            "tools": tools,
            "stream": False
        }
        response = requests.post("http://localhost:11434/api/chat", json=payload)
        data    = response.json()
        message = data["message"]

    if show_raw:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="slabel">Raw response</div>', unsafe_allow_html=True)
        st.json(data)
        st.markdown('</div>', unsafe_allow_html=True)

    if message.get("tool_calls"):
        tool_call = message["tool_calls"][0]
        tool_name = tool_call["function"]["name"]
        raw_args  = tool_call["function"]["arguments"]

        obj = {}
        for key, value in raw_args.items():
            if isinstance(value, str):
                try:    obj[key] = json.loads(value)
                except: obj[key] = value
            else:
                obj[key] = value

        badge_class = "badge-sum" if tool_name == "summarize_text" else "badge-exp"
        st.markdown(
            f'<p>Model chose: <span class="{badge_class}">{tool_name}</span></p>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="slabel">Tool call arguments</div>', unsafe_allow_html=True)
        st.json(obj)
        st.markdown('</div>', unsafe_allow_html=True)

        spinner_label = "Summarizing…" if tool_name == "summarize_text" else "Expanding…"
        with st.spinner(spinner_label):
            result, action = dispatch_tool(tool_name, obj)

        result_title = "Summary" if action == "summarize" else "Expanded text"
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="slabel">{result_title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result">{result}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button("⬇ Download result", data=result,
                           file_name=f"quillbot-{action}.txt", mime="text/plain")
    else:
        with st.chat_message("assistant"):
            st.markdown(message["content"])

st.markdown("---")
st.markdown("""
**Activity 1:** Try an ambiguous instruction like "change this text". Which tool does the model pick?

**Activity 2:** What happens if you give a very short sentence and say "expand this"? How much does it grow?

**Activity 3:** Add a third tool — `paraphrase_text` — and test whether the model picks the right one when you say "rewrite this".
""")