import sqlite3
import csv
import os
from . import DB_FILE

def cargar_menu():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, nombre, precio FROM menu")
    menu = [{"id": row[0], "nombre": row[1], "precio": row[2]} for row in c.fetchall()]
    conn.close()
    return menu

