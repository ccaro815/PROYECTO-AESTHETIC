from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_BINDS'] = {
    'tokens': 'sqlite:///tokens.db'
}

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    apellido = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

class Token(db.Model):
    __bind_key__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    token = db.Column(db.String(256), nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)


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
            
            token = s.dumps(email, salt='email-confirm')
            validation_token = Token(user_id=new_user.id, token=token)
            db.session.add(validation_token)
            db.session.commit()

            msg = Message('Confirma tu correo electrónico', sender='tu_email@example.com', recipients=[email])
            link = url_for('confirm_email', token=token, _external=True)
            msg.body = f'Haz clic en el siguiente enlace para confirmar tu cuenta: {link}'
            mail.send(msg)

            # Mostrar mensaje de éxito
            return render_template('Registro.html', success=True)
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la cuenta: {str(e)}', 'danger')
            return redirect(url_for('register'))

    return render_template('Registro.html')

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=172800)  # 48 horas de validez
    except SignatureExpired:
        flash('El enlace de confirmación ha expirado. Por favor, regístrate de nuevo.', 'danger')
        return redirect(url_for('register'))

    user = User.query.filter_by(email=email).first_or_404()

    if user.confirmed:
        flash('Tu cuenta ya ha sido confirmada.', 'success')
    else:
        user.confirmed = True
        db.session.commit()
        flash('Tu cuenta ha sido confirmada. Ya puedes iniciar sesión.', 'success')

    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)







