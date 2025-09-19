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
        model="claude-3-7-sonnet-20250219", max_tokens=1024, messages=messages
    )

    return message.content[0].text

def main():
    try:
        print("Hola! Soy Claude, un agente de codificación. Escribe 'exit' o 'quit' para salir.")
        messages = []
        while True:
            user_input = input("Tu: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Adios! 👋")
                break

            add_user_message(messages, user_input)
            response = chat(messages)
            add_assistant_message(messages, response)
            print(f"🤖 {response}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
