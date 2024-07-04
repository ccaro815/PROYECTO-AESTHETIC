from flask import Flask, render_template, request, redirect, url_for
import Pag_Registro # Importar el archivo Pag_Registro

app = Flask(__name__)

# Simulación de una base de datos en memoria
usuarios = {}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        if usuario in usuarios and usuarios[usuario]['password'] == contrasena:
            return redirect(url_for('dashboard'))
        else:
            return "Usuario o contraseña incorrectos"
    return render_template('Pag_Login.html')

@app.route('/dashboard')
def dashboard():
    return "Bienvenido al Dashboard"

if __name__ == '__main__':
    app.run(debug=True)
