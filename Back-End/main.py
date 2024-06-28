import io

from flask import Flask, render_template, request, jsonify, send_from_directory, send_file, redirect, session, url_for,flash
from database import db
from CRUD import *
import os

from models import Produtos, Membros, Agendamentos, Event

parent_dir = os.path.dirname(os.getcwd())
template_dir = os.path.join(parent_dir, 'Front-End')
static_dir = os.path.join(parent_dir, 'Front-End', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BD_Atletica.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'zanela'

db.init_app(app)

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account = Membros.query.filter_by(emailLogin=username, senhaLogin=password).first()
        if account:
            session['loggedin'] = True
            session['id'] = account.idMembros
            session['username'] = account.nomeMembro
            return redirect(url_for('agenda'))
        else:
            msg = 'Credenciais incorretas!'
    return render_template('login.html', msg=msg)



@app.route('/estoque.html')
@login_required
def estoque():
    return render_template('estoque.html')

@app.route('/membros.html')
@login_required
def membros():
    return render_template('membros.html')


@app.route('/agenda.html')
@login_required
def agenda():
    events = Event.query.all()
    return render_template('agenda.html', events=events)


@app.route('/add_event', methods=['POST'])
@login_required
def add_event():
    title = request.form['title']
    description = request.form['description']
    start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
    end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M')

    new_event = Event(title=title, description=description, start_time=start_time, end_time=end_time)
    db.session.add(new_event)
    db.session.commit()
    flash('Event added successfully!')
    return redirect(url_for('agenda'))


@app.route('/delete_event/<int:event_id>')
@login_required
def delete_event(event_id):
    event = Event.query.get(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!')
    return redirect(url_for('agenda'))


@app.route('/update_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    event = Event.form(event_id)
    if request.method == 'POST':
        event.title = request.form['title']
        event.description = request.form['description']
        event.start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
        event.end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M')

        db.session.commit()
        flash('Event updated successfully!')
        return redirect(url_for('agenda'))

@app.route('/get_all_products')

@login_required
def all_products():
    products = get_all_products()
    return jsonify([product.to_dict() for product in products])

@app.route('/get_all_members')
@login_required
def all_members():
    products = get_all_members()
    return jsonify([product.to_dict() for product in products])

@app.route('/update-stock', methods=['POST'])
@login_required
def update_stock():

    data = request.get_json()
    productId = data.get('productId')
    newQuantity = data.get('newQuantity')

    update_product_stock(productId, newQuantity)

    return 'Estoque atualizado com sucesso!', 200


@app.route('/add_product', methods=['POST'])
@login_required
def add_product():
    data = request.form
    nomeProduto = data.get('nomeProduto')
    estoqueProduto = data.get('estoqueProduto')
    precoProduto = data.get('precoProduto')
    foto = request.files.get('imagemProduto')

    add_product_with_image(nomeProduto, estoqueProduto, foto, precoProduto)

    return 'Produto adicionado com sucesso!', 200

@app.route('/delete-product/<int:productId>', methods=['DELETE'])
@login_required
def remove_product(productId):
    delete_product(productId)
    return 'Produto removido com sucesso!', 200

@app.route('/imagem_produto/<int:productId>')
@login_required
def images(productId):
    product = Produtos.query.get(productId)
    if product and product.foto:
        return send_file(io.BytesIO(product.foto), mimetype='image/jpeg')
    else:
        return "No image found for product", 404


@app.route('/imagem_membro/<int:memberId>')
@login_required
def member_images(memberId):
    member = Membros.query.get(memberId)
    if member and member.fotoMembro:
        return send_file(io.BytesIO(member.fotoMembro), mimetype='image/jpeg')
    else:
        return "No image found for member", 404

@app.route('/add_member', methods=['POST'])
@login_required
def add_member_new():
    data = request.form
    nomeMembro = data.get('memberName')
    sobrenomeMembro = data.get('memberLastName')
    dataNascimento = data.get('memberDob')
    fotoMembro = request.files.get('memberImage')
    emailLogin = data.get('memberLogin')
    validadar =validade_email(emailLogin)
    senhaLogin = data.get('memberPassword')
    print('----')
    print(validadar)
    print('---')
    if(validadar):
        add_member(nomeMembro, sobrenomeMembro, dataNascimento, fotoMembro, emailLogin, senhaLogin)
        return 'Membro adicionado com sucesso!', 200

    return 'Membro ja existe', 200


@app.route('/get_member/<int:memberId>')
@login_required
def get_member_new(memberId):
    member = get_member(memberId)
    return jsonify(member.to_dict())

@app.route('/update_member', methods=['PUT'])
@login_required
def update_member_new():
    data = request.form

    memberId = data.get('idMember')
    nomeMembro = data.get('memberName')
    sobrenomeMembro = data.get('memberLastName')
    dataNascimento = data.get('memberDob')
    fotoMembro = request.files.get('memberImage')
    emailLogin = data.get('memberLogin')
    senhaLogin = data.get('memberPassword')

    update_member(memberId, nomeMembro, sobrenomeMembro, dataNascimento, fotoMembro, emailLogin, senhaLogin)

    return 'Membro atualizado com sucesso!', 200

@app.route('/delete_member/<int:memberId>', methods=['DELETE'])
def remove_member(memberId):
    delete_member(memberId)
    return 'Membro removido com sucesso!', 200

if __name__ == '__main__':
    from models import Produtos, Membros, Agendamentos
    with app.app_context():
        db.create_all()
    app.run(debug=True)
