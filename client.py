import asyncio
import json
from mcp import ClientSession
from mcp.client.sse import sse_client
from openai import OpenAI
import os
from dotenv import load_dotenv
from src.printer import cprint

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

NUM_MESAS = 10
conversaciones = {}

COMANDOS = {
    "/back": "Regresa a la selección de mesas",
    "/clear": "Limpia la conversación de la mesa actual",
    "/help": "Muestra este mensaje de ayuda",
    "--help": "Muestra este mensaje de ayuda"
}

def build_openai_tool_schema(tool):
    schema = dict(tool.inputSchema)
    schema["additionalProperties"] = False  # Strict mode
    props = schema.get("properties", {})
    schema["required"] = list(props.keys())
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or f"Función {tool.name}",
            "parameters": schema,
            "strict": True,
        },
    }

def show_help():
    print("\nComandos disponibles:")
    for cmd, desc in COMANDOS.items():
        print(f"  {cmd:8} {desc}")
    print()

async def main():
    url = "http://localhost:8080/sse"
    async with sse_client(url) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            tools = await session.list_tools()
            openai_tools = [build_openai_tool_schema(tool) for tool in tools.tools]
            tool_schemas = {tool.name: tool for tool in tools.tools}  # Diccionario para consulta rápida

            print("Conectado al restaurante MCP HTTP.\n")

            while True:
                # Selección de mesa
                mesa = None
                while mesa is None:
                    print(f"Mesas disponibles: {', '.join(str(i) for i in range(1, NUM_MESAS + 1))}")
                    mesa_input = input("Selecciona el número de mesa (1-10): ").strip()
                    if mesa_input.isdigit() and 1 <= int(mesa_input) <= NUM_MESAS:
                        mesa = int(mesa_input)
                    else:
                        print("❌ Número de mesa inválido. Intenta de nuevo.\n")

                cprint("info", f"Has entrado a la mesa {mesa}. Escribe /help para ver los comandos disponibles.")

                # Conversación por mesa (historial propio)
                if mesa not in conversaciones:
                    conversaciones[mesa] = [
                        {
                            "role": "system",
                            "content": (
                                f"Eres un asistente para la mesa {mesa} del restaurante MCP. "
                                "Usa las herramientas proporcionadas para ayudar al usuario. "
                                f"Siempre que una herramienta requiera el parámetro 'mesa', usa el número {mesa}."
                            ),
                        }
                    ]
                messages = conversaciones[mesa]

                while True:
                    user_input = input("Mensaje (/help para comandos): ").strip()

                    # Comandos especiales
                    if user_input.lower() == "/back":
                        print("\nVolviendo a la selección de mesas...\n")
                        break
                    elif user_input.lower() in ("/help", "--help"):
                        show_help()
                        continue
                    elif user_input.lower() == "/clear":
                        conversaciones[mesa] = [
                            {
                                "role": "system",
                                "content": (
                                    f"Eres un asistente para la mesa {mesa} del restaurante MCP. "
                                    "Usa las herramientas proporcionadas para ayudar al usuario. "
                                    f"Siempre que una herramienta requiera el parámetro 'mesa', usa el número {mesa}."
                                ),
                            }
                        ]
                        messages = conversaciones[mesa]
                        print("🧹 Conversación limpiada.\n")
                        continue

                    cprint("user", user_input)
                    messages.append({"role": "user", "content": user_input})

                    # Llama a OpenAI
                    completion = client.chat.completions.create(
                        model="gpt-4.1",
                        messages=messages,
                        tools=openai_tools,
                    )

                    msg = completion.choices[0].message
                    tool_calls = getattr(msg, "tool_calls", None)
                    if tool_calls:
                        messages.append(
                            {
                                "role": "assistant",
                                "content": msg.content,
                                "tool_calls": [tc.model_dump() for tc in tool_calls],
                            }
                        )
                        for tool_call in tool_calls:
                            tool_name = tool_call.function.name
                            args = json.loads(tool_call.function.arguments)
                            # Inyectar 'mesa' si hace falta
                            if (
                                tool_name in tool_schemas and
                                "mesa" in tool_schemas[tool_name].inputSchema.get("properties", {}) and
                                "mesa" not in args
                            ):
                                args["mesa"] = mesa
                            result = await session.call_tool(tool_name, args)
                            messages.append(
                                {
                                    "role": "tool",
                                    "tool_call_id": tool_call.id,
                                    "content": result.content[0].text,
                                }
                            )
                        # Respuesta final de OpenAI
                        completion = client.chat.completions.create(
                            model="gpt-4.1",
                            messages=messages,
                            tools=openai_tools,
                        )
                        final_msg = completion.choices[0].message
                        cprint("assistant", final_msg.content)
                        messages.append({"role": "assistant", "content": final_msg.content})
                    else:
                        cprint("assistant", msg.content)
                        messages.append({"role": "assistant", "content": msg.content})

if __name__ == "__main__":
    asyncio.run(main())
