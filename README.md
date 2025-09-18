# Claude Agent

Ejemplo basico de uso de la API de Claude con Python.

## Setup

1. Instalar dependencias con uv:
   ```bash
   uv pip install anthropic python-dotenv
   ```

2. Crear archivo `.env` con tu API key:
   ```
   ANTHROPIC_API_KEY=tu_api_key_aqui
   ```

## Codigo

- `01_hello.py`: Ejemplo basico que envia un mensaje a Claude y recibe una respuesta. Usa el modelo `claude-4-sonnet-20250514` para generar un poema corto sobre el oceano.
- `02_chat.py`: Ejemplo de conversacion con multiples mensajes. Mantiene el historial de la conversacion y demuestra como hacer preguntas de seguimiento usando el contexto previo.
- `03_chat.py`: Chat interactivo por terminal con Claude. Permite mantener una conversación continua escribiendo mensajes en la consola. Escribe 'exit' o 'quit' para salir del chat.
- `04_system_prompt.py`: Chat interactivo con system prompt personalizado. Demuestra como usar system prompts para definir el comportamiento del asistente como un ayudante de codificación que proporciona explicaciones claras y concisas.
- `05_temperature.py`: Chat interactivo que demuestra el uso del parámetro temperature para controlar la aleatoriedad de las respuestas.
- `06_edit_text_tool.py`: Chat interactivo con capacidades de editor de texto integrado. Permite a Claude leer, crear, editar y modificar archivos directamente usando la herramienta de editor de texto de Anthropic.
- `07_web_search_tool.py`: Chat interactivo con capacidades de búsqueda web en tiempo real. Combina el editor de texto con búsqueda web limitada a sitios de desarrollo (Stack Overflow, GitHub, docs oficiales).

## Herramienta de Editor de Texto (`06_edit_text_tool.py`)

El archivo `06_edit_text_tool.py` implementa la herramienta de editor de texto integrada de Anthropic (`text_editor_20250728`), permitiendo a Claude interactuar directamente con archivos del sistema.

### Capacidades del Editor de Texto

- **Leer archivos**: Ver contenido completo o rangos específicos de líneas con numeración
- **Crear archivos**: Crear nuevos archivos con contenido especificado
- **Editar archivos**: Reemplazar texto específico con coincidencia exacta
- **Insertar texto**: Agregar contenido en líneas específicas
- **Listar directorios**: Explorar contenidos de carpetas

### Comandos Disponibles

1. **view**: Lee archivos o lista directorios
2. **create**: Crea nuevos archivos
3. **str_replace**: Reemplaza texto específico en archivos existentes
4. **insert**: Inserta texto en una línea específica

### Características de Seguridad

- Prevención de directory traversal (`..`, rutas absolutas)
- Restricción a extensiones de archivo permitidas (`.py`, `.txt`, `.md`, `.json`, etc.)
- Creación automática de respaldos antes de editar archivos existentes
- Validación de coincidencias únicas para reemplazos de texto

### Ejemplos de Uso

```
- "Lee el archivo test.py"
- "Crea un archivo llamado fibonacci.py con código de ejemplo"
- "Arregla el error de sintaxis en mi archivo"
- "Lista los archivos en el directorio actual"
- "Reemplaza la función antigua con una nueva implementación"
```

## Parámetro Temperature

El parámetro `temperature` controla la aleatoriedad de las respuestas (rango: 0.0 - 1.0):

- **Temperature Baja (0.0 - 0.3)**: Respuestas más deterministas y enfocadas. Ideal para respuestas fácticas y asistencia en programación.
- **Temperature Media (0.4 - 0.7)**: Balance entre creatividad y coherencia. Perfecto para respuestas educativas y resolución de problemas.
- **Temperature Alta (0.8 - 1.0)**: Alta creatividad y variedad en respuestas. Excelente para lluvia de ideas y narrativa.
