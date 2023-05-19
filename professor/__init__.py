from flask import Flask
from flask import Blueprint
from flask import render_template,redirect, url_for, request, session,send_from_directory
from DAO.UsuarioDAO import UsuarioDAO
from DAO.SalaDAO import SalaDAO
from Model.Usuario import Usuario
from flask import json, jsonify
from flask_bcrypt import Bcrypt
import datetime

from Model.Sala import Sala
from Model.Atividade import Atividade
from Model.Usuario import Usuario

professor = Blueprint('professor', __name__,
                        template_folder='templates', static_folder='static')
bcrypt = Bcrypt()


@professor.route('/principal')
def principal():
    id_usuario = session['usuarioLogado']
    usuarioDAO = UsuarioDAO()
    usuario_logado = usuarioDAO.recuperaUsuario(id_usuario)
    salaDAO = SalaDAO()
    arraySalas = salaDAO.recupera_salas_usuario(usuario_logado)
    salas = salaDAO.recupera_salas_usuario(usuario_logado)
    if(usuario_logado.tipo == "professor"):
        return render_template("principal_professor.html",arraySalas=arraySalas)

@professor.route("/carregar_sala/<int:id>")
def carregar_sala(id):
    salaDAO = SalaDAO()
    sala_selecionada = salaDAO.recuperaSala(id)
    return render_template("sala_professor.html",sala_selecionada=sala_selecionada)

@professor.route("/excluir_sala/<int:id>")
def excluir_sala(id):
    salaDAO = SalaDAO()
    salaDAO.removeSala(id)
    id_usuario = session['usuarioLogado']
    return redirect(url_for('professor.principal'))

@professor.route("/criar_sala",methods=['POST'])
def criar_sala():
    print("Criar Sala.")

    logo = request.files['logo']
    if(logo.filename == ""):
        dataSave = ""
        enderecoArquivo="logo_gameIF.jpeg"
    else:    
        dataSave = datetime.datetime.now().strftime('%d%m%Y%H%M%S')
        print(dataSave)
        logo.save(f'logos/{dataSave}_{logo.filename}')
        enderecoArquivo = dataSave+'_'+logo.filename
    
    sala = Sala(nome=request.form['nome_sala'],descricao=request.form['descricao'],logo=enderecoArquivo,atividades=[])
    usuarioDAO = UsuarioDAO()
    sala.participantes.append(usuarioDAO.recuperaUsuario(session['usuarioLogado']))
    salaDAO = SalaDAO()
    salaDAO.adicionarSala(sala)
    print("session['usuarioLogado']: "+str(session['usuarioLogado']))
    id_usuario = session['usuarioLogado']
    return redirect(url_for('salas.minhas_salas',id_usuario=id_usuario))

@professor.route("/carregar_sala/<int:id>")
def carregar_sala(id):
    salaDAO = SalaDAO()
    sala_selecionada = salaDAO.recuperaSala(id)
    return render_template("sala_professor.html",sala_selecionada=sala_selecionada)

@professor.route("/tela_criar_sala")
def tela_criar_salas():
    return render_template("adicionar_sala.html")