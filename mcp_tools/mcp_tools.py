import sqlite3
from mcp.server.fastmcp import FastMCP
import csv
import os
DB_FILE = "management/database.db"
MENU_FILE = "management/menu.csv"
PEDIDOS_FILE = "management/pedidos.csv"
mcp = FastMCP("restaurante-http", host="0.0.0.0", port=8080)
def cargar_menu():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, nombre, precio FROM menu")
    menu = [{"id": row[0], "nombre": row[1], "precio": row[2]} for row in c.fetchall()]
    conn.close()
    return menu


def guardar_menu(menu):
    with open(MENU_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "nombre", "precio"])
        writer.writeheader()
        for item in menu:
            writer.writerow(item)


def cargar_pedidos():
    pedidos = []
    if os.path.exists(PEDIDOS_FILE):
        with open(PEDIDOS_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pedidos.append(
                    {
                        "item": row["item"],
                        "cantidad": int(row["cantidad"]),
                        "mesa": int(row["mesa"]),
                    }
                )
    # cprint("pedidos", pedidos)
    return pedidos


def guardar_pedidos(pedidos):
    with open(PEDIDOS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["item", "cantidad", "mesa"])
        writer.writeheader()
        for pedido in pedidos:
            writer.writerow(pedido)




@mcp.tool(name="obtener_menu", description="Obtener el menú del restaurante")
def obtener_menu() -> str:
    breakpoint()
    menu = cargar_menu()
    return "\n".join([f"{i['id']}. {i['nombre']} (${i['precio']})" for i in menu])


@mcp.tool(name="listar_tablas", description="Listar todas las tablas y columnas de la base de datos")
def listar_tablas() -> str:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = c.fetchall()

    resultado = []
    for tabla in tablas:
        tabla_name = tabla[0]
        c.execute(f"PRAGMA table_info({tabla_name})")
        columnas = c.fetchall()
        columnas_str = ", ".join([col[1] + " (" + col[2] + ")" for col in columnas])
        resultado.append(f"{tabla_name}: {columnas_str}")

    conn.close()
    return "\n".join(resultado)



@mcp.tool(name="limpiar_pedidos", description="Limpiar los pedidos de una mesa")
def limpiar_pedidos(mesa: int) -> str:
    pedidos = cargar_pedidos()
    nuevos_pedidos = [p for p in pedidos if p["mesa"] != mesa]
    limpiar = len(pedidos) - len(nuevos_pedidos)
    guardar_pedidos(nuevos_pedidos)
    return f"Se eliminaron {limpiar} pedidos de la mesa {mesa}."


@mcp.tool(name="eliminar_pedido", description="Eliminar un pedido de la mesa")
def eliminar_pedido(mesa: int, indice: int) -> str:
    pedidos = cargar_pedidos()
    pedidos_mesa = [p for p in pedidos if p["mesa"] == mesa]
    if 0 <= indice < len(pedidos_mesa):
        pedido_a_eliminar = pedidos_mesa[indice]
        pedidos.remove(pedido_a_eliminar)
        guardar_pedidos(pedidos)
        return f"Pedido eliminado: {pedido_a_eliminar['cantidad']} x {pedido_a_eliminar['item']} de la mesa {mesa}"
    else:
        return "Índice de pedido inválido para esta mesa."


@mcp.tool(name="agregar_pedido", description="Agregar un pedido a la mesa")
def agregar_pedido(item_id: int, cantidad: int = 1, mesa: int = 1) -> str:
    menu = cargar_menu()
    pedidos = cargar_pedidos()
    item = next((i for i in menu if i["id"] == item_id), None)
    if not item:
        return "Producto no encontrado."
    pedidos.append({"item": item["nombre"], "cantidad": cantidad, "mesa": mesa})
    guardar_pedidos(pedidos)
    return f"Pedido agregado: {cantidad} x {item['nombre']} para la mesa {mesa}"


@mcp.tool(name="ver_pedidos_mesa", description="Ver los pedidos de una mesa")
def ver_pedidos_mesa(mesa: int) -> str:
    pedidos = cargar_pedidos()
    pedidos_mesa = [p for p in pedidos if p["mesa"] == mesa]
    if not pedidos_mesa:
        return f"No hay pedidos para la mesa {mesa}."
    return "\n".join(
        [f"{idx}. {p['cantidad']} x {p['item']}" for idx, p in enumerate(pedidos_mesa)]
    )
