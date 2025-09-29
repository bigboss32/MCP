import sqlite3
from . import mcp
from . import DB_FILE
import sqlite3
import pandas as pd
import os
from datetime import datetime

@mcp.tool(
    name="exportar_tabla_excel",
    description="Exportar los datos de una tabla específica a un archivo Excel"
)
def exportar_tabla_excel(nombre_tabla: str, ruta_destino: str = None) -> str:
    """
    Exporta los datos de una tabla SQLite a un archivo Excel.
    
    Args:
        nombre_tabla (str): Nombre de la tabla a exportar
        ruta_destino (str, optional): Ruta donde guardar el archivo Excel. 
                                    Si no se especifica, se guarda en el directorio actual
    
    Returns:
        str: Mensaje con el resultado de la operación
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (nombre_tabla,))
        if not c.fetchone():
            conn.close()
            return f"Error: La tabla '{nombre_tabla}' no existe en la base de datos."
        query = f"SELECT * FROM {nombre_tabla}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        if df.empty:
            return f"Advertencia: La tabla '{nombre_tabla}' está vacía."
        if ruta_destino is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ruta_destino = f"{nombre_tabla}_{timestamp}.xlsx"
        directorio = os.path.dirname(ruta_destino)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        with pd.ExcelWriter(ruta_destino, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=nombre_tabla, index=False)
            worksheet = writer.sheets[nombre_tabla]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)  
                worksheet.column_dimensions[column_letter].width = adjusted_width
        num_filas = len(df)
        num_columnas = len(df.columns)
        tamaño_archivo = os.path.getsize(ruta_destino)
        tamaño_mb = round(tamaño_archivo / 1024 / 1024, 2)
        
        resultado = f"""✅ Exportación exitosa:
📋 Tabla: {nombre_tabla}
📊 Datos: {num_filas} filas, {num_columnas} columnas
📁 Archivo: {ruta_destino}
💾 Tamaño: {tamaño_mb} MB
🕒 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        return resultado
        
    except sqlite3.Error as e:
        return f"❌ Error de base de datos: {str(e)}"
    except pd.errors.DatabaseError as e:
        return f"❌ Error al leer datos: {str(e)}"
    except PermissionError:
        return f"❌ Error de permisos: No se puede escribir en la ruta especificada."
    except Exception as e:
        return f"❌ Error inesperado: {str(e)}"
