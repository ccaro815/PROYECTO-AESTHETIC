from flask import Flask, g, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import random
import os
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta
from models.calificacion import Calificacion

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Aestethic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'aestheticestetica22@gmail.com'
app.config['MAIL_PASSWORD'] = 'hnwm mlzy lcah sgko'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    apellido = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    permissions = db.Column(db.String(200), nullable=True)

class VerificationToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    expires_at = db.Column(db.DateTime, nullable=False)
    user = db.relationship('User', backref=db.backref('verification_tokens', lazy=True))
    
class Servicio(db.Model):
    __tablename__ = 'servicio'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    categoria = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String, nullable=True)
    precio = db.Column(db.Float, nullable=False)

@app.route('/calificar_servicio/<int:servicio_id>', methods=['POST'])
def calificar_servicio(servicio_id):
    data = request.get_json()
    calificacion = data.get('calificacion')

    if calificacion:
        nueva_calificacion = Calificacion(
            servicio_id=servicio_id,
            usuario_id=session['user_id'],
            calificacion=calificacion
        )
        db.session.add(nueva_calificacion)
        db.session.commit()
        return jsonify(success=True), 200
    else:
        return jsonify(success=False, message="Calificación no proporcionada"), 400


@app.before_request
def add_user_to_template():
    g.user_name = session.get('user_name', None)
    g.user_apellido = session.get('user_apellido', None)
    g.user_email = session.get('user_email', None)
    g.avatar_color = session.get('avatar_color', None)

def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_USERNAME']
    )
    mail.send(msg)

def generate_confirmation_token(email):
    return ts.dumps(email, salt='email-confirm-key')

def confirm_token(token, expiration=3600):
    try:
        email = ts.loads(token, salt='email-confirm-key', max_age=expiration)
    except:
        return False
    return email

@app.route('/')
def home():
    user_name = session.get('user_name', None)
    user_apellido = session.get('user_apellido', None)
    user_email = session.get('user_email', None)
    avatar_color = session.get('avatar_color', None)
    return render_template('Pag_Principal_AESTETIC.html', user_name=user_name, user_apellido=user_apellido, user_email=user_email, avatar_color=avatar_color)

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
            session['user_email'] = user.email
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
    session.pop('user_email', None)
    session.pop('avatar_color', None)
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            nombre = data.get('nombre')
            apellido = data.get('apellido')
            email = data.get('email')
            password = data.get('contrasena')

            # Verificar si el email ya está registrado
            if User.query.filter_by(email=email).first():
                return jsonify(success=False, message='El correo ya está registrado.')

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(nombre=nombre, apellido=apellido, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            # Generar y almacenar el token de verificación
            token = generate_confirmation_token(new_user.email)
            expires_at = datetime.utcnow() + timedelta(hours=48)
            verification_token = VerificationToken(token=token, user_id=new_user.id, expires_at=expires_at)
            db.session.add(verification_token)
            db.session.commit()

            # Enviar el correo de confirmación
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Por favor confirma tu correo"
            send_email(new_user.email, subject, html)

            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Tipo de contenido no soportado"), 415
    return render_template('Registro.html')

@app.route('/register_success')
def register_success():
    return render_template('register_success.html')

@app.route('/confirm_email/<token>')
def confirm_email(token):
    verification_token = VerificationToken.query.filter_by(token=token).first_or_404()

    if verification_token.expires_at < datetime.utcnow():
        flash('El enlace de confirmación ha expirado.', 'danger')
        return redirect(url_for('home'))

    user = verification_token.user
    db.session.delete(verification_token)
    db.session.commit()

    flash('Has confirmado tu correo electrónico. Gracias! Ahora puedes iniciar sesión.', 'success')
    return redirect(url_for('login'))

@app.route('/manage_roles', methods=['GET', 'POST'])
def manage_roles():
    if 'user_email' not in session or session['user_email'] != 'cristianezequiel915@gmail.com':
        flash('No tienes permiso para acceder a esta página', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        role_name = request.form['role_name']
        permissions = request.form.get('permissions', '')
        new_role = Role(name=role_name, permissions=permissions)
        db.session.add(new_role)
        db.session.commit()
        flash('Rol agregado exitosamente', 'success')
    
    roles = Role.query.all()
    return render_template('manage_roles.html', roles=roles)

@app.route('/assign_role', methods=['GET', 'POST'])
def assign_role():
    if 'user_email' not in session or session['user_email'] != 'cristianezequiel915@gmail.com':
        flash('No tienes permiso para acceder a esta página', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        user_email = request.form['user_email']
        role_id = request.form['role_id']
        user = User.query.filter_by(email=user_email).first()
        role = Role.query.get(role_id)
        
        if user and role:
            user.roles.append(role)
            db.session.commit()
            flash('Rol asignado exitosamente', 'success')
        else:
            flash('Usuario o rol no encontrado', 'danger')
    
    users = User.query.all()
    roles = Role.query.all()
    return render_template('assign_role.html', users=users, roles=roles)

def user_has_permission(user, permission):
    for role in user.roles:
        if permission in role.permissions.split(','):
            return True
    return False

@app.route('/restricted_page')
def restricted_page():
    user = User.query.get(session['user_id'])
    if not user_has_permission(user, 'access_restricted_page'):
        flash('No tienes permiso para acceder a esta página', 'danger')
        return redirect(url_for('home'))
    return render_template('restricted_page.html')

@app.route('/buscar_servicios', methods=['GET'])
def buscar_servicios():
    query = request.args.get('query', '').lower()
    servicios = [
        {'nombre': 'Tratamientos Faciales', 'ruta': url_for('tratamiento_facial')},
        {'nombre': 'Depilación', 'ruta': url_for('tratamiento_depilacion')},
        {'nombre': 'Masajes', 'ruta': url_for('tratamiento_masajes')},
        {'nombre': 'Spa de Manos', 'ruta': url_for('tratamiento_spa_de_manos')},
        {'nombre': 'Tratamientos Corporales', 'ruta': url_for('tratamientos_corporales')}
    ]
    resultados = [s for s in servicios if query in s['nombre'].lower()]
    
    return jsonify(resultados)

@app.route('/servicios')
def servicios():
    return render_template('Servicios.html')

@app.route('/tratamientos_corporales')
def tratamientos_corporales():
    return render_template('service/Pag_Tratamiento Corporales.html')

@app.route('/tratamientos_facial')
def tratamiento_facial():
    return render_template('service/Pag_TratamientoFacial.html')

@app.route('/tratamientos_depilacion')
def tratamiento_depilacion():
    return render_template('service/Pag_Depilacion.html')

@app.route('/tratamientos_spa_de_manos')
def tratamiento_spa_de_manos():
    return render_template('service/Pag_SpaDeManos.html')

@app.route('/tratamientos_masajes')
def tratamiento_masajes():
    return render_template('service/Pag_Masajes.html')

@app.route('/novedades')
def novedades():
    return render_template('Novedades.html')

@app.route('/gif_card')
def gif_card():
    return render_template('Gif_Card.html')

@app.route('/contactos')
def contactos():
    return render_template('Contactos.html')

@app.route('/calendario')
def calendario():
    return render_template('Calendario.html')

@app.route('/carrito')
def carrito():
    user_name = session.get('user_name', None)
    user_apellido = session.get('user_apellido', None)
    user_email = session.get('user_email', None)
    avatar_color = session.get('avatar_color', None)
    return render_template('Carrito.html', user_name=user_name, user_apellido=user_apellido, user_email=user_email, avatar_color=avatar_color)

@app.route('/create_service_category', methods=['GET', 'POST'])
def create_service_category():
    return render_template('create_service_category.html')

@app.route('/manage_service_category')
def manage_service_category():
    return render_template('manage_service_category.html')

if __name__ == '__main__':
    app.run(debug=True)














