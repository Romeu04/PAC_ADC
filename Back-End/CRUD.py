from models import db, Produtos, Membros, Agendamentos
import requests
def add_product_with_image(idProduto, nomeProduto, estoqueProduto, image_path, precoProduto):
    with open(image_path, 'rb') as f:
        photo = f.read()
    new_product = Produtos(idProduto=idProduto, nomeProduto=nomeProduto, estoqueProduto=estoqueProduto, foto=photo, precoProduto=precoProduto)
    db.session.add(new_product)
    db.session.commit()

def get_product(idProduto):
    product = Produtos.query.get(idProduto)
    return product

def update_product(idProduto, nomeProduto, estoqueProduto, foto, precoProduto):
    product = Produtos.query.get(idProduto)
    if product:
        product.nomeProduto = nomeProduto
        product.estoqueProduto = estoqueProduto
        product.foto = foto
        product.precoProduto = precoProduto
        db.session.commit()

def delete_product(idProduto):
    product = Produtos.query.get(idProduto)
    if product:
        db.session.delete(product)
        db.session.commit()

def add_member(nomeMembro, sobrenomeMembro, dataNascimento, fotoMembro, nomeLogin, senhaLogin, NiveisUsuarios_idNiveisUsuarios):
    new_member = Membros(nomeMembro=nomeMembro, sobrenomeMembro=sobrenomeMembro, dataNascimento=dataNascimento, fotoMembro=fotoMembro, nomeLogin=nomeLogin, senhaLogin=senhaLogin, NiveisUsuarios_idNiveisUsuarios=NiveisUsuarios_idNiveisUsuarios)
    db.session.add(new_member)
    db.session.commit()

def get_member(idMembros):
    member = Membros.query.get(idMembros)
    return member

def update_member(idMembros, nomeMembro, sobrenomeMembro, dataNascimento, fotoMembro, nomeLogin, senhaLogin, NiveisUsuarios_idNiveisUsuarios):
    member = Membros.query.get(idMembros)
    if member:
        member.nomeMembro = nomeMembro
        member.sobrenomeMembro = sobrenomeMembro
        member.dataNascimento = dataNascimento
        member.fotoMembro = fotoMembro
        member.nomeLogin = nomeLogin
        member.senhaLogin = senhaLogin
        member.NiveisUsuarios_idNiveisUsuarios = NiveisUsuarios_idNiveisUsuarios
        db.session.commit()

def delete_member(idMembros):
    member = Membros.query.get(idMembros)
    if member:
        db.session.delete(member)
        db.session.commit()

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
