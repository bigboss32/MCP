from . import mcp
from .db_utils import cargar_menu


@mcp.tool(name="obtener_menu", description="Obtener el menú del restaurante")
def obtener_menu() -> str:
    menu = cargar_menu()
    return "\n".join([f"{i['id']}. {i['nombre']} (${i['precio']})" for i in menu])
