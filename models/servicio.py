from . import db

class Servicio(db.Model):
    __tablename__ = 'servicio'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    categoria = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String)
    precio = db.Column(db.Float, nullable=False)
