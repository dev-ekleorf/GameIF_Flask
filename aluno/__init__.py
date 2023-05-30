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

aluno = Blueprint('aluno', __name__,
                        template_folder='templates', static_folder='static')

@aluno.route("/procurar_salas")
def procurar_salas():
    salaDAO = SalaDAO()
    salas_disponiveis = salaDAO.listarSalas()
    return render_template("lista_salas.html",salas=salas_disponiveis)

@aluno.route("/participar/<int:id>")
def participar(id):
    salaDAO = SalaDAO()
    id_usuario = session['usuarioLogado']
    sala = salaDAO.recuperaSala(id)
    usuarioDAO = UsuarioDAO()
    sala.participantes.append(usuarioDAO.recuperaUsuario(id_usuario))
    salaDAO.editarSala(sala)
    return redirect(url_for('usuarios.minhas_salas',id_usuario=id_usuario))


@aluno.route("/sair_da_sala/<int:id_sala>")
def sair_da_sala(id_sala):
    id_usuario = session['usuarioLogado']
    salaDAO = SalaDAO()
    usuarioDAO = UsuarioDAO()
    usuario = usuarioDAO.recuperaUsuario(id_usuario)
    sala = salaDAO.recuperaSala(id_sala)
    sala.participantes.remove(usuario)
    salaDAO.editarSala(sala)
    salas = salaDAO.recupera_salas_usuario(usuario)
    return render_template("principal_aluno.html",arraySalas=salas)

@aluno.route("/carregar_sala/<int:id>")
def carregar_sala(id):
    salaDAO = SalaDAO()
    sala_selecionada = salaDAO.recuperaSala(id)
    return render_template("sala_aluno.html",sala_selecionada=sala_selecionada)