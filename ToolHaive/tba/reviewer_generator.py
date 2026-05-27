import streamlit as st
from openai import OpenAI

# GROQ CLIENT
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)


def generate_reviewer(text, reviewer_type):

    prompt = f"""
    Create an academic reviewer based on the notes below.

    Reviewer Type:
    {reviewer_type}

    Instructions:
    - Make it organized
    - Keep important concepts
    - Make it useful for studying
    - Use simple and clear wording

    Notes:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
                You are an academic reviewer generator.
                Your task is to transform lecture notes
                into effective study materials.
                """
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content


def render():

    st.title("📚 Reviewer Generator")

    st.write(
        "Generate study reviewers from your notes."
    )

    text = st.text_area(
        "Paste lecture notes or study material",
        height=300,
        placeholder="Paste your lesson notes here..."
    )

    reviewer_type = st.selectbox(
        "Reviewer Format",
        [
            "Key Points Summary",
            "Question & Answer Reviewer",
            "Flashcards",
            "Practice Quiz"
        ]
    )

    if st.button("Generate Reviewer"):

        if not text.strip():
            st.warning("Please enter lecture notes.")
            return

        with st.spinner("Generating reviewer..."):

            try:
                output = generate_reviewer(
                    text,
                    reviewer_type
                )

                st.success("Reviewer generated!")

                st.subheader("Generated Reviewer")
                st.write(output)

            except Exception as e:
                st.error(f"Error: {e}")