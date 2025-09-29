import sqlite3
from . import mcp
from . import DB_FILE
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

@mcp.tool(
    name="crear_tabla",
    description="Ejecuta una sentencia SQL para crear una tabla en SQLite"
)
def crear_tabla(sql: str) -> str:
    """
    sql: sentencia SQL de creación de tabla, por ejemplo:
         CREATE TABLE IF NOT EXISTS clientes (
             id INTEGER PRIMARY KEY,
             nombre TEXT,
             correo TEXT
         );
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
        return f"Tabla creada correctamente o ya existe."
    except Exception as e:
        return f"Error al crear tabla: {str(e)}"
    

@mcp.tool(name="obtener_estructura_tabla", description="Devuelve columnas y tipos de una tabla SQLite")
def obtener_estructura_tabla(tabla_name: str) -> str:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(f"PRAGMA table_info({tabla_name})")
    columnas = c.fetchall()
    conn.close()
    if not columnas:
        return f"La tabla '{tabla_name}' no existe."
    return "\n".join([f"{col[1]} ({col[2]})" for col in columnas])