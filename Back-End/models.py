import base64

from flask import Flask
from database import db

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/mydb'

class Produtos(db.Model):
    __tablename__ = 'Produtos'
    idProduto = db.Column(db.Integer, primary_key=True)
    nomeProduto = db.Column(db.String(45), nullable=False)
    estoqueProduto = db.Column(db.Integer, nullable=False)
    foto = db.Column(db.LargeBinary, nullable=True)
    precoProduto = db.Column(db.Float, nullable=False)

    def to_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if self.foto is not None:
            data['foto'] = base64.b64encode(self.foto).decode('utf-8')
        return data

class Membros(db.Model):
    __tablename__ = 'Membros'
    idMembros = db.Column(db.Integer, primary_key=True)
    nomeMembro = db.Column(db.String(45), nullable=False)
    sobrenomeMembro = db.Column(db.String(45), nullable=False)
    dataNascimento = db.Column(db.Date, nullable=False)
    fotoMembro = db.Column(db.LargeBinary)
    emailLogin = db.Column(db.String(45), nullable=False, unique=True)
    senhaLogin = db.Column(db.String(45), nullable=False)

    def to_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if self.fotoMembro is not None:
            data['fotoMembro'] = base64.b64encode(self.fotoMembro).decode('utf-8')
        return data

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Event {self.title}>'