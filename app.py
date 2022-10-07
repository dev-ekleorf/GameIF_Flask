from flask import *
from flask import blueprints
from DAO.UsuarioDAO import UsuarioDAO
from usuarios import usuarios

app = Flask(__name__)

import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate("C:\\Users\\ekleorf\\Documents\\gameif-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client() 

app.register_blueprint(usuarios,url_prefix='/usuarios')


@app.route("/")
def index():
    print("Inicial.")
    emp_ref = db.collection('usuarios')
    docs = emp_ref.stream()
    for doc in docs: print('{} => {} '.format(doc.id, doc.to_dict()))
    usuario_dao = UsuarioDAO().listar_usuarios()
    return render_template("telaLogin.html")

@app.route('/logos/<nome_arquivo>')
def logos(nome_arquivo):
    return send_from_directory('logos', nome_arquivo)