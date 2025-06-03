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


def build_openai_tool_schema(tool):
    schema = dict(tool.inputSchema)
    schema["additionalProperties"] = False  # Strict mode

    # OpenAI strict mode: all properties must be required!
    props = schema.get("properties", {})
    # If 'required' is missing or incomplete, fix it:
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


async def main():
    url = "http://localhost:8080/sse"
    async with sse_client(url) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            tools = await session.list_tools()
            openai_tools = [build_openai_tool_schema(tool) for tool in tools.tools]
            messages = [
                {
                    "role": "system",
                    "content": "Eres un asistente para el restaurante MCP. Usa las herramientas proporcionadas para ayudar al usuario.",
                }
            ]
            print("Conectado al restaurante MCP HTTP.\n")
            while True:
                user_input = input("¿Qué quieres hacer o preguntar?: ").strip()
                cprint("user", user_input)
                messages.append({"role": "user", "content": user_input})

                completion = client.chat.completions.create(
                    model="gpt-4.1",
                    messages=messages,
                    tools=openai_tools,
                )

                msg = completion.choices[0].message
                tool_calls = getattr(msg, "tool_calls", None)
                if tool_calls:
                    # 1. Agrega el mensaje del asistente que contiene las tool_calls
                    messages.append(
                        {
                            "role": "assistant",
                            "content": msg.content,
                            "tool_calls": [tc.model_dump() for tc in tool_calls],
                        }
                    )
                    # 2. Por cada tool_call, ejecuta y agrega el mensaje de tool
                    for tool_call in tool_calls:
                        tool_name = tool_call.function.name
                        args = json.loads(tool_call.function.arguments)
                        result = await session.call_tool(tool_name, args)
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": result.content[0].text,
                            }
                        )
                    # 3. Ahora pide la respuesta final de OpenAI
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
