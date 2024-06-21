from flask import Flask, render_template
import os

parent_dir = os.path.dirname(os.getcwd())
template_dir = os.path.join(parent_dir, 'Front-End')
static_dir = os.path.join(parent_dir, 'Front-End', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

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

if __name__ == '__main__':
    app.run(debug=True)