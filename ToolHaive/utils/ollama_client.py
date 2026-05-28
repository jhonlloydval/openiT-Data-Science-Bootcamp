"""
utils/ollama_client.py
───────────────────────────────────────────────────────────────────────────────
ToolHaive AI — Shared Ollama API Wrapper
All AI calls route through here so the model and URL are configured once.
───────────────────────────────────────────────────────────────────────────────
"""

import requests
import json
import os

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL      = "phi4-mini"
PROMPT_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

MODEL_OPTIONS = {
    "phi4-mini": {
        "label": "phi4-mini",
        "status": "available",
        "default": True,
    },
    "llama3.2": {
        "label": "llama3.2",
        "status": "available",
        "default": False,
    },
    "gemma3:4b": {
        "label": "gemma3:4b",
        "status": "TBA",
        "default": False,
    },
    "qwen3.5": {
        "label": "qwen3.5",
        "status": "TBA",
        "default": False,
    },
    "claude-3-5-sonnet": {
        "label": "claude-3-5-sonnet",
        "status": "TBA",
        "default": False,
    },
    "gemini-2.0-flash": {
        "label": "gemini-2.0-flash",
        "status": "TBA",
        "default": False,
    },
}


def load_prompt_template(filename: str) -> str:
    """Load a shared prompt template from ToolHaive's prompt directory."""
    path = os.path.join(PROMPT_TEMPLATE_DIR, filename)
    with open(path) as f:
        return f.read()


def scoped_system_prompt(
    tool_name: str,
    tool_scope: str,
    tool_prompt: str,
    refusal_message: str | None = None,
) -> str:
    """Combine the shared ToolHaive boundary with a tool-specific prompt."""
    refusal = refusal_message or (
        f"This request is outside the scope of {tool_name}. "
        "I can only assist with this tool's purpose."
    )
    template = load_prompt_template("tool_scope.txt")
    return template.format(
        tool_name=tool_name.strip(),
        tool_scope=tool_scope.strip(),
        refusal_message=refusal.strip(),
        tool_prompt=tool_prompt.strip(),
    )


def chat(messages: list[dict], stream: bool = False, model: str | None = None) -> str:
    """Send a message list to Ollama and return the assistant reply as a string.

    Args:
        messages: List of {"role": ..., "content": ...} dicts.
                  Include a system prompt only when a tool needs one.
        stream:   False (default) returns the full response at once.
                  True not used in this prototype.
        model:    Optional Ollama model name that overrides the default.
    Returns:
        The model's reply string, or an error message if the call fails.
    """
    try:
        selected_model = model or MODEL
        payload  = {"model": selected_model, "messages": messages, "stream": False}
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        return (
            "⚠️ Could not connect to Ollama. "
            "Make sure Ollama is running (`ollama serve`) and phi4-mini is pulled "
            "(`ollama pull phi4-mini`)."
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
