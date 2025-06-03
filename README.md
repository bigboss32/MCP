# Restaurante MCP - Ejemplo

Este repositorio demuestra un restaurante digital conversacional usando **MCP** (Model Context Protocol), Python, y OpenAI GPT.

---

## 🚀 Descripción

- Menú digital con emojis 🍕🍔
- Pedidos por mesa (¡hasta 10 mesas simultáneas, peor puede ser cualquier número!)
- Comandos útiles para limpiar, cambiar de mesa, ayuda, etc.
- Mock de link de pago
- Cliente conversacional potenciado con GPT y herramientas MCP

---

## ⚡ Instalación y primer uso

> **Requisito:** Tener instalado [`uv`](https://github.com/astral-sh/uv) ([guía oficial de instalación](https://github.com/astral-sh/uv#installation))

### 1. Clona el repositorio

```bash
git clone https://github.com/Charlytoc/mcp-server-client.git
cd mcp-server-client
```

### 2. Configura tu API KEY de OpenAI

Crea un archivo `.env` en la raíz y agrega:

```
OPENAI_API_KEY=sk-...
```

### 3. Ejecuta el proyecto

```bash
bash start.sh
```

Este comando:

- Crea y activa el entorno virtual (si no existe)
- Instala dependencias automáticamente con `uv`
- Lanza el servidor y el cliente en terminal interactiva

---

## 📝 Estructura principal

- `server.py` → Lógica del restaurante y API MCP
- `client.py` → Cliente conversacional
- `management/menu.csv` → Menú editable (¡puedes usar emojis!)
- `management/pedidos.csv` → Pedidos por mesa (se genera solo)
- `start.sh` → Script de arranque automático

---

## 💡 Objetivo

El objetivo de este proyecto es demostrar cómo se puede usar MCP para crear un restaurante digital conversacional de una forma sencilla y sin necesidad de grandes conocimientos de IA.

---

## 📋 Ejemplo de menú con emojis

```csv
id,nombre,precio
1,🍕 Pizza,120
2,🍔 Hamburguesa,80
3,🥗 Ensalada,60
4,🍪 Cookie de Oreo,10
5,🥖 Pan de Jamón,30
# ... y más
```

---

## 🛠️ Personaliza el menú

Edita el archivo `management/menu.csv` para agregar, quitar o modificar productos.  
Puedes usar **emojis** en los nombres para hacerlo más visual.

---

## 🧪 Funcionalidades MCP disponibles

- Ver menú
- Agregar pedido
- Eliminar pedido
- Limpiar pedidos de una mesa
- Ver pedidos de una mesa
- Calcular total de la cuenta
- Generar link de pago mock

---

## ⚠️ Notas técnicas

- Si el puerto `8080` aparece ocupado, puedes liberarlo con:
  - `netstat -ano | findstr :8080` (ver PID)
  - `taskkill /PID <PID> /F` (matar proceso)
- El entorno virtual y dependencias se gestionan automáticamente por `start.sh` usando [`uv`](https://github.com/astral-sh/uv).
- El script detecta el sistema operativo para guiar la instalación de `uv` si falta.

---

## 📣 Créditos

- Proyecto de ejemplo MCP (**Model Context Protocol**) por [@Charlytoc](https://github.com/Charlytoc)
- Basado en [OpenAI GPT](https://platform.openai.com/) y [MCP](https://github.com/Charlytoc/mcp-server-client)

---

¿Dudas o sugerencias?  
¡Abre un issue o escribe en Discussions!

---
