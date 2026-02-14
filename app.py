import os
from flask import Flask, render_template, request, redirect, url_for, flash
from database import crear_db, guardar_mensaje

# crea la base de datos automáticamente al iniciar
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

# -------- GUARDAR MENSAJE --------
@app.route('/enviar', methods=['POST'])
def enviar():
    nombre = request.form['nombre']
    email = request.form['email']
    mensaje = request.form['mensaje']

    # usamos la función del database.py
    guardar_mensaje(nombre, email, mensaje)

    flash("Mensaje enviado correctamente")

    return redirect(url_for('contacto'))

# -------- PUERTO PARA RENDER --------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
