import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import crear_db, guardar_mensaje, obtener_mensajes, validar_usuario

# crear base de datos automáticamente
crear_db()

app = Flask(__name__)
app.secret_key = "sofnet_secret_key"


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
            session['usuario'] = usuario[1]
            session['rol'] = usuario[3]
            return redirect(url_for('admin'))
        else:
            flash("Credenciales incorrectas")

    return render_template('login.html')


# -------- CERRAR SESIÓN --------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio'))


# -------- PANEL ADMIN / COLABORADOR --------
@app.route('/admin')
def admin():
    if not session.get('usuario'):
        return redirect(url_for('login'))

    mensajes = obtener_mensajes()
    return render_template('admin.html',
                           mensajes=mensajes,
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
    app.run(host="0.0.0.0", port=port)
