import ollama


RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"

PREFERRED_MODELS = ["llama3.2", "llama3", "qwen2.5", "mistral"]


def ui_header(model):
    print(f"{BOLD}{CYAN}" + "=" * 50 + f"{RESET}")
    print(f"{BOLD}{CYAN}  Simple Ollama Chatbot{RESET}")
    print(f"{YELLOW}  Model: {model}{RESET}")
    print(f"  Commands: /help  /model  /clear  /quit")
    print(f"{BOLD}{CYAN}" + "=" * 50 + f"{RESET}\n")


def get_available_models():
    data = ollama.list()
    models = data.get("models", [])
    names = []
    for m in models:
        name = m.get("model") or m.get("name")
        if name:
            names.append(name)
    return names


def choose_model(installed):
    for preferred in PREFERRED_MODELS:
        for name in installed:
            if name.startswith(preferred):
                return name
    return installed[0] if installed else None


def print_help():
    print(f"{YELLOW}Commands:{RESET}")
    print("  /help  - show commands")
    print("  /model - show current model")
    print("  /clear - clear chat memory")
    print("  /quit  - exit\n")


def main():
    try:
        installed = get_available_models()
    except Exception as e:
        print(f"{RED}Cannot reach Ollama server.{RESET}")
        print(f"Error: {e}")
        print("Tip: run 'ollama serve' first.")
        return

    model = choose_model(installed)
    if not model:
        print(f"{RED}No local models found in Ollama.{RESET}")
        print("Run: ollama pull llama3.2")
        return

    ui_header(model)
    messages = [{"role": "system", "content": "You are a helpful, concise assistant."}]

    while True:
        try:
            user_text = input(f"{GREEN}You > {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{CYAN}Bot > Goodbye!{RESET}")
            break

        if not user_text:
            continue

        cmd = user_text.lower()
        if cmd in {"/quit", "quit", "exit"}:
            print(f"{CYAN}Bot > Goodbye!{RESET}")
            break
        if cmd == "/help":
            print_help()
            continue
        if cmd == "/model":
            print(f"{YELLOW}Current model: {model}{RESET}\n")
            continue
        if cmd == "/clear":
            messages = [{"role": "system", "content": "You are a helpful, concise assistant."}]
            print(f"{YELLOW}Chat memory cleared.{RESET}\n")
            continue

        messages.append({"role": "user", "content": user_text})

        try:
            print(f"{CYAN}Bot > thinking...{RESET}")
            response = ollama.chat(model=model, messages=messages)
            bot_text = response["message"]["content"]
        except Exception as e:
            print(f"{RED}Bot > Request failed.{RESET}")
            print(f"Error: {e}")
            print("Tip: confirm model exists with `ollama list`.\n")
            continue

        print(f"{CYAN}Bot > {bot_text}{RESET}\n")
        messages.append({"role": "assistant", "content": bot_text})


if __name__ == "__main__":
    main()
