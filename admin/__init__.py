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


@admin.route("/listar_salas")
def listar_salas():
    salaDAO = SalaDAO()
    salas = salaDAO.listarSalas()
    return render_template("listar_salas.html",salas=salas)

@admin.route('/listar_usuarios') 
def listar_usuarios():
    try: 
        usuarios = UsuarioDAO.listarUsuarios()
        return render_template("listar_usuarios.html",usuarios=usuarios)
    except Exception as e: 
        return f"Ocorreu um erro: {e}"

@admin.route('/principal')
def principal():
    id_usuario = session['usuarioLogado']
    usuarioDAO = UsuarioDAO()
    usuario_logado = usuarioDAO.recuperaUsuario(id_usuario)
    salaDAO = SalaDAO()
    arraySalas = salaDAO.recupera_salas_usuario(usuario_logado)
    if(usuario_logado.tipo == "admin"):
        return render_template("principal_admin.html",arraySalas=arraySalas)
    
@admin.route("/tela_adicionar_usuario")
def tela_adicionar_usuario():
    return render_template("admin_adicionar_usuario.html")

@admin.route("/tela_editar_usuario/<id_usuario>")
def tela_editar_usuario(id_usuario):
    usuarioDAO = UsuarioDAO()
    usuario = usuarioDAO.recuperaUsuario(id_usuario)
    return render_template("admin_tela_editar_usuario.html",usuario=usuario)

@admin.route("/excluir_usuario/<int:id>")
def excluir_usuario(id):
    usuarioDAO = UsuarioDAO()
    usuarioDAO.removeUsuario(id)
    return redirect(url_for('admin.listar_usuarios'))
    

