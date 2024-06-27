import io

from flask import Flask, render_template, request, jsonify, send_from_directory, send_file, redirect, session, url_for

from database import db
from CRUD import *
import os

parent_dir = os.path.dirname(os.getcwd())
template_dir = os.path.join(parent_dir, 'Front-End')
static_dir = os.path.join(parent_dir, 'Front-End', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BD_Atletica.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super_secret_key'

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
    return render_template('agenda.html')

@app.route('/get_all_products')
@login_required
def all_products():
    products = get_all_products()
    return jsonify([product.to_dict() for product in products])

@app.route('/get_all_members')
@login_required
def all_members():
    products = get_all_members()
    print(products)
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
def remove_product(productId):
    delete_product(productId)
    return 'Produto removido com sucesso!', 200

@app.route('/imagem_produto/<int:productId>')
def images(productId):
    product = Produtos.query.get(productId)
    if product and product.foto:
        return send_file(io.BytesIO(product.foto), mimetype='image/jpeg')
    else:
        return "No image found for product", 404


@app.route('/imagem_membro/<int:memberId>')
def member_images(memberId):
    member = Membros.query.get(memberId)
    if member and member.fotoMembro:
        return send_file(io.BytesIO(member.fotoMembro), mimetype='image/jpeg')
    else:
        return "No image found for member", 404

@app.route('/add_member', methods=['POST'])
def add_member_new():
    data = request.form
    nomeMembro = data.get('memberName')
    sobrenomeMembro = data.get('memberLastName')
    dataNascimento = data.get('memberDob')
    fotoMembro = request.files.get('memberImage')
    emailLogin = data.get('memberLogin')
    senhaLogin = data.get('memberPassword')

    add_member(nomeMembro, sobrenomeMembro, dataNascimento, fotoMembro, emailLogin, senhaLogin)

    return 'Membro adicionado com sucesso!', 200

@app.route('/get_member/<int:memberId>')
def get_member_new(memberId):
    member = get_member(memberId)
    return jsonify(member.to_dict())

@app.route('/update_member', methods=['POST'])
def update_member_new():
    data = request.form
    memberId = data.get('memberId')
    nomeMembro = data.get('memberName')
    sobrenomeMembro = data.get('memberLastName')
    dataNascimento = data.get('memberDob')
    fotoMembro = request.files.get('memberImage')
    emailLogin = data.get('memberLogin')
    senhaLogin = data.get('memberPassword')

    update_member(memberId, nomeMembro, sobrenomeMembro, dataNascimento, fotoMembro, emailLogin, senhaLogin)

    return 'Membro atualizado com sucesso!', 200

if __name__ == '__main__':
    from models import Produtos, Membros, Agendamentos
    with app.app_context():
        db.create_all()
    app.run(debug=True)
