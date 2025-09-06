import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()  # Load environment variables from a .env file if present

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages):
    message = client.messages.create(
        model="claude-4-sonnet-20250514", max_tokens=1024, messages=messages
    )

    return message.content[0].text

def main():
    try:
        messages = []
        add_user_message(messages, "Que es un coding agent? Respuesta corta")
        answer = chat(messages)
        print("Claude:", answer)
        add_assistant_message(messages, answer)
        add_user_message(messages, "Escribe otra sentencia")
        answer = chat(messages)
        print("Claude:", answer)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
