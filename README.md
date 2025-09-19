# 🤖 Claude Agent Tutorial

> **Aprende a construir agentes de IA con Claude paso a paso**

Una guía completa y progresiva para desarrollar agentes inteligentes usando la API de Claude de Anthropic. Desde mensajes básicos hasta agentes avanzados con herramientas y streaming en tiempo real.

## 📋 Navegación

| Sección | Descripción |
|---------|-------------|
| [🚀 ¿Qué son los Claude Agents?](#-qué-son-los-claude-agents) | Introducción y capacidades |
| [⚙️ Configuración](#️-configuración-inicial) | Setup inicial y API key |
| [📚 Tutorial Progresivo](#-tutorial-progresivo) | 8 niveles de aprendizaje |
| [🌟 Nivel 1: Primer Mensaje](#-nivel-1-primer-mensaje---01_hellopy) | Mensaje básico |
| [🔄 Nivel 2: Conversación](#-nivel-2-conversación-con-memoria---02_chatpy) | Historial de chat |
| [💬 Nivel 3: Chat Interactivo](#-nivel-3-chat-interactivo---03_chatpy) | Terminal interactiva |
| [🎭 Nivel 4: System Prompts](#-nivel-4-personalidad-con-system-prompts---04_system_promptpy) | Personalidad |
| [🎲 Nivel 5: Temperature](#-nivel-5-control-de-creatividad---05_temperaturepy) | Control de creatividad |
| [📝 Nivel 6: Editor de Texto](#-nivel-6-herramientas-de-edición---06_edit_text_toolpy) | Manipulación de archivos |
| [🔍 Nivel 7: Búsqueda Web](#-nivel-7-búsqueda-web---07_web_search_toolpy) | Búsqueda en tiempo real |
| [⚡ Nivel 8: Streaming](#-nivel-8-streaming-avanzado---08_data_streamingpy) | Respuestas en streaming |
| [🏃‍♂️ Guía Rápida](#️-guía-de-ejecución-rápida) | Comandos de ejecución |
| [🎯 Casos de Uso](#-casos-de-uso-prácticos) | Ejemplos prácticos |
| [📖 Recursos](#-recursos-adicionales) | Links útiles |
| [🤝 Contribuir](#-contribuir) | Cómo colaborar |

---

## 🚀 ¿Qué son los Claude Agents?

Los **Claude Agents** son programas que utilizan la API de Claude para crear experiencias de IA interactivas y potentes. Pueden:

- 💬 Mantener conversaciones complejas
- 🛠️ Usar herramientas para interactuar con archivos y sistemas
- 🔍 Buscar información en tiempo real
- 📊 Procesar datos con streaming eficiente
- 🎯 Adaptarse a diferentes roles y personalidades

---

<br>

<br>

<br>

<br>

<br>

<br>

<br>

<br>

## ⚙️ Configuración Inicial

### 1. Instalar dependencias

```bash
uv pip install anthropic python-dotenv
```

### 2. Configurar API Key

Crea un archivo `.env` en la raíz del proyecto:

```env
ANTHROPIC_API_KEY=tu_api_key_aqui
```

### 3. Obtener tu API Key

1. Visita [console.anthropic.com](https://console.anthropic.com)
2. Crea una cuenta o inicia sesión
3. Genera una nueva API key en la sección "API Keys"

---

<br>

<br>

<br>

<br>

<br>

<br>

<br>

<br>

## 📚 Tutorial Progresivo

### 🌟 Nivel 1: Primer Mensaje - `01_hello.py`

**Concepto**: Aprende lo básico enviando un mensaje simple a Claude.

```python
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def main():
    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": "Escribe un poema corto sobre el oceano"
        }]
    )
    print("Claude:", message.content[0].text)
```

**✨ Características:**
- Configuración básica del cliente
- Mensaje único
- Respuesta simple

---

<br>

<br>

<br>

<br>

<br>

<br>

<br>

<br>

### 🔄 Nivel 2: Conversación con Memoria - `02_chat.py`

**Concepto**: Mantén el contexto entre mensajes para conversaciones más naturales.

```python
def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages):
    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=1024,
        messages=messages
    )
    return message.content[0].text

# Mantener historial de conversación
messages = []
add_user_message(messages, "¿Qué es un coding agent?")
response = chat(messages)
add_assistant_message(messages, response)

# Segunda pregunta con contexto
add_user_message(messages, "Dame un ejemplo práctico")
response = chat(messages)
```

**✨ Nuevas características:**
- ➕ Historial de conversación
- ➕ Contexto persistente
- ➕ Funciones de utilidad

---

<br>

<br>

<br>

<br>

<br>

<br>

<br>

<br>

### 💬 Nivel 3: Chat Interactivo - `03_chat.py`

**Concepto**: Crea una interfaz de chat en terminal para interacción en tiempo real.

```python
def main():
    print("¡Hola! Soy Claude. Escribe 'exit' o 'quit' para salir.")
    messages = []

    while True:
        user_input = input("Tu: ")
        if user_input.lower() in ['exit', 'quit']:
            print("¡Adiós! 👋")
            break

        add_user_message(messages, user_input)
        response = chat(messages)
        add_assistant_message(messages, response)
        print(f"🤖 {response}")
```

**✨ Nuevas características:**
- ➕ Interfaz de terminal interactiva
- ➕ Loop de conversación continua
- ➕ Comandos de salida

---

<br>

<br>

<br>

<br>

<br>

<br>

<br>

<br>

### 🎭 Nivel 4: Personalidad con System Prompts - `04_system_prompt.py`

**Concepto**: Define el comportamiento y personalidad del agente.

```python
def chat(messages, system=None):
    params = {
        "model": "claude-3-7-sonnet-20250219",
        "max_tokens": 1024,
        "messages": messages
    }

    if system:
        params["system"] = system

    return client.messages.create(**params)

# Definir personalidad
system = "Eres un asistente de programación que proporciona explicaciones claras y concisas."

# Usar en la conversación
response = chat(messages, system=system)
```

**✨ Nuevas características:**
- ➕ System prompts para personalidad
- ➕ Comportamiento personalizable
- ➕ Roles específicos (tutor, experto, etc.)

---

<br>

<br>

<br>

<br>

<br>

<br>

<br>

<br>

### 🎲 Nivel 5: Control de Creatividad - `05_temperature.py`

**Concepto**: Controla la creatividad y determinismo de las respuestas.

```python
def chat(messages, system=None, temperature=0.7):
    params = {
        "model": "claude-3-7-sonnet-20250219",
        "max_tokens": 1024,
        "messages": messages,
        "temperature": temperature  # 0.0 = determinista, 1.0 = creativo
    }

    if system:
        params["system"] = system

    return client.messages.create(**params)
```

**🌡️ Niveles de Temperature:**
- **0.0 - 0.3**: Respuestas precisas y deterministas (ideal para código)
- **0.4 - 0.7**: Balance entre precisión y creatividad
- **0.8 - 1.0**: Máxima creatividad (ideal para brainstorming)

**✨ Nuevas características:**
- ➕ Control de creatividad
- ➕ Respuestas más predecibles o variadas
- ➕ Adaptabilidad al tipo de tarea

---

<br>

<br>

<br>

<br>

<br>

<br>

<br>

<br>

### 📝 Nivel 6: Herramientas de Edición - `06_edit_text_tool.py`

**Concepto**: Claude puede leer, crear y modificar archivos directamente.

```python
def chat(messages, system=None, temperature=0.7):
    params = {
        "model": "claude-3-7-sonnet-20250219",
        "max_tokens": 1024,
        "messages": messages,
        "temperature": temperature,
        "tools": [{
            "type": "text_editor_20250124",
            "name": "str_replace_editor",
        }]
    }

    if system:
        params["system"] = system

    return client.messages.create(**params)
```

**🛠️ Capacidades del Editor:**
- **📖 view**: Leer archivos y directorios
- **✏️ str_replace**: Reemplazar texto específico
- **📄 create**: Crear nuevos archivos
- **➕ insert**: Insertar texto en líneas específicas

**✨ Nuevas características:**
- ➕ Manipulación de archivos
- ➕ Lectura de código
- ➕ Edición asistida por IA
- ➕ Gestión automática de herramientas

---

<br>

<br>

<br>

<br>

<br>

<br>

<br>

<br>

### 🔍 Nivel 7: Búsqueda Web - `07_web_search_tool.py`

**Concepto**: Acceso a información actualizada en tiempo real.

```python
"tools": [
    {
        "type": "text_editor_20250124",
        "name": "str_replace_editor",
    },
    {
        "type": "web_search_20250305",
        "name": "web_search",
        "max_uses": 5,
        "allowed_domains": [
            "stackoverflow.com",
            "github.com",
            "docs.python.org",
            "developer.mozilla.org",
            "w3schools.com",
        ],
    }
]
```

**🌐 Dominios Permitidos:**
- **Stack Overflow**: Soluciones de programación
- **GitHub**: Repositorios y ejemplos
- **Documentación oficial**: Python, MDN, W3Schools

**✨ Nuevas características:**
- ➕ Búsqueda web en tiempo real
- ➕ Información actualizada
- ➕ Citación automática de fuentes
- ➕ Límites de seguridad

---

<br>

<br>

<br>

<br>

<br>

<br>

<br>

<br>

### ⚡ Nivel 8: Streaming Avanzado - `08_data_streaming.py`

**Concepto**: Respuestas en tiempo real con streaming de herramientas.

```python
def chat_stream(messages, system=None, temperature=0.7):
    params = {
        "model": "claude-3-7-sonnet-20250219",
        "max_tokens": 4096,
        "messages": messages,
        "temperature": temperature,
        "tools": [
            {"type": "text_editor_20250124", "name": "str_replace_editor"},
            {
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 5,
                "allowed_domains": ["stackoverflow.com", "github.com", ...]
            }
        ],
        "betas": ["fine-grained-tool-streaming-2025-05-14"],
    }

    if system:
        params["system"] = system

    return client.beta.messages.stream(**params)
```

**⚡ Características del Streaming:**
- **🚀 Respuestas instantáneas**: Ver texto mientras se genera
- **🔧 Tool streaming**: Seguimiento en tiempo real del uso de herramientas
- **📊 Progreso visual**: Indicadores de estado y progreso
- **🔄 Manejo automático**: Procesamiento de respuestas complejas

**✨ Nuevas características:**
- ➕ Streaming de texto en tiempo real
- ➕ Streaming de parámetros de herramientas
- ➕ Experiencia de usuario mejorada
- ➕ Manejo de múltiples herramientas simultáneamente

---

<br>

<br>

<br>

<br>

<br>

<br>

<br>

<br>
<br>

## 🏃‍♂️ Guía de Ejecución Rápida

```bash
# Ejecutar los ejemplos en orden
uv run 01_hello.py          # Primer mensaje
uv run 02_chat.py           # Conversación
uv run 03_chat.py           # Chat interactivo
uv run 04_system_prompt.py  # Con personalidad
uv run 05_temperature.py    # Con creatividad
uv run 06_edit_text_tool.py # Con edición de archivos
uv run 07_web_search_tool.py # Con búsqueda web
uv run 08_data_streaming.py  # Con streaming avanzado
```

---

<br>

<br>

<br>

<br>

<br>

<br>

<br>

<br>

## 🎯 Casos de Uso Prácticos

### 👨‍💻 Asistente de Programación
```python
system = "Eres un experto en Python. Ayudas a escribir código limpio y eficiente."
```

### 📚 Tutor Interactivo
```python
system = "Eres un tutor paciente. Guía paso a paso sin dar respuestas directas."
```

### 🔍 Investigador
```python
system = "Eres un investigador meticuloso. Siempre citas fuentes y verificas información."
```

---

<br>

<br>

<br>

<br>

<br>

<br>

<br>

<br>

## 📖 Recursos Adicionales

- 📘 [Documentación oficial de Anthropic](https://docs.anthropic.com)
- 🛠️ [API Reference](https://docs.anthropic.com/claude/reference)
- 💡 [Guías de mejores prácticas](https://docs.anthropic.com/claude/docs)
- 🔧 [Herramientas disponibles](https://docs.anthropic.com/claude/docs/tool-use)

---

## 🤝 Contribuir

¿Tienes ideas para mejorar los ejemplos? ¡Las contribuciones son bienvenidas!

1. Fork el repositorio
2. Crea tu rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

<div align="center">

**🚀 ¡Construye el futuro con Claude Agents! 🚀**

[Comenzar Tutorial](#-nivel-1-primer-mensaje---01_hellopy) • [API Docs](https://docs.anthropic.com) • [Ejemplos](/)

</div>
