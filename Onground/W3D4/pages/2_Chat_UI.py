import streamlit as st

st.set_page_config(page_title="Chat UI", layout="wide", page_icon="✦")

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
  <h1>✦ Page 2 — Chat UI Components</h1>
  <p>Explore Streamlit's built-in chat components using a grammar check example.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="tip">📖 <strong>What this page teaches:</strong> How <code>st.chat_message()</code> and <code>st.chat_input()</code> work — the visual building blocks of any chat interface.</div>', unsafe_allow_html=True)

st.markdown("Below is a static preview of what a QuillBot grammar check conversation looks like using Streamlit's chat UI:")

with st.chat_message("assistant"):
    st.markdown("👋 Hi! I'm QuillBot. Paste any text and I'll check the grammar for you.")

with st.chat_message("user"):
    st.markdown("their going to the store and buyed some apple's yesterday.")

with st.chat_message("assistant"):
    st.markdown("""✅ **Corrected text:**

They're going to the store and bought some apples yesterday.

**Changes made:**
- *their* → *they're* (contraction for "they are")
- *buyed* → *bought* (irregular past tense)
- *apple's* → *apples* (no apostrophe needed for a simple plural)
""")

with st.chat_message("user"):
    st.markdown("Can you also make it more formal?")

with st.chat_message("assistant"):
    st.markdown("""✅ **Formal version:**

They are proceeding to the store, where they purchased several apples yesterday.
""")

st.markdown("---")
st.markdown("**This is a static display.** The chat bubbles above are built with:")
st.code("""with st.chat_message("assistant"):
    st.markdown("Your message here")

with st.chat_message("user"):
    st.markdown("User message here")

# Pull-down input bar at the bottom:
st.chat_input("Type something…")
""", language="python")

st.chat_input("This input bar is just for display — it doesn't send anything on this page")

st.markdown("---")
st.markdown("""
**Activity 1:** Add a third exchange to the static preview above — a user asks for a casual version and the assistant replies.

**Activity 2:** What roles can `st.chat_message()` accept? Try `"system"` and see how it looks.

**Activity 3:** Head to Page 3 to see these components wired up to a live llama3.2 conversation.
""")