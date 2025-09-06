# Claude Agent

Ejemplo básico de uso de la API de Claude con Python.

## Setup

1. Instalar dependencias con uv:
   ```bash
   uv pip install anthropic python-dotenv
   ```

2. Crear archivo `.env` con tu API key:
   ```
   ANTHROPIC_API_KEY=tu_api_key_aqui
   ```

## Código

- `01_hello.py`: Ejemplo básico que envía un mensaje a Claude y recibe una respuesta. Usa el modelo `claude-4-sonnet-20250514` para generar un poema corto sobre el océano.