import streamlit as st
import requests
import json

st.set_page_config(page_title="Ollama Chat", layout="wide")

st.title("Assistant Conversation")

def process_tool(params, tool_name):
    if tool_name == "country_flag":
        return country_flag(params)
    else:
        return f"Tool {tool_name} not found."
    
def country_flag(params):
    country = params["country"]
    response = requests.get(f"https://restcountries.com/v3.1/name/{country}?fields=flags")
    data = response.json()
    st.image(data[0]["flags"]["png"], caption=data[0]["flags"].get("alt", ""))
    return f"successfully displayed the flag of {country}";

tools = [
    {
        "type": "function",
        "function": {
            "name": "country_flag",
            "description": "shows the flag of a country",
            "parameters": {
                "type": "object",
                "properties": {
                    "country": {"type": "string"}
                },
                "required": ["country"]
            }
        }
    }
]


# We will store the conversation history in Streamlit's session state, which allows us to keep track of messages across user interactions.
if "messages" not in st.session_state:
    st.session_state.messages = [
        # Also, initialize the system prompt
        {"role": "system", "content": "You are a helpful assistant that shows the flags of countries."}
    ]

# Iterate through the conversation history
for msg in st.session_state.messages:
    # display each message in the appropriate format based on its role (system, user, assistant)
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# this is where the user will type their message. st.chat_input() is a built-in Streamlit component that creates a text input and automatically scrolls to the bottom of the page when new messages are added.
prompt = st.chat_input("Try this: Get the flag of the Philippines using the tool")


def generate():
    payload = {
        "model": "llama3.2",
        "messages": st.session_state.messages,
        "tools": tools,
        "stream": True
    }

    with st.chat_message("assistant"): placeholder = st.empty()
    
    complete_response = ""
    has_tool_calls = False

    with requests.post("http://localhost:11434/api/chat", json=payload, stream=True) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)

                tool_calls = chunk.get("message", {}).get("tool_calls")
                if tool_calls:
                    has_tool_calls = True
                    for tool_call in tool_calls:
                        tool_call_id = tool_call["id"]
                        tool_call_name = tool_call["function"]["name"]
                        tool_call_args = tool_call["function"]["arguments"]                    

                        # parse to object
                        obj = {}
                        for key, value in tool_call_args.items():
                            if isinstance(value, str):
                                try:
                                    obj[key] = json.loads(value)
                                except json.JSONDecodeError:
                                    obj[key] = value
                            else:
                                obj[key] = value

                        tool_response = process_tool(obj, tool_call_name)

                        st.session_state.messages.append({
                            "role": "tool", 
                            "content": tool_response, 
                            "tool_name": tool_call_name,
                            "tool_call_id": tool_call_id
                        })
                else:
                    complete_response += chunk["message"]["content"]
                    placeholder.markdown(complete_response + "▌")

    if has_tool_calls:
        # After processing tool calls, we want to regenerate the response so that the model can incorporate the tool responses into its final answer
        generate()
    else:        
        placeholder.markdown(complete_response)    
        st.session_state.messages.append({"role": "assistant", "content": complete_response})

# run this logic every time the user submits a new message
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    generate()
    