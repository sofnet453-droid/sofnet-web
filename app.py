import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import crear_db, guardar_mensaje, obtener_mensajes, validar_usuario, registrar_usuario, activar_usuario
import smtplib
from email.message import EmailMessage

# Crear base de datos automáticamente
crear_db()

app = Flask(__name__)
app.secret_key = "sofnet_secret_key"

# ============================================================
# 🔹 GOOGLE OAUTH DESACTIVADO TEMPORALMENTE
# ============================================================
# from flask_dance.contrib.google import make_google_blueprint, google
#
# google_bp = make_google_blueprint(
#     client_id=os.environ.get("GOOGLE_CLIENT_ID"),
#     client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
#     scope=["profile", "email"]
# )
#
# app.register_blueprint(google_bp, url_prefix="/login")

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
        username = request.form['username']
        password = request.form['password']

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

# -------- REGISTRO --------
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirmar = request.form['confirmar']

        if password != confirmar:
            flash("Las contraseñas no coinciden")
            return redirect(url_for('registro'))

        token, correo = registrar_usuario(username, email, password)
        if not token:
            flash("El usuario o correo ya existe")
            return redirect(url_for('registro'))

        msg = EmailMessage()
        msg['Subject'] = 'Confirma tu cuenta'
        msg['From'] = 'tucorreo@gmail.com'
        msg['To'] = correo
        link = url_for('confirmar', token=token, _external=True)
        msg.set_content(f"Hola {username}, confirma tu cuenta haciendo click aquí: {link}")

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('tucorreo@gmail.com', 'tu_password')
                smtp.send_message(msg)
            flash("Correo de confirmación enviado. Revisa tu bandeja.")
        except Exception as e:
            print("Error enviando correo:", e)
            flash("No se pudo enviar el correo. Contacta con el administrador.")

        return redirect(url_for('login'))

    return render_template('registro.html')

# -------- CONFIRMAR CORREO --------
@app.route('/confirmar/<token>')
def confirmar(token):
    activar_usuario(token)
    flash("Cuenta activada correctamente. Ahora puedes iniciar sesión")
    return redirect(url_for('login'))

# ============================================================
# 🔐 DASHBOARD SEPARADO POR ROLES
# ============================================================

@app.route('/dashboard/admin')
def dashboard_admin():
    if not session.get('usuario') or session.get('rol') != "admin":
        return redirect(url_for('login'))

    mensajes = obtener_mensajes()
    return render_template('dashboard_admin.html',
                           mensajes=mensajes,
                           rol=session.get('rol'),
                           usuario=session.get('usuario'))

@app.route('/dashboard/colaborador')
def dashboard_colaborador():
    if not session.get('usuario') or session.get('rol') != "colaborador":
        return redirect(url_for('login'))

    return render_template('dashboard_colaborador.html',
                           rol=session.get('rol'),
                           usuario=session.get('usuario'))

# -------- GUARDAR MENSAJE --------
@app.route('/enviar', methods=['POST'])
def enviar():
    nombre = request.form['nombre']
    email = request.form['email']
    mensaje = request.form['mensaje']

    guardar_mensaje(nombre, email, mensaje)
    flash("Mensaje enviado correctamente")
    return redirect(url_for('contacto'))

# -------- PUERTO PARA RENDER --------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
