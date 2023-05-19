from flask import Flask
from flask import Blueprint
from flask import render_template,redirect, url_for, request, session,send_from_directory
from DAO.UsuarioDAO import UsuarioDAO
from DAO.SalaDAO import SalaDAO
from Model.Usuario import Usuario
from flask import json, jsonify
from flask_bcrypt import Bcrypt

from Model.Sala import Sala
from Model.Atividade import Atividade
from Model.Usuario import Usuario

usuarios = Blueprint('usuarios', __name__,
                        template_folder='templates', static_folder='static')
bcrypt = Bcrypt()


@usuarios.route("/login",methods=['POST'])
def login():
    login = request.form['login']
    senha = request.form['senha']
    print("Login: "+login)
    print("senha: "+senha)

    usuario_logado = Usuario()
    usuario_logado = UsuarioDAO.validaLogin(login,senha)
    if(usuario_logado == False):
        print("Falha ao logar")
        return redirect("/")
    else:
        session['usuarioLogado'] = usuario_logado.id
        session['tipo_usuario'] = usuario_logado.tipo
        salaDAO = SalaDAO()
        salas = salaDAO.recupera_salas_usuario(usuario_logado)
        if(usuario_logado.tipo == "professor"):
            return redirect(url_for('professor.principal'))
        elif(usuario_logado.tipo == "aluno"):
            print("Vai para a tela de Principal Aluno")
            return redirect(url_for('aluno.principal'))
        elif(usuario_logado.tipo == "admin"):
            usuarios = UsuarioDAO.listarUsuarios()
            return redirect(url_for('admin.principal'))
    return redirect("/")

@usuarios.route('/principal')
def principal():
    id_usuario = session['usuarioLogado']
    usuarioDAO = UsuarioDAO()
    usuario_logado = usuarioDAO.recuperaUsuario(id_usuario)
    salaDAO = SalaDAO()
    arraySalas = salaDAO.recupera_salas_usuario(usuario_logado)
    salas = salaDAO.recupera_salas_usuario(usuario_logado)
    if(usuario_logado.tipo == "professor"):
        return render_template("principal_professor.html",arraySalas=arraySalas)
    elif(usuario_logado.tipo == "aluno"):
        return render_template("principal_aluno.html",arraySalas=arraySalas)
    elif(usuario_logado.tipo == "admin"):
        usuarios = UsuarioDAO.listarUsuarios()
        return render_template("principal_administrador.html",usuarios=usuarios)

@usuarios.route('/listar_usuarios') 
def listar_usuarios():
    try: 
        usuarios = UsuarioDAO.listarUsuarios()
        return render_template("principal_administrador.html",usuarios=usuarios)
    except Exception as e: 
        return f"Ocorreu um erro: {e}"


@usuarios.route("/adicionarUsuario",methods=['POST'])
def adicionarUsuario():
    
    usuario = request.form['usuario']
    senha = str(bcrypt.generate_password_hash(request.form['senha']).decode('utf-8'))
    print("usuarioform: "+usuario)
    print("senhaform: "+senha)

    user = Usuario(nome=usuario,senha=senha,tipo="aluno")
    
    print("usuariomodel: "+user.nome)
    print("senhamodel: "+user.senha)
    usuarioDAO = UsuarioDAO()    
    
    usuarioDAO.adicionaUsuario(user)

    return redirect("/")

@usuarios.route("/tela_cadastro")
def telaCadastro():
    return render_template("tela_cadastro.html")

@usuarios.route("/cadastrarUsuario",methods=['POST'])
def cadastrarUsuario():
    usuario = request.form['usuario']
    #senha = str(bcrypt.generate_password_hash(request.form['senha']).decode('utf-8'))
    print("usuario: "+usuario)
    #print("senha: "+senha)

    #user = Usuario("",usuario,senha)
    #print("usuariomodel: "+user.nome)
    #print("senhamodel: "+user.senha)

    #usuarioDAO = UsuarioDAO()    
    
    #usuarioDAO.adicionaUsuario(user)

    return redirect("/")

@usuarios.route("/telaAdicionarUsuario")
def telaAdicionarUsuario():
    return render_template("adicionarUsuario.html")

@usuarios.route("/excluirUsuario/<int:id>")
def excluirUsuario(id):
    usuarioDAO = UsuarioDAO()
    usuarioDAO.removeUsuario(id)
    return redirect(url_for('usuarios.listar_usuarios'))

@usuarios.route("/telaEditarUsuario/<int:id>")
def telaEditarUsuario(id):
    print("telaEditarFilme: Id: "+str(id))
    #usuarioDAO = UsuarioDAO()
    usuarioRecuperado = ""#usuarioDAO.recuperaUsuario(id)
    return render_template("editarUsuario.html",usuarioRecuperado=usuarioRecuperado)

@usuarios.route("/editarUsuario/<int:id>",methods=['POST'])
def editarUsuario(id):
    print("Editar Usuario!")
    #usuarioDAO = UsuarioDAO()
    #usuario = usuarioDAO.recuperaUsuario(id)
    #usuario.nome = request.form['nome']
    #usuario.senha = str(bcrypt.generate_password_hash(request.form['senha']).decode('utf-8'))
    #usuarioDAO.editarUsuario(usuario)
    return redirect(url_for('usuarios.listarUsuarios'))


@usuarios.route("/logout")
def logout():
    print("Realiza Logoff.")
    session.pop('usuarioLogado',None)
    return redirect("/")

@usuarios.route("/recuperaUsuarios",methods=['GET', 'POST'])
def recuperaUsuarios():
    print("Recuperar Usuarios para o select!")
    #usuarioDAO = UsuarioDAO()
    #vetUsuarios = usuarioDAO.listarUsuarios()
    dictUsuarios = {}
    #for usuario in vetUsuarios:
       #dictUsuarios[usuario.id] = usuario.nome
    #return jsonify(dictUsuarios)

@usuarios.route("/meu_perfil")
def meu_perfil():
    print("Meu Perfil")
    #busca usuário por ID
    id_usuario = session['usuarioLogado']
    usuarioDAO = UsuarioDAO()
    usuario = usuarioDAO.recuperaUsuario(id_usuario)
    print(usuario)
    return render_template("meu_perfil.html",usuario=usuario)

@usuarios.route("/minhas_salas/<int:id_usuario>")
def minhas_salas(id_usuario):
    if session['tipo_usuario'] == "professor":
        return redirect(url_for('professor.principal'))
    elif session['tipo_usuario'] == "aluno":
        return redirect(url_for('aluno.principal'))

