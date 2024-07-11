from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.password == password:
            return redirect(url_for('dashboard'))
        else:
            return "Usuario o contraseña incorrectos"
    return render_template('Pag_Login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        dni = request.form['dni']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        if password != confirm_password:
            return "Las contraseñas no coinciden"
        if Usuario.query.filter_by(email=email).first():
            return "El usuario ya existe"
        nuevo_usuario = Usuario(nombre=nombre, dni=dni, email=email, password=password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('Pag_Registro.html')

@app.route('/dashboard')
def dashboard():
    return "Bienvenido al Dashboard"

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

