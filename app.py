from flask import *
from flask import blueprints
from DAO.UsuarioDAO import UsuarioDAO
from usuarios import usuarios
from salas import salas
from flask_bcrypt import Bcrypt
from helper.config import *

app = Flask(__name__)
app.secret_key=b'gifkey#635jk8927'
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/gameif_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

usuario_participa_sala = db.Table(
    "usuario_participa_sala",
    db.Column("id",db.Integer, primary_key=True),
    db.Column("usuario_id",db.Integer,db.ForeignKey("usuario.id")),
    db.Column("sala_id",db.Integer,db.ForeignKey("sala.id")),
    db.Column("pontuacao",db.Integer)
)
app.register_blueprint(usuarios,url_prefix='/usuarios')
app.register_blueprint(salas,url_prefix='/salas')

db.init_app(app)

@app.route("/")
def index():
    #db.drop_all()
    #db.create_all()
    return render_template("telaLogin.html")

@app.route('/logos/<nome_arquivo>')
def logos(nome_arquivo):
    return send_from_directory('logos', nome_arquivo)