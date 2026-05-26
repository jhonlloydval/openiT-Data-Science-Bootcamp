import streamlit as st
import requests
import json

st.set_page_config(page_title="QuillBot — Full", layout="wide", page_icon="✦")

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.header { background: #0f2744; padding: 28px 32px; border-radius: 16px; margin-bottom: 24px; }
.header h1 { font-size: 2rem; color: #fff; font-weight: 700; margin: 0 0 4px; }
.header p  { color: #93b8d8; font-size: 0.9rem; margin: 0; }
.pills { display: flex; gap: 8px; margin-top: 12px; flex-wrap: wrap; }
.pill  { background: rgba(255,255,255,0.12); color: #d4e8f7; padding: 5px 14px;
         border-radius: 999px; font-size: 0.8rem; border: 1px solid rgba(255,255,255,0.2); }
.card  { background: #fff; border: 1px solid #e2eaf4; border-radius: 14px; padding: 22px; margin-bottom: 16px; }
.slabel { font-size: 0.72rem; font-weight: 700; color: #4a6785;
          text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }
.result { background: #f7fafd; border: 1.5px solid #b8d4f0; border-radius: 12px;
          padding: 18px; line-height: 1.8; color: #0f1f33; font-size: 0.97rem; white-space: pre-wrap; }
.stat-row { display: flex; gap: 24px; margin-top: 12px; padding-top: 12px;
            border-top: 1px solid #e2eaf4; }
.stat { font-size: 0.82rem; color: #52667a; }
.stat b { color: #0f2744; }
.err  { background: #fff5f5; border: 1px solid #f5b8b8; border-radius: 10px;
        padding: 12px 16px; color: #7d2a2a; font-size: 0.88rem; margin-top: 12px; }
.wc   { font-size: 0.78rem; color: #8a9fb5; text-align: right; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header">
  <h1>✦ QuillBot — Full Writing Assistant</h1>
  <p>Paraphrase · Grammar check · AI review · Summarize · Expand · Translate</p>
  <div class="pills">
    <span class="pill">Streaming output</span>
    <span class="pill">Tone control</span>
    <span class="pill">Word count</span>
    <span class="pill">Download</span>
    <span class="pill">llama3.2</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Language options (for translate) ─────────────────────────────────────────
LANGUAGES = [
    "Spanish", "French", "German", "Japanese", "Chinese",
    "Filipino (Tagalog)", "Cebuano", "Ilocano"
]

# ── Layout ────────────────────────────────────────────────────────────────────
col_main, col_side = st.columns([2.4, 1])

with col_main:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">Your text</div>', unsafe_allow_html=True)
    text = st.text_area("input", height=260,
        placeholder="Paste a sentence, paragraph, or essay you'd like to improve…",
        label_visibility="collapsed")
    wc = len(text.split()) if text.strip() else 0
    st.markdown(f'<div class="wc">{wc} word{"s" if wc != 1 else ""}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_side:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">Feature</div>', unsafe_allow_html=True)
    mode = st.radio("mode", [
        "Paraphrase",
        "Grammar check",
        "AI review",
        "Summarize",
        "Expand",
        "Translate",
    ], index=0, label_visibility="collapsed")

    st.markdown('<div class="slabel" style="margin-top:14px">Tone / Style</div>', unsafe_allow_html=True)
    tone = st.selectbox("tone", ["Standard", "Formal", "Casual", "Creative", "Academic"],
                        label_visibility="collapsed")

    # Translate-specific option
    if mode == "Translate":
        st.markdown('<div class="slabel" style="margin-top:10px">Target language</div>', unsafe_allow_html=True)
        target_lang = st.selectbox("lang", LANGUAGES, label_visibility="collapsed")
    else:
        target_lang = "Spanish"

    # Summarize-specific option
    if mode == "Summarize":
        st.markdown('<div class="slabel" style="margin-top:10px">Summary length</div>', unsafe_allow_html=True)
        summary_length = st.selectbox("sumlen", ["One sentence", "Short paragraph", "Bullet points"],
                                      label_visibility="collapsed")
    else:
        summary_length = "Short paragraph"

    st.markdown("---")
    st.markdown('<div class="slabel">Options</div>', unsafe_allow_html=True)
    use_streaming  = st.checkbox("Stream output", value=True)
    show_prompt    = st.checkbox("Show system prompt")
    show_raw       = st.checkbox("Show raw response")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Build system prompt & user message ───────────────────────────────────────
if mode == "Paraphrase":
    system_prompt = (
        f"You are an expert paraphrasing assistant. "
        f"Rewrite the user's text completely while preserving all meaning, facts, and intent. "
        f"Use a {tone.lower()} tone. Do not add new information. "
        f"Return only the paraphrased text — no preamble, no explanation."
    )
    user_msg     = f"Paraphrase the following text:\n\n{text}"
    result_label = "Paraphrased text"

elif mode == "Grammar check":
    system_prompt = (
        f"You are a meticulous grammar and style editor. "
        f"Fix all grammar, spelling, punctuation, and clarity issues. "
        f"Preserve the original meaning exactly. Use a {tone.lower()} register. "
        f"Return only the corrected text — no preamble."
    )
    user_msg     = f"Edit the following text for grammar, style, and clarity:\n\n{text}"
    result_label = "Corrected text"

elif mode == "AI review":
    system_prompt = (
        "You are a skilled writing coach. Analyze the text for: "
        "readability and clarity, tone consistency, whether it sounds natural or AI-written, "
        "and grammar. Write a concise review (3–4 sentences) and end with one specific, actionable suggestion."
    )
    user_msg     = f"Review the following text and provide feedback:\n\n{text}"
    result_label = "Writing review"

elif mode == "Summarize":
    system_prompt = (
        f"You are an expert at summarizing text. "
        f"Condense the user's text into a {summary_length.lower()} that captures all key points. "
        f"Use a {tone.lower()} tone. Return only the summary — no preamble."
    )
    user_msg     = f"Summarize the following text:\n\n{text}"
    result_label = f"Summary ({summary_length.lower()})"

elif mode == "Expand":
    system_prompt = (
        f"You are an expert writer and writing coach. "
        f"Expand and elaborate on the user's text, adding depth, detail, and supporting ideas. "
        f"Use a {tone.lower()} style. Return only the expanded text — no preamble."
    )
    user_msg     = f"Expand the following text:\n\n{text}"
    result_label = "Expanded text"

else:  # Translate
    system_prompt = (
        f"You are a professional translator. "
        f"Translate the user's text into {target_lang} accurately and naturally. "
        f"Preserve the meaning and tone. Return only the translated text — no preamble."
    )
    user_msg     = f"Translate the following text into {target_lang}:\n\n{text}"
    result_label = f"Translation → {target_lang}"

# ── Show system prompt ────────────────────────────────────────────────────────
if show_prompt:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">System prompt</div>', unsafe_allow_html=True)
    st.code(system_prompt, language=None)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Run button ────────────────────────────────────────────────────────────────
run = st.button("▶  Run QuillBot", use_container_width=True, type="primary")

if run:
    if not text or not text.strip():
        st.markdown('<div class="err">⚠️ Please enter some text before running.</div>',
                    unsafe_allow_html=True)
    elif len(text.strip()) < 10:
        st.markdown('<div class="err">⚠️ Text is too short — enter at least a sentence.</div>',
                    unsafe_allow_html=True)
    else:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_msg},
        ]

        # ── Streaming ─────────────────────────────────────────────────────────
        if use_streaming:
            payload = {"model": "llama3.2", "messages": messages, "stream": True}

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f'<div class="slabel">{result_label}</div>', unsafe_allow_html=True)
            placeholder = st.empty()
            complete_response = ""

            try:
                with requests.post("http://localhost:11434/api/chat", json=payload, stream=True, timeout=90) as response:
                    response.raise_for_status()
                    for line in response.iter_lines():
                        if line:
                            chunk = json.loads(line)
                            token = chunk.get("message", {}).get("content", "")
                            complete_response += token
                            placeholder.markdown(
                                f'<div class="result">{complete_response.replace(chr(10), "<br>")}▌</div>',
                                unsafe_allow_html=True
                            )

                placeholder.markdown(
                    f'<div class="result">{complete_response.replace(chr(10), "<br>")}</div>',
                    unsafe_allow_html=True
                )

                in_words  = len(text.split())
                out_words = len(complete_response.split())
                diff      = out_words - in_words
                diff_str  = f"+{diff}" if diff > 0 else str(diff)
                st.markdown(
                    f'<div class="stat-row">'
                    f'<span class="stat">Input: <b>{in_words} words</b></span>'
                    f'<span class="stat">Output: <b>{out_words} words</b></span>'
                    f'<span class="stat">Change: <b>{diff_str} words</b></span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

                col_dl, col_retry = st.columns(2)
                with col_dl:
                    st.download_button("⬇ Download as .txt", data=complete_response,
                                       file_name="quillbot-output.txt", mime="text/plain",
                                       use_container_width=True)
                with col_retry:
                    if st.button("↺ Run again", use_container_width=True):
                        st.rerun()

            except requests.exceptions.ConnectionError:
                st.markdown('<div class="err">❌ Cannot reach Ollama. Make sure it is running at localhost:11434.</div>', unsafe_allow_html=True)
            except requests.exceptions.Timeout:
                st.markdown('<div class="err">⏱️ Request timed out. Try a shorter text or restart Ollama.</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="err">❌ Error: {e}</div>', unsafe_allow_html=True)

        # ── Non-streaming ──────────────────────────────────────────────────────
        else:
            payload = {"model": "llama3.2", "messages": messages, "stream": False}

            try:
                with st.spinner("QuillBot is thinking…"):
                    response = requests.post("http://localhost:11434/api/chat", json=payload, timeout=90)
                    response.raise_for_status()
                    data  = response.json()
                    reply = data["message"]["content"]

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f'<div class="slabel">{result_label}</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="result">{reply.replace(chr(10), "<br>")}</div>',
                    unsafe_allow_html=True
                )

                in_words  = len(text.split())
                out_words = len(reply.split())
                diff      = out_words - in_words
                diff_str  = f"+{diff}" if diff > 0 else str(diff)
                st.markdown(
                    f'<div class="stat-row">'
                    f'<span class="stat">Input: <b>{in_words} words</b></span>'
                    f'<span class="stat">Output: <b>{out_words} words</b></span>'
                    f'<span class="stat">Change: <b>{diff_str} words</b></span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

                col_dl, col_retry = st.columns(2)
                with col_dl:
                    st.download_button("⬇ Download as .txt", data=reply,
                                       file_name="quillbot-output.txt", mime="text/plain",
                                       use_container_width=True)
                with col_retry:
                    if st.button("↺ Run again", use_container_width=True):
                        st.rerun()

                if show_raw:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown('<div class="slabel">Raw API response</div>', unsafe_allow_html=True)
                    st.json(data)
                    st.markdown('</div>', unsafe_allow_html=True)

            except requests.exceptions.ConnectionError:
                st.markdown('<div class="err">❌ Cannot reach Ollama. Make sure it is running at localhost:11434.</div>', unsafe_allow_html=True)
            except requests.exceptions.Timeout:
                st.markdown('<div class="err">⏱️ Request timed out. Try a shorter text or restart Ollama.</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="err">❌ Error: {e}</div>', unsafe_allow_html=True)