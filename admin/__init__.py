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

admin = Blueprint('admin', __name__,
                        template_folder='templates', static_folder='static')


@admin.route("/procurar_salas")
def procurar_salas():
    salaDAO = SalaDAO()
    salas_disponiveis = salaDAO.listarSalas()
    return render_template("lista_salas.html",salas=salas_disponiveis)

@admin.route('/principal')
def principal():
    id_usuario = session['usuarioLogado']
    usuarioDAO = UsuarioDAO()
    usuario_logado = usuarioDAO.recuperaUsuario(id_usuario)
    salaDAO = SalaDAO()
    arraySalas = salaDAO.recupera_salas_usuario(usuario_logado)
    salas = salaDAO.recupera_salas_usuario(usuario_logado)
    if(usuario_logado.tipo == "admin"):
        return render_template("principal_admin.html",arraySalas=arraySalas)