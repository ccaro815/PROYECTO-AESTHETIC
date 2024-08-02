from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

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
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        password = request.form['contrasena']
        hashed_password = generate_password_hash(password, method='sha256')

        new_user = User(nombre=nombre, apellido=apellido, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('Register.html')

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

@app.route('/gift_card')
def gift_card():
    return render_template('GiftCard.html')

@app.route('/novedades')
def novedades():
    return render_template('Novedades.html')

@app.route('/contact')
def contact():
    return render_template('Contactos.html')

if __name__ == '__main__':
    app.run(debug=True)









