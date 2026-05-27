import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

def summarize_text(text, style):
    prompt = f"""
    Summarize the text below.

    Style: {style}

    Text:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an academic summarizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


def render():
    st.title("📄 Document Summarizer")

    text = st.text_area("Enter text to summarize", height=250)

    style = st.selectbox(
        "Summary Type",
        ["Short Summary", "Bullet Points", "Key Takeaways"]
    )

    if st.button("Generate Summary"):
        if not text.strip():
            st.warning("Please enter text.")
            return

        with st.spinner("Summarizing..."):
            output = summarize_text(text, style)

        st.subheader("Output")
        st.write(output)