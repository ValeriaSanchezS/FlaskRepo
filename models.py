from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Departamento(db.Model):
    __tablename__ = 'Departamentos'
    ID = db.Column(db.Integer, primary_key=True)
    Departamento = db.Column(db.String(100))
    Contraseña = db.Column(db.String(50))
    VistaEspecial = db.Column(db.Boolean)

class RegistroUsuario(db.Model, UserMixin):
    __tablename__ = 'RegistroUsuarios'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(50))
    Apellidos = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    DepartamentoID = db.Column(db.Integer, db.ForeignKey('Departamentos.ID'), unique=True, nullable=False)
    Contraseña = db.Column(db.String(50))

    departamento = db.relationship('Departamento', backref=db.backref('usuarios', lazy=True))

    def verify_password(self, password):
        return check_password_hash(self.Contraseña, password)
