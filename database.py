import sqlite3

# CREAR BASE DE DATOS Y TABLAS
def crear_db():
    conn = sqlite3.connect("sofnet.db")
    cursor = conn.cursor()

    # TABLA CONTACTOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contactos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL,
        mensaje TEXT NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # TABLA USUARIOS (ADMIN Y COLABORADORES)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        rol TEXT NOT NULL
    )
    """)

    # CREAR ADMIN POR DEFECTO SI NO EXISTE
    cursor.execute("SELECT * FROM usuarios WHERE username = ?", ("admin",))
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO usuarios (username, password, rol)
        VALUES (?, ?, ?)
        """, ("admin", "admin123", "admin"))

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


# OBTENER MENSAJES
def obtener_mensajes():
    conn = sqlite3.connect("sofnet.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contactos ORDER BY fecha DESC")
    datos = cursor.fetchall()

    conn.close()
    return datos


# VALIDAR USUARIO
def validar_usuario(username, password):
    conn = sqlite3.connect("sofnet.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM usuarios
        WHERE username=? AND password=?
    """, (username, password))

    usuario = cursor.fetchone()
    conn.close()
    return usuario
