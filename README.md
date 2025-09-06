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

- `01_hello.py`: Ejemplo b�sico que env�a un mensaje a Claude y recibe una respuesta. Usa el modelo `claude-4-sonnet-20250514` para generar un poema corto sobre el oc�ano.
- `02_chat.py`: Ejemplo de conversaci�n con m�ltiples mensajes. Mantiene el historial de la conversaci�n y demuestra c�mo hacer preguntas de seguimiento usando el contexto previo.