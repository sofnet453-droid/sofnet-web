import sqlite3

def crear_db():
    conn = sqlite3.connect("sofnet.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensajes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        correo TEXT,
        mensaje TEXT
    )
    """)

    conn.commit()
    conn.close()
