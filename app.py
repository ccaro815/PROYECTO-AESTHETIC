from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    apellido = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

@app.route('/')
def home():
    user_name = session.get('user_name', None)
    user_apellido = session.get('user_apellido', None)
    avatar_color = session.get('avatar_color', None)
    return render_template('Pag_Principal_AESTETIC.html', user_name=user_name, user_apellido=user_apellido, avatar_color=avatar_color)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        contrasena = request.form['contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']

        if contrasena != confirmar_contrasena:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(contrasena, method='pbkdf2:sha256')
        new_user = User(nombre=nombre, apellido=apellido, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Cuenta creada con éxito', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la cuenta: {str(e)}', 'danger')
            return redirect(url_for('register'))
    
    return render_template('Registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['usuario']
        password = request.form['contrasena']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.nombre
            session['user_apellido'] = user.apellido
            session['avatar_color'] = generate_random_color()
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('home'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')

    return render_template('Login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_apellido', None)
    session.pop('avatar_color', None)
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('home'))

@app.route('/servicios')
def servicios():
    return render_template('Servicios.html')

if __name__ == '__main__':
    app.run(debug=True)






