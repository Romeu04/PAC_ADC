import os
from datetime import datetime

from werkzeug.utils import secure_filename
from models import db, Produtos, Membros, Agendamentos,Event
import requests
def add_product_with_image(nomeProduto, estoqueProduto, imagemProduto, precoProduto):

    if imagemProduto:
        photo = imagemProduto.read()
    else:
        photo = None

    new_product = Produtos(nomeProduto=nomeProduto, estoqueProduto=estoqueProduto, foto=photo, precoProduto=precoProduto)
    db.session.add(new_product)
    db.session.commit()

def add_product(nomeProduto, estoqueProduto, precoProduto):
    new_product = Produtos(nomeProduto=nomeProduto, estoqueProduto=estoqueProduto, precoProduto=precoProduto)
    db.session.add(new_product)
    db.session.commit()


def get_product(idProduto):
    product = Produtos.query.get(idProduto)
    return product

def get_all_products():
    products = Produtos.query.all()
    return products

def update_product(idProduto, nomeProduto, estoqueProduto, foto, precoProduto):
    product = Produtos.query.get(idProduto)
    if product:
        product.nomeProduto = nomeProduto
        product.estoqueProduto = estoqueProduto
        product.foto = foto
        product.precoProduto = precoProduto
        db.session.commit()

def update_product_stock(productId, newQuantity):
    product = Produtos.query.get(productId)
    if product:
        product.estoqueProduto = newQuantity
        db.session.commit()

def delete_product(idProduto):
    product = Produtos.query.get(idProduto)
    if product:
        db.session.delete(product)
        db.session.commit()

def validade_email(email):
    return len(Membros.query.filter_by(emailLogin=email).all()) == 0


def add_member(nomeMembro, sobrenomeMembro, dataNascimento, fotoMembro, emailLogin, senhaLogin):

    if fotoMembro:
        photo = fotoMembro.read()
    else:
        photo = None

    dataNascimento = datetime.strptime(dataNascimento, '%Y-%m-%d')

    new_member = Membros(nomeMembro=nomeMembro, sobrenomeMembro=sobrenomeMembro, dataNascimento=dataNascimento, fotoMembro=photo, emailLogin=emailLogin, senhaLogin=senhaLogin)
    db.session.add(new_member)
    db.session.commit()

def get_member(idMembros):
    member = Membros.query.get(idMembros)
    return member

def update_member_old(storedMember, updatedMember):
    for key, value in updatedMember.__dict__.items():
        if value is not None and key != '_sa_instance_state':
            setattr(storedMember, key, value)
    db.session.merge(storedMember)
    db.session.commit()

def update_member(idMembros, nomeMembro, sobrenomeMembro, dataNascimento, fotoMembro, emailLogin, senhaLogin):
    member = Membros.query.get(idMembros)

    if fotoMembro:
        photo = fotoMembro.read()
    else:
        photo = None

    dataNascimentos = datetime.strptime(dataNascimento, '%Y-%m-%d')

    if member:
        member.nomeMembro = nomeMembro
        member.sobrenomeMembro = sobrenomeMembro
        member.dataNascimento = dataNascimentos
        if photo is not None:
            member.fotoMembro = photo
        member.emailLogin = emailLogin
        member.senhaLogin = senhaLogin
        db.session.commit()

def delete_member(idMembros):
    member = Membros.query.get(idMembros)
    if member:
        db.session.delete(member)
        db.session.commit()

def get_all_members():
    members = Membros.query.all()
    return members

def add_appointment(diaAgendamento, dataInicio, dataTermino, descricaoAgendamento, Membros_idMembros):
    new_appointment = Agendamentos(diaAgendamento=diaAgendamento, dataInicio=dataInicio, dataTermino=dataTermino, descricaoAgendamento=descricaoAgendamento, Membros_idMembros=Membros_idMembros)
    db.session.add(new_appointment)
    db.session.commit()

def get_appointment(idAgendamentos):
    appointment = Agendamentos.query.get(idAgendamentos)
    return appointment

def update_appointment(idAgendamentos, diaAgendamento, dataInicio, dataTermino, descricaoAgendamento, Membros_idMembros):
    appointment = Agendamentos.query.get(idAgendamentos)
    if appointment:
        appointment.diaAgendamento = diaAgendamento
        appointment.dataInicio = dataInicio
        appointment.dataTermino = dataTermino
        appointment.descricaoAgendamento = descricaoAgendamento
        appointment.Membros_idMembros = Membros_idMembros
        db.session.commit()

def delete_appointment(idAgendamentos):
    appointment = Agendamentos.query.get(idAgendamentos)
    if appointment:
        db.session.delete(appointment)
        db.session.commit()

