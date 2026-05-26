import streamlit as st
import requests
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="Ollama Chat", layout="wide")

st.title("Basic")

prompt = st.text_input("Ask llama3.2 something...")

messages = [
    {"role": "system", "content": "You are a playful cat assistant. Always answer like a cat and include some form of 'meow' in your reply."},
    {"role": "user", "content": prompt}
]

payload = {
    "model": "llama3.2",
    "messages": messages,
    "stream": False
}

if st.button("Send") and prompt:
    response = requests.post("http://localhost:11434/api/chat", json=payload)

    components.html(f"<script>console.log({json.dumps(response.json())})</script>", height=0)

    data = response.json()
    assistant_reply = None
    if isinstance(data, dict):
        message = data.get("message") or data.get("choices", [{}])[0].get("message")
        if isinstance(message, dict):
            assistant_reply = message.get("content")
        elif isinstance(message, list) and message:
            assistant_reply = message[0].get("content")

    if assistant_reply is None:
        assistant_reply = "Sorry, I could not find the assistant reply in the response."

    st.write(assistant_reply)

# Activity 1: What does the response look like? Can you find the content of the assistant's reply in the response? make it so that the st.write() only shows the assistant's reply, not the entire response object.
# Activity 2: Add a system prompt that tells the assistant to be a cat that says meow, or a pirate that say Arrg. How does that change the response?