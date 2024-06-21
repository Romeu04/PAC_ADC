from flask import Flask, render_template
from database import db
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

@app.route('/membros.html')
def membros():
    return render_template('membros.html')

@app.route('/agenda.html')
def agenda():
    return render_template('agenda.html')

#teste

if __name__ == '__main__':
    from models import Produtos, Membros, Agendamentos
    with app.app_context():
        db.create_all()
    app.run(debug=True)