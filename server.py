from mcp.server.fastmcp import FastMCP

mcp = FastMCP("restaurante-http", host="0.0.0.0", port=8080)

MENU = [
    {"id": 1, "nombre": "Pizza", "precio": 120},
    {"id": 2, "nombre": "Hamburguesa", "precio": 80},
    {"id": 3, "nombre": "Ensalada", "precio": 60},
]
PEDIDOS = []


@mcp.tool()
def obtener_menu() -> str:
    return "\n".join([f"{i['id']}. {i['nombre']} (${i['precio']})" for i in MENU])


@mcp.tool()
def limpiar_pedidos() -> str:
    PEDIDOS.clear()
    return "Todos los pedidos han sido eliminados."


@mcp.tool()
def eliminar_pedido(indice: int) -> str:
    if 0 <= indice < len(PEDIDOS):
        pedido = PEDIDOS.pop(indice)
        return f"Pedido eliminado: {pedido['cantidad']} x {pedido['item']}"
    else:
        return "Índice de pedido inválido."


@mcp.tool()
def agregar_pedido(item_id: int, cantidad: int = 1) -> str:
    item = next((i for i in MENU if i["id"] == item_id), None)
    if not item:
        return "Producto no encontrado."
    PEDIDOS.append({"item": item["nombre"], "cantidad": cantidad})
    return f"Pedido agregado: {cantidad} x {item['nombre']}"


def ver_pedidos() -> str:
    if not PEDIDOS:
        return "No hay pedidos aún."
    return "\n".join(
        [f"{idx}. {p['cantidad']} x {p['item']}" for idx, p in enumerate(PEDIDOS)]
    )


if __name__ == "__main__":
    # El puerto y host se pasan aquí, NO en el constructor
    mcp.run(transport="sse")
