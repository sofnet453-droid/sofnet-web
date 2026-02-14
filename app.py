import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from database import crear_db

# crea la base de datos automáticamente al iniciar
crear_db()

app = Flask(__name__)

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

    # conexión a base de datos
    conexion = sqlite3.connect("sofnet.db")
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO mensajes (nombre, correo, mensaje)
        VALUES (?, ?, ?)
    """, (nombre, email, mensaje))

    conexion.commit()
    conexion.close()

    return redirect(url_for('contacto'))


# -------- PUERTO PARA RENDER --------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
