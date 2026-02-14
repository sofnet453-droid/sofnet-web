import sqlite3
import random, string

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
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        rol TEXT NOT NULL,
        activo INTEGER DEFAULT 0,  -- 0=inactivo, 1=activo
        token_confirmacion TEXT
    )
    """)

    # CREAR ADMIN POR DEFECTO SI NO EXISTE
    cursor.execute("SELECT * FROM usuarios WHERE username = ?", ("admin",))
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO usuarios (username, email, password, rol, activo)
        VALUES (?, ?, ?, ?, 1)
        """, ("admin", "admin@sofnet.com", "admin123", "admin"))

    conn.commit()
    conn.close()


# ---------------- FUNCIONES ----------------

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


# GENERAR TOKEN ALEATORIO
def generar_token(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# REGISTRAR USUARIO
def registrar_usuario(username, email, password, rol="colaborador"):
    conn = sqlite3.connect("sofnet.db")
    cursor = conn.cursor()
    token = generar_token()
    try:
        cursor.execute("""
            INSERT INTO usuarios (username, email, password, rol, activo, token_confirmacion)
            VALUES (?, ?, ?, ?, 0, ?)
        """, (username, email, password, rol, token))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return None, None
    conn.close()
    return token, email


# ACTIVAR USUARIO CON TOKEN
def activar_usuario(token):
    conn = sqlite3.connect("sofnet.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET activo=1, token_confirmacion=NULL WHERE token_confirmacion=?", (token,))
    conn.commit()
    conn.close()


# VALIDAR LOGIN ACTIVOS
def validar_usuario(username, password):
    conn = sqlite3.connect("sofnet.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM usuarios
        WHERE username=? AND password=? AND activo=1
    """, (username, password))
    usuario = cursor.fetchone()
    conn.close()
    return usuario
