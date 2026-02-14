import sqlite3

# CREAR BASE DE DATOS Y TABLAS
def crear_db():
    conn = sqlite3.connect("sofnet.db")
    cursor = conn.cursor()

    # TABLA DE MENSAJES DEL CONTACTO
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contactos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL,
        mensaje TEXT NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# GUARDAR MENSAJE
def guardar_mensaje(nombre, email, mensaje):
    conn = sqlite3.connect("sofnet.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO contactos(nombre, email, mensaje)
        VALUES (?, ?, ?)
    """, (nombre, email, mensaje))

    conn.commit()
    conn.close()


# VER MENSAJES (para panel admin futuro)
def obtener_mensajes():
    conn = sqlite3.connect("sofnet.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contactos ORDER BY fecha DESC")
    datos = cursor.fetchall()

    conn.close()
    return datos
