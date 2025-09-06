import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()  # Load environment variables from a .env file if present

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def main():
    try:
        message = client.messages.create(
            model="claude-4-sonnet-20250514",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Escribe un poema corto sobre el oceano"
                }
            ]
        )
        print("Claude:")
        print(message.content[0].text)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
