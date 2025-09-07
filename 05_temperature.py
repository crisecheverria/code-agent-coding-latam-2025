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

def chat(messages, system=None, temperature=0.7):
    params = {
        "model": "claude-4-sonnet-20250514",
        "max_tokens": 1024,
        "messages": messages,
        "temperature": temperature
    }

    if system:
        params["system"] = system

    message = client.messages.create( **params)


    return message.content[0].text

def main():
    try:
        print("Hola! Soy Claude, un agente de codificación. Escribe 'exit' o 'quit' para salir.")
        messages = []

        system = "You are a helpful coding assistant who provides clear and concise explanations."
        
        #system = "You are a patient coding assistant. Do not directly answer a user question. Guide users through coding problems step-by-step."
        
        while True:
            user_input = input("Tu: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Adios! 👋")
                break

            add_user_message(messages, user_input)
            response = chat(messages, system=system)
            add_assistant_message(messages, response)
            print(f"🤖 {response}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
