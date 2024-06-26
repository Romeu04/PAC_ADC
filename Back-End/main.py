import io

from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from database import db
from CRUD import *
import os

parent_dir = os.path.dirname(os.getcwd())
template_dir = os.path.join(parent_dir, 'Front-End')
static_dir = os.path.join(parent_dir, 'Front-End', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BD_Atletica.db'
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

@app.route('/update-stock', methods=['POST'])
def update_stock():
    data = request.get_json()
    productId = data.get('productId')
    newQuantity = data.get('newQuantity')

    update_product_stock(productId, newQuantity)

    return 'Estoque atualizado com sucesso!', 200

@app.route('/add_product', methods=['POST'])
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

@app.route('/images/<int:productId>')
def images(productId):
    product = Produtos.query.get(productId)
    if product and product.foto:
        return send_file(io.BytesIO(product.foto), mimetype='image/jpeg')
    else:
        return "No image found for product", 404

if __name__ == '__main__':
    from models import Produtos, Membros, Agendamentos
    with app.app_context():
        db.create_all()
    app.run(debug=True)