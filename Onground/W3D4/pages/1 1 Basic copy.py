import streamlit as st
import requests
import json

st.set_page_config(page_title="QuillBot - Writing Assistant", layout="wide")

st.markdown(
    """
    <style>
    * { margin: 0; padding: 0; }
    body { background: linear-gradient(135deg, #f5f8fc 0%, #eff4ff 100%); }
    .header-container { background: linear-gradient(135deg, #0c3a69 0%, #1e5a96 100%); padding: 40px; border-radius: 24px; margin-bottom: 32px; box-shadow: 0 20px 50px rgba(12, 58, 105, 0.15); }
    .header-title { font-size: 2.8rem; color: #ffffff; font-weight: 800; margin-bottom: 8px; }
    .header-subtitle { font-size: 1.1rem; color: #c7dff7; }
    .feature-pills { display: flex; gap: 10px; margin-top: 18px; flex-wrap: wrap; }
    .feature-pill { background: rgba(255, 255, 255, 0.2); color: #ffffff; padding: 8px 16px; border-radius: 999px; font-size: 0.95rem; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.3); }
    .main-card { background: #ffffff; border: 1px solid #d4dfe9; border-radius: 22px; padding: 32px; margin-bottom: 28px; box-shadow: 0 16px 40px rgba(62, 87, 123, 0.08); }
    .section-label { color: #0c3a69; font-size: 1.1rem; font-weight: 700; margin-bottom: 14px; display: flex; align-items: center; }
    .section-label::before { content: ""; width: 4px; height: 20px; background: linear-gradient(180deg, #0c3a69, #1e5a96); border-radius: 2px; margin-right: 12px; }
    .input-area { background: #f8fbff; border: 1px solid #d4dfe9; border-radius: 16px; padding: 2px; }
    .settings-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-bottom: 20px; }
    @media (max-width: 768px) { .settings-grid { grid-template-columns: 1fr; } }
    .setting-box { background: #f5f8fc; border: 1px solid #d9e4f0; border-radius: 12px; padding: 16px; }
    .setting-label { color: #1b3a66; font-weight: 700; margin-bottom: 8px; font-size: 0.95rem; }
    .output-box { background: #f8fbff; border: 2px solid #b8d8ff; border-radius: 16px; padding: 24px; color: #0f172a; line-height: 1.8; white-space: pre-wrap; }
    .stats-row { display: flex; gap: 20px; margin-top: 18px; padding-top: 18px; border-top: 1px solid #d4dfe9; }
    .stat-item { display: flex; align-items: center; gap: 8px; }
    .stat-label { color: #52667a; font-size: 0.9rem; }
    .stat-value { color: #0c3a69; font-weight: 700; font-size: 1.15rem; }
    .button-run { width: 100%; padding: 14px; border: none; border-radius: 12px; background: linear-gradient(135deg, #0c3a69, #1e5a96); color: #ffffff; font-size: 1rem; font-weight: 700; cursor: pointer; transition: all 0.3s; box-shadow: 0 8px 20px rgba(12, 58, 105, 0.25); }
    .button-run:hover { transform: translateY(-2px); box-shadow: 0 12px 30px rgba(12, 58, 105, 0.35); }
    .copy-button { background: #eef4ff; color: #0c3a69; border: 1px solid #b8d8ff; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.9rem; }
    .copy-button:hover { background: #d4e8ff; }
    .error-box { background: #fff5f5; border: 1px solid #fcb4b4; border-radius: 12px; padding: 16px; color: #7d2a2a; }
    .success-box { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 16px; color: #15803d; }
    .expander { background: #f8fbff; border: 1px solid #d4dfe9; border-radius: 12px; padding: 16px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="header-container">
        <div class="header-title">✨ QuillBot</div>
        <div class="header-subtitle">Your AI writing assistant powered by llama3.2</div>
        <div class="feature-pills">
            <div class="feature-pill">📝 Paraphrase</div>
            <div class="feature-pill">✓ Grammar Check</div>
            <div class="feature-pill">🤖 AI Checker</div>
            <div class="feature-pill">🎯 Tone Adjustment</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

col_main, col_sidebar = st.columns([2.5, 1])

with col_main:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Enter Your Text</div>', unsafe_allow_html=True)
    text = st.text_area(
        "Your writing",
        height=280,
        placeholder="Paste a sentence, paragraph, essay, or any text you want to improve...",
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_sidebar:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Tool Settings</div>', unsafe_allow_html=True)
    
    mode = st.radio(
        "Tool",
        ["Paraphrase", "Grammar Check", "AI Checker"],
        index=0,
        label_visibility="collapsed",
    )
    
    tone = st.selectbox(
        "Tone",
        ["Standard", "Formal", "Casual", "Creative", "Academic"],
        index=0,
    )
    
    st.markdown("---")
    st.markdown('<div class="setting-label">Advanced</div>', unsafe_allow_html=True)
    show_prompt = st.checkbox("Show system prompt")
    show_response = st.checkbox("Show raw response")
    
    st.markdown("---")
    st.markdown('<div class="setting-label">Model Info</div>', unsafe_allow_html=True)
    st.write("**Model:** llama3.2")
    st.write("**Server:** localhost:11434")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)

col_button, col_info = st.columns([2, 1])
with col_button:
    run_button = st.button("🚀 Run QuillBot", use_container_width=True, key="run_button")

with col_info:
    word_count = len(text.split()) if text else 0
    char_count = len(text) if text else 0
    st.metric("Word Count", word_count)

st.markdown('</div>', unsafe_allow_html=True)

if show_prompt:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">System Prompt</div>', unsafe_allow_html=True)
    
    if mode == "Paraphrase":
        prompt_text = (
            "You are an expert professional paraphrasing assistant. "
            "Rewrite the user's text completely while preserving all meaning, facts, and intent. "
            "Match the selected tone. Do not add new information. "
            "Return only the paraphrased text, no explanations."
        )
    elif mode == "Grammar Check":
        prompt_text = (
            "You are a meticulous grammar and style editor. "
            "Correct all grammar, spelling, punctuation, and clarity issues. "
            "Preserve the original meaning exactly. "
            "Return only the corrected text."
        )
    else:
        prompt_text = (
            "You are an AI writing reviewer. Analyze this text for: "
            "1. Readability and clarity; 2. Tone consistency; 3. Whether it sounds human or AI-written; "
            "4. Grammar and style. Provide a short review (3-4 sentences) with one actionable suggestion."
        )
    
    st.code(prompt_text, language="python")
    st.markdown('</div>', unsafe_allow_html=True)

if run_button:
    if not text or not text.strip():
        st.markdown(
            '<div class="error-box"><strong>⚠️ Error:</strong> Please enter text before running the tool.</div>',
            unsafe_allow_html=True,
        )
    else:
        with st.spinner("⏳ QuillBot is processing your text..."):
            if mode == "Paraphrase":
                system_prompt = (
                    "You are an expert professional paraphrasing assistant. "
                    "Rewrite the user's text completely while preserving all meaning, facts, and intent. "
                    "Match the selected tone. Do not add new information. "
                    "Return only the paraphrased text, no explanations."
                )
                user_instruction = f"Paraphrase this text in {tone.lower()} tone:\n\n{text}"
            elif mode == "Grammar Check":
                system_prompt = (
                    "You are a meticulous grammar and style editor. "
                    "Correct all grammar, spelling, punctuation, and clarity issues. "
                    "Preserve the original meaning exactly. "
                    "Return only the corrected text."
                )
                user_instruction = f"Edit this text for grammar, style, and clarity:\n\n{text}"
            else:
                system_prompt = (
                    "You are an AI writing reviewer. Analyze this text for: "
                    "1. Readability and clarity; 2. Tone consistency; 3. Whether it sounds human or AI-written; "
                    "4. Grammar and style. Provide a short review (3-4 sentences) with one actionable suggestion."
                )
                user_instruction = f"Review this text and provide feedback:\n\n{text}"

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_instruction},
            ]

            payload = {
                "model": "llama3.2",
                "messages": messages,
                "stream": False,
            }

            try:
                response = requests.post(
                    "http://localhost:11434/api/chat",
                    json=payload,
                    timeout=50,
                )
                response.raise_for_status()
                data = response.json()

                assistant_reply = None
                if isinstance(data, dict):
                    message = data.get("message") or data.get("choices", [{}])[0].get("message")
                    if isinstance(message, dict):
                        assistant_reply = message.get("content")
                    elif isinstance(message, list) and message:
                        assistant_reply = message[0].get("content")

                if assistant_reply is None:
                    assistant_reply = "Error: Could not find the assistant reply in the response."

                st.markdown('<div class="main-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-label">Output Result</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="output-box">{assistant_reply.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📋 Copy to Clipboard"):
                        st.write("(Copy functionality - use browser console)")
                with col2:
                    if st.button("📥 Download"):
                        st.write("(Download as .txt file)")
                with col3:
                    if st.button("🔄 Try Again"):
                        st.rerun()

                word_count_output = len(assistant_reply.split())
                char_count_output = len(assistant_reply)
                st.markdown(
                    f'<div class="stats-row">'
                    f'<div class="stat-item"><span class="stat-label">Input Words:</span> <span class="stat-value">{len(text.split())}</span></div>'
                    f'<div class="stat-item"><span class="stat-label">Output Words:</span> <span class="stat-value">{word_count_output}</span></div>'
                    f'<div class="stat-item"><span class="stat-label">Character Change:</span> <span class="stat-value">{char_count_output - len(text)}</span></div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                st.markdown('</div>', unsafe_allow_html=True)

                if show_response:
                    st.markdown('<div class="main-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-label">Raw API Response</div>', unsafe_allow_html=True)
                    st.json(data)
                    st.markdown('</div>', unsafe_allow_html=True)

            except requests.exceptions.Timeout:
                st.markdown(
                    '<div class="error-box"><strong>⏱️ Timeout:</strong> The request took too long. Please try again.</div>',
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.markdown(
                    f'<div class="error-box"><strong>❌ Error:</strong> {str(e)}</div>',
                    unsafe_allow_html=True,
                )
