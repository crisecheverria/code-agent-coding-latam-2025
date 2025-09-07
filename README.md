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
- `04_system_prompt.py`: Chat interactivo con system prompt personalizado. Demuestra como usar system prompts para definir el comportamiento del asistente como un ayudante de codificación que proporciona explicaciones claras y concisas.
- `05_temperature.py`: Chat interactivo que demuestra el uso del parámetro temperature para controlar la aleatoriedad de las respuestas.

## Parámetro Temperature

El parámetro `temperature` controla la aleatoriedad de las respuestas (rango: 0.0 - 1.0):

- **Temperature Baja (0.0 - 0.3)**: Respuestas más deterministas y enfocadas. Ideal para respuestas fácticas y asistencia en programación.
- **Temperature Media (0.4 - 0.7)**: Balance entre creatividad y coherencia. Perfecto para respuestas educativas y resolución de problemas.
- **Temperature Alta (0.8 - 1.0)**: Alta creatividad y variedad en respuestas. Excelente para lluvia de ideas y narrativa.
