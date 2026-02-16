import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import (
    crear_db,
    guardar_mensaje,
    obtener_mensajes,
    validar_usuario,
    registrar_usuario,
    activar_usuario,
    crear_usuario_admin,
    obtener_usuarios,
    cambiar_estado_usuario
)
from functools import wraps

# Crear base de datos automáticamente
crear_db()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "sofnet_secret_key")

# ============================================================
# 🔐 DECORADOR PARA PROTEGER RUTAS
# ============================================================

def login_required(rol=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not session.get('usuario'):
                return redirect(url_for('login'))

            if rol and session.get('rol') != rol:
                return redirect(url_for('login'))

            return f(*args, **kwargs)
        return wrapped
    return decorator

# -------- INICIO --------
@app.route('/')
def inicio():
    return render_template('index.html')

# -------- SERVICIOS --------
@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

# -------- NOSOTROS --------
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

# -------- CONTACTO --------
@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# -------- LOGIN GENERAL --------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        usuario = validar_usuario(username, password)

        if usuario:
            session['usuario'] = usuario["username"]
            session['rol'] = usuario["rol"]
            flash("¡Bienvenido!")

            if usuario["rol"] == "admin":
                return redirect(url_for('dashboard_admin'))
            else:
                return redirect(url_for('dashboard_colaborador'))
        else:
            flash("Credenciales incorrectas o usuario no activado")

    return render_template('login.html')

# -------- LOGOUT --------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio'))

# ============================================================
# -------- REGISTRO (SIN ENVÍO DE CORREO) --------
# ============================================================

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmar = request.form.get('confirmar')

        # Validaciones básicas
        if not username or not email or not password or not confirmar:
            flash("Todos los campos son obligatorios")
            return redirect(url_for('registro'))

        if password != confirmar:
            flash("Las contraseñas no coinciden")
            return redirect(url_for('registro'))

        token, correo = registrar_usuario(username, email, password)

        if not token:
            flash("El usuario o correo ya existe")
            return redirect(url_for('registro'))

        flash("Cuenta registrada correctamente. Espera activación del administrador.")
        return redirect(url_for('login'))

    return render_template('registro.html')

# -------- CONFIRMAR CUENTA (opcional si decides usar token luego) --------
@app.route('/confirmar/<token>')
def confirmar(token):
    activar_usuario(token)
    flash("Cuenta activada correctamente.")
    return redirect(url_for('login'))

# ============================================================
# 🔐 DASHBOARD ADMIN
# ============================================================

@app.route('/dashboard/admin')
@login_required(rol="admin")
def dashboard_admin():
    mensajes = obtener_mensajes()
    usuarios = obtener_usuarios()

    return render_template(
        'dashboard_admin.html',
        mensajes=mensajes,
        usuarios=usuarios,
        rol=session.get('rol'),
        usuario=session.get('usuario')
    )

@app.route('/admin/usuarios')
@login_required(rol="admin")
def admin_usuarios():
    return render_template('admin_usuarios.html')

@app.route('/admin/roles')
@login_required(rol="admin")
def admin_roles():
    return render_template('admin_roles.html')

@app.route('/admin/mensajes')
@login_required(rol="admin")
def admin_mensajes():
    return render_template('admin_mensajes.html')

@app.route('/admin/configuracion')
@login_required(rol="admin")
def admin_configuracion():
    return render_template('admin_configuracion.html')

# ============================================================
# 👥 CREAR USUARIO DESDE ADMIN
# ============================================================

@app.route('/admin/crear_usuario', methods=['POST'])
@login_required(rol="admin")
def admin_crear_usuario():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    rol = request.form.get('rol')

    creado = crear_usuario_admin(username, email, password, rol)

    if creado:
        flash("Usuario creado correctamente")
    else:
        flash("Error: usuario o correo ya existe")

    return redirect(url_for('dashboard_admin'))

# ============================================================
# 🔄 ACTIVAR / DESACTIVAR USUARIO
# ============================================================

@app.route('/admin/cambiar_estado/<int:user_id>/<int:estado>')
@login_required(rol="admin")
def admin_cambiar_estado(user_id, estado):
    cambiar_estado_usuario(user_id, estado)
    flash("Estado actualizado correctamente")
    return redirect(url_for('dashboard_admin'))

# ============================================================
# 👨‍💼 DASHBOARD COLABORADOR
# ============================================================

@app.route('/dashboard/colaborador')
@login_required(rol="colaborador")
def dashboard_colaborador():
    return render_template(
        'dashboard_colaborador.html',
        rol=session.get('rol'),
        usuario=session.get('usuario')
    )

# -------- GUARDAR MENSAJE --------
@app.route('/enviar', methods=['POST'])
def enviar():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    mensaje = request.form.get('mensaje')

    guardar_mensaje(nombre, email, mensaje)
    flash("Mensaje enviado correctamente")
    return redirect(url_for('contacto'))

# -------- PUERTO --------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
