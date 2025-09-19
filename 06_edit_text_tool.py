import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file if present

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages, content):
    assistant_message = {"role": "assistant", "content": content}
    messages.append(assistant_message)


def chat(messages, system=None, temperature=0.7):
    params = {
        "model": "claude-3-7-sonnet-20250219",
        "max_tokens": 1024,
        "messages": messages,
        "temperature": temperature,
        "tools": [
            {
                "type": "text_editor_20250124",
                "name": "str_replace_editor",
            }
        ],
    }

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message


def handle_text_editor_tool(tool_call):
    """Handle text editor tool calls from Claude according to official documentation."""
    try:
        input_params = tool_call.input
        command = input_params.get("command", "")
        file_path = input_params.get("path", "")

        # Debug logging
        print(f"🔍 Tool call - Command: {command}, Path: {file_path}")
        print(f"🔍 All input params: {input_params}")

        # Normalize path to current directory
        if file_path.startswith("/"):
            # Remove leading slash to make it relative to current directory
            file_path = file_path.lstrip("/")
            print(f"🔧 Normalized path: {file_path}")

        # Security check: prevent directory traversal but allow relative paths
        if ".." in file_path:
            return "Error: Invalid file path for security reasons"

        # Restrict to certain file extensions for safety
        allowed_extensions = {
            ".py",
            ".txt",
            ".md",
            ".json",
            ".yaml",
            ".yml",
            ".js",
            ".ts",
            ".html",
            ".css",
            ".sh",
            "",
        }
        path = Path(file_path)
        if path.suffix.lower() not in allowed_extensions:
            return f"Error: File extension '{path.suffix}' not allowed for security reasons"

        if command == "view":
            view_range = input_params.get("view_range")
            return handle_view(file_path, view_range)
        elif command == "str_replace":
            old_str = input_params.get("old_str", "")
            new_str = input_params.get("new_str", "")

            # Workaround: If old_str is empty and file is empty, treat as content insertion
            if old_str == "" and Path(file_path).exists():
                try:
                    with open(Path(file_path), "r", encoding="utf-8") as f:
                        current_content = f.read()
                    if current_content.strip() == "":
                        print(
                            "🔧 Workaround: Converting empty str_replace to file content insertion"
                        )
                        with open(Path(file_path), "w", encoding="utf-8") as f:
                            f.write(new_str)
                        return f"Successfully added content to {file_path}"
                except Exception as e:
                    print(f"Workaround failed: {e}")

            return handle_str_replace(file_path, old_str, new_str)
        elif command == "create":
            file_text = input_params.get("file_text", "")
            return handle_create(file_path, file_text)
        elif command == "insert":
            insert_line = input_params.get("insert_line", 0)
            new_str = input_params.get("new_str", "")
            return handle_insert(file_path, insert_line, new_str)
        else:
            return f"Error: Unknown command '{command}'"

    except Exception as e:
        return f"Error: {str(e)}"


def handle_view(file_path, view_range=None):
    """Handle view command to read file contents or list directory."""
    try:
        path = Path(file_path)

        if path.is_dir():
            # List directory contents
            items = []
            for item in sorted(path.iterdir()):
                if item.is_dir():
                    items.append(f"{item.name}/")
                else:
                    items.append(item.name)
            return f"Directory contents of {file_path}:\n" + "\n".join(items)

        elif path.is_file():
            # Read file contents
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if view_range:
                start_line, end_line = view_range
                if end_line == -1:
                    end_line = len(lines)
                lines = lines[start_line - 1 : end_line]

            # Add line numbers
            numbered_lines = []
            start_num = view_range[0] if view_range else 1
            for i, line in enumerate(lines):
                numbered_lines.append(f"{start_num + i}: {line.rstrip()}")

            return "\n".join(numbered_lines)

        else:
            return "Error: File not found"

    except Exception as e:
        return f"Error reading file: {str(e)}"


def handle_str_replace(file_path, old_str, new_str):
    """Handle string replacement in file."""
    try:
        path = Path(file_path)
        if not path.exists():
            return "Error: File not found"

        # Read file
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for matches
        count = content.count(old_str)
        if count == 0:
            return "Error: No match found for replacement text"
        elif count > 1:
            return f"Error: Found {count} matches for replacement text. Please provide more context to make a unique match"

        # Perform replacement
        new_content = content.replace(old_str, new_str)

        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)

        return "Successfully replaced text at exactly one location"

    except Exception as e:
        return f"Error during replacement: {str(e)}"


def handle_create(file_path, file_text):
    """Handle file creation."""
    try:
        path = Path(file_path)

        if path.exists():
            return f"Error: File {file_path} already exists"

        # Create parent directories if needed
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(file_text)

        return f"Successfully created file {file_path}"

    except Exception as e:
        return f"Error creating file: {str(e)}"


def handle_insert(file_path, insert_line, new_str):
    """Handle text insertion at specific line."""
    try:
        path = Path(file_path)
        if not path.exists():
            return "Error: File not found"

        # Read file
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Insert text
        if insert_line == 0:
            lines.insert(0, new_str + "\n")
        else:
            lines.insert(insert_line, new_str + "\n")

        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        return f"Successfully inserted text at line {insert_line}"

    except Exception as e:
        return f"Error during insertion: {str(e)}"


def process_claude_response(response, messages):
    """Process Claude's response and handle any tool calls."""
    response_content = []
    has_tool_use = False

    for content in response.content:
        if content.type == "text":
            response_content.append(content)
            print(f"🤖 {content.text}")
        elif content.type == "tool_use":
            response_content.append(content)
            print(f"🔧 Claude is using tool: {content.name}")
            has_tool_use = True

    # Add Claude's response to messages first
    add_assistant_message(messages, response_content)

    # Then handle tool use if present
    if has_tool_use:
        tool_results = []
        for content in response.content:
            if content.type == "tool_use":
                if content.name == "str_replace_editor":
                    tool_result = handle_text_editor_tool(content)
                    print(f"📁 Tool result: {tool_result}")

                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": tool_result,
                        }
                    )

        # Add tool results to conversation
        if tool_results:
            messages.append({"role": "user", "content": tool_results})

            try:
                # Continue the conversation to get Claude's response to the tool result
                follow_up = chat(
                    messages,
                    system="You are a helpful coding assistant with text editor capabilities.",
                )
                # Only process follow-up if Claude has something more to say
                if follow_up.content and any(
                    c.type == "text" and c.text.strip() for c in follow_up.content
                ):
                    return process_claude_response(follow_up, messages)
            except Exception as e:
                print(f"Error in follow-up response: {e}")
                return False

    return True


def main():
    try:
        print(
            "Hola! Soy Claude, un agente de codificación con capacidades de editor de texto."
        )
        print(
            "Puedes pedirme que lea, edite, o cree archivos. Escribe 'exit' o 'quit' para salir."
        )
        print("Ejemplos:")
        print("- 'Lee el archivo test.py'")
        print("- 'Crea un archivo llamado hello.py con código básico'")
        print("- 'Arregla el error de sintaxis en mi archivo'")
        print()

        messages = []
        system = "You are a helpful coding assistant with text editor capabilities. You can read, create, and modify files to help users with their programming tasks."

        while True:
            user_input = input("Tu: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Adios! 👋")
                break

            add_user_message(messages, user_input)
            response = chat(messages, system=system)
            process_claude_response(response, messages)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
