from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.your-email-provider.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'

db = SQLAlchemy(app)
mail = Mail(app)

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
        
        # Verificar si el correo electrónico ya está registrado
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Este correo electrónico ya está registrado. Por favor, utiliza otro correo o inicia sesión.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(contrasena, method='pbkdf2:sha256')
        new_user = User(nombre=nombre, apellido=apellido, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()

            # Enviar correo de confirmación
            msg = Message('Confirmación de Registro', recipients=[email])
            msg.body = f"Hola {nombre} {apellido},\n\nGracias por registrarte en nuestra plataforma. Por favor, confirma tu correo electrónico. Puedes iniciar sesión usando el siguiente enlace: {url_for('login', _external=True)}\n\nTu correo registrado es: {email}\n\nSaludos,\nEquipo de Soporte"
            mail.send(msg)

            flash('Cuenta creada con éxito. Verifica tu correo para continuar.', 'success')
            return redirect(url_for('registro_exitoso'))
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

@app.route('/registro_exitoso')
def registro_exitoso():
    return render_template('registro_exitoso.html')

@app.route('/resend_confirmation')
def resend_confirmation():
    user_id = session.get('user_id')
    if not user_id:
        flash('Debes iniciar sesión para reenviar el correo de confirmación', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(user_id)
    if user:
        msg = Message('Reenvío de Confirmación de Registro', recipients=[user.email])
        msg.body = f"Hola {user.nombre} {user.apellido},\n\nEste es un reenvío de la confirmación de tu registro. Puedes iniciar sesión usando el siguiente enlace: {url_for('login', _external=True)}\n\nTu correo registrado es: {user.email}\n\nSaludos,\nEquipo de Soporte"
        mail.send(msg)
        flash('Correo de confirmación reenviado.', 'success')
    else:
        flash('Usuario no encontrado.', 'danger')
    
    return redirect(url_for('home'))

@app.route('/servicios')
def servicios():
    return render_template('Servicios.html')

if __name__ == '__main__':
    app.run(debug=True)






