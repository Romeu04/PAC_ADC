from flask import Flask, render_template, request, jsonify
from database import db
from CRUD import *
import os

parent_dir = os.path.dirname(os.getcwd())
template_dir = os.path.join(parent_dir, 'Front-End')
static_dir = os.path.join(parent_dir, 'Front-End', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/estoque.html')
def estoque():
    return render_template('estoque.html')

@app.route('/get_all_products')
def all_products():
    products = get_all_products()
    return jsonify([product.to_dict() for product in products])

@app.route('/membros.html')
def membros():
    return render_template('membros.html')

@app.route('/agenda.html')
def agenda():
    return render_template('agenda.html')


@app.route('/add_product/<int:product_id>', methods=['POST', 'GET'])
def add_product_velho(product_id):
    product = get_product(product_id)
    print(product)
    if product:
        product.estoqueProduto += 1
        db.session.commit()
        return 'Produto adicionado com sucesso!', 200
    else:
        return 'Produto não encontrado!', 404

@app.route('/update-stock', methods=['POST'])
def update_stock():
    data = request.get_json()
    productId = data.get('productId')
    newQuantity = data.get('newQuantity')

    update_product_stock(productId, newQuantity)

    return 'Estoque atualizado com sucesso!', 200

@app.route('/add_product', methods=['POST'])
def add_product_form():
    print(request.form)
    nomeProduto = request.form['nomeProduto']
    estoqueProduto = request.form['estoqueProduto']
    precoProduto = request.form['precoProduto']
    add_product(nomeProduto, estoqueProduto, precoProduto)
    return 'Produto adicionado com sucesso!', 200

@app.route('/remove_product/<int:productId>', methods=['DELETE'])
def remove_product(productId):
    delete_product(productId)
    return 'Produto removido com sucesso!', 200

if __name__ == '__main__':
    from models import Produtos, Membros, Agendamentos
    with app.app_context():
        db.create_all()
    app.run(debug=True)