from flask import *
from flask import blueprints
from DAO.UsuarioDAO import UsuarioDAO
from usuarios import usuarios
from professor import professor
from aluno import aluno
from admin import admin
from flask_bcrypt import Bcrypt
from helper.config import *
from Model.Resposta import Resposta
import os
from sqlalchemy import create_engine
import psycopg2
from flask import flash
from datetime import datetime,date


app = Flask(__name__)
app.secret_key=b'gifkey#635jk8927'
bcrypt = Bcrypt(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/gameif_db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

participacoes = db.Table('participacoes',
    db.Column('sala_id',db.Integer,db.ForeignKey('sala.id'),primary_key=True),
    db.Column('participante_id',db.Integer,db.ForeignKey('usuario.id'),primary_key=True),
)


app.register_blueprint(usuarios,url_prefix='/usuarios')
app.register_blueprint(professor,url_prefix='/professor')
app.register_blueprint(aluno,url_prefix='/aluno')
app.register_blueprint(admin,url_prefix='/admin')



db.init_app(app)

@app.route("/")
def index():
    #db.drop_all()
    #db.create_all()
    session.clear()
    messages = get_flashed_messages()  # Obter as flash messages
    return render_template("tela_login.html", messages=messages)

@app.route('/logos/<nome_arquivo>')
def logos(nome_arquivo):
    return send_from_directory('logos', nome_arquivo)

@app.route('/avatar/<nome_arquivo>')
def avatar(nome_arquivo):
    return send_from_directory('avatar', nome_arquivo)

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d/%m/%Y'):
    if isinstance(value, date):
        return value.strftime(format)
    return datetime.strptime(value, '%Y-%m-%d').strftime(format)