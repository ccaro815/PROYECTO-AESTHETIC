from datetime import datetime
from . import db

class Calificacion(db.Model):
    __tablename__ = 'calificacion'
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Integer, nullable=False)
    # comentario = db.Column(db.Text, nullable=True)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicio.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    servicio = db.relationship('Servicio', backref=db.backref('calificaciones', lazy=True))
    user = db.relationship('User', backref=db.backref('calificaciones', lazy=True))
