from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import relationship


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)

    phone_number = db.Column(db.String(15), unique=True, nullable=True)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_users = db.relationship('User', backref=db.backref(
        'creator', remote_side=[id]), lazy=True)

    labcenter_id = db.Column(db.Integer, db.ForeignKey('labcenter.id'))
    labcenter = db.relationship('LabCenter', back_populates='users')

    forms = db.relationship('PlantDiagnosticForm',
                            backref='form_user', lazy=True)

    is_active = db.Column(db.Boolean, default=True)

    @property
    def password(self):
        raise AttributeError(
            'Password attribute should not be accessed directly.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(
            password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'), nullable=False)
    host = db.relationship('Host', backref=db.backref('messages', lazy=True))
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    message_type = db.Column(db.String(10), nullable=False)  # 'Email' or 'SMS'
    signature = db.Column(db.Text, nullable=False)

    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender = db.relationship(
        'User', backref=db.backref('sent_messages', lazy=True))

    def __init__(self, username, email, phone_number, host, message_type, signature, sender):
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.host = host
        self.message_type = message_type
        self.signature = signature
        self.sender = sender


class Signature(db.Model):
    __tablename__ = 'signature'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recommended_text = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'), nullable=False)
    host = db.relationship('Host', backref=db.backref('signatures', lazy=True))

    def __init__(self, recommended_text, host, status):
        self.recommended_text = recommended_text
        self.host = host
        self.status = status
