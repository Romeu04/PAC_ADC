from flask import Flask
from main import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/mydb'

class Produtos(db.Model):
    __tablename__ = 'Produtos'
    idProduto = db.Column(db.Integer, primary_key=True)
    nomeProduto = db.Column(db.String(45), nullable=False)
    estoqueProduto = db.Column(db.Integer, nullable=False)
    foto = db.Column(db.LargeBinary, nullable=True)
    precoProduto = db.Column(db.Float, nullable=False)

class NiveisUsuarios(db.Model):
    __tablename__ = 'NiveisUsuarios'
    idNiveisUsuarios = db.Column(db.Integer, primary_key=True)
    nomeNivel = db.Column(db.String(45), nullable=False)

class Membros(db.Model):
    __tablename__ = 'Membros'
    idMembros = db.Column(db.Integer, primary_key=True)
    nomeMembro = db.Column(db.String(45), nullable=False)
    sobrenomeMembro = db.Column(db.String(45), nullable=False)
    dataNascimento = db.Column(db.Date, nullable=False)
    fotoMembro = db.Column(db.LargeBinary)
    nomeLogin = db.Column(db.String(45), nullable=False, unique=True)
    senhaLogin = db.Column(db.String(45), nullable=False, unique=True)
    NiveisUsuarios_idNiveisUsuarios = db.Column(db.Integer, db.ForeignKey('NiveisUsuarios.idNiveisUsuarios'), nullable=False)

class Agendamentos(db.Model):
    __tablename__ = 'Agendamentos'
    idAgendamentos = db.Column(db.Integer, primary_key=True)
    diaAgendamento = db.Column(db.Date, nullable=False)
    dataInicio = db.Column(db.Date, nullable=False)
    dataTermino = db.Column(db.Date, nullable=False)
    descricaoAgendamento = db.Column(db.String(255), nullable=False)
    Membros_idMembros = db.Column(db.Integer, db.ForeignKey('Membros.idMembros'), nullable=False)

class logProdutos(db.Model):
    __tablename__ = 'logProdutos'
    idlogProdutos = db.Column(db.Integer, primary_key=True)
    dataAlteracao = db.Column(db.Date, nullable=False)
    Produtos_codProduto = db.Column(db.Integer, db.ForeignKey('Produtos.idProduto'), nullable=False)
    Membros_idMembros = db.Column(db.Integer, db.ForeignKey('Membros.idMembros'), nullable=False)
