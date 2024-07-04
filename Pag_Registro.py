from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulación de una base de datos en memoria
usuarios = {}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        dni = request.form['dni']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        
        # Verificar si las contraseñas coinciden
        if password != confirm_password:
            return "Las contraseñas no coinciden"
        
        # Verificar si el usuario ya existe
        if email in usuarios:
            return "El usuario ya existe"
        
        # Guardar el usuario en la 'base de datos'
        usuarios[email] = {'nombre': nombre, 'dni': dni, 'password': password}
        
        return redirect(url_for('login'))
    
    return render_template('Pag_Registro.html')

if __name__ == '__main__':
    app.run(debug=True)
