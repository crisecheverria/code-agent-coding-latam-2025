# Claude Agent

Ejemplo b�sico de uso de la API de Claude con Python.

## Setup

1. Instalar dependencias con uv:
   ```bash
   uv pip install anthropic python-dotenv
   ```

2. Crear archivo `.env` con tu API key:
   ```
   ANTHROPIC_API_KEY=tu_api_key_aqui
   ```

## C�digo

- `01_hello.py`: Ejemplo basico que envia un mensaje a Claude y recibe una respuesta. Usa el modelo `claude-4-sonnet-20250514` para generar un poema corto sobre el oceano.
- `02_chat.py`: Ejemplo de conversacion con multiples mensajes. Mantiene el historial de la conversacion y demuestra como hacer preguntas de seguimiento usando el contexto previo.
- `03_chat.py`: Chat interactivo por terminal con Claude. Permite mantener una conversación continua escribiendo mensajes en la consola. Escribe 'exit' o 'quit' para salir del chat.
