"""
utils/ollama_client.py
───────────────────────────────────────────────────────────────────────────────
ToolHive AI — Shared Ollama API Wrapper
All AI calls route through here so the model and URL are configured once.
───────────────────────────────────────────────────────────────────────────────
"""

import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL      = "llama3.2"


def chat(messages: list[dict], stream: bool = False) -> str:
    """Send a message list to Ollama and return the assistant reply as a string.

    Args:
        messages: List of {"role": ..., "content": ...} dicts.
                  Include the system prompt as the first message.
        stream:   False (default) returns the full response at once.
                  True not used in this prototype.
    Returns:
        The model's reply string, or an error message if the call fails.
    """
    try:
        payload  = {"model": MODEL, "messages": messages, "stream": False}
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        return (
            "⚠️ Could not connect to Ollama. "
            "Make sure Ollama is running (`ollama serve`) and Llama 3.2 is pulled "
            "(`ollama pull llama3.2`)."
        )
    except requests.exceptions.Timeout:
        return "⚠️ The model took too long to respond. Please try again."
    except Exception as e:
        return f"⚠️ Unexpected error: {e}"


def is_ollama_running() -> bool:
    """Quick health-check — returns True if Ollama is reachable."""
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False
