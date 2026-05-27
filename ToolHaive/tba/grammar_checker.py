import streamlit as st
from openai import OpenAI

# GROQ CLIENT
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

def check_grammar(text):
    prompt = f"""
    You are an advanced grammar checker.

    Task:
    - Correct all grammar mistakes
    - Improve sentence structure
    - Keep the original meaning
    - Make it sound academic and clear

    Text:
    {text}

    Output format:
    1. Corrected Version
    2. Explanation of major corrections
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an expert English grammar and writing assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


def render():
    st.title("📝 Grammar Checker")

    text = st.text_area("Enter your text", height=250)

    if st.button("Check Grammar"):

        if not text.strip():
            st.warning("Please enter text.")
            return

        with st.spinner("Checking grammar..."):
            result = check_grammar(text)

        st.subheader("Result")
        st.write(result)