import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

def paraphrase_text(text, tone):
    prompt = f"""
    Paraphrase the text below.

    Tone: {tone}

    Text:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an academic paraphraser."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content


def render():
    st.title("✍️ Text Paraphraser")

    text = st.text_area("Enter text to paraphrase", height=250)

    tone = st.selectbox(
        "Tone",
        ["Academic", "Formal", "Simple"]
    )

    if st.button("Paraphrase"):
        if not text.strip():
            st.warning("Please enter text.")
            return

        with st.spinner("Paraphrasing..."):
            output = paraphrase_text(text, tone)

        st.subheader("Output")
        st.write(output)