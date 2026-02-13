from flask import Flask, render_template, request
from flask import request, redirect, url_for


app = Flask(__name__)

# -------- INICIO --------
@app.route('/')
def inicio():
    return render_template('index.html')

# -------- SERVICIOS --------
@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

# -------- CONTACTO --------
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        mensaje = request.form['mensaje']

        print("Nombre:", nombre)
        print("Email:", email)
        print("Mensaje:", mensaje)

    return render_template('contacto.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    nombre = request.form['nombre']
    email = request.form['email']
    mensaje = request.form['mensaje']

    with open('mensajes.txt', 'a', encoding='utf-8') as archivo:
        archivo.write(f"Nombre: {nombre}\n")
        archivo.write(f"Email: {email}\n")
        archivo.write(f"Mensaje: {mensaje}\n")
        archivo.write("-" * 30 + "\n")

    return redirect(url_for('contacto'))



# -------- EJECUCIÓN --------
if __name__ == "__main__":
    app.run()
