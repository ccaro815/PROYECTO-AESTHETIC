from . import db

class VerificationToken(db.Model):
    __tablename__ = 'verification_token'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    expires_at = db.Column(db.DateTime, nullable=False)
    user = db.relationship('User', backref=db.backref('verification_tokens', lazy=True))
