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

usuarios = Blueprint('usuarios', __name__,
                        template_folder='templates', static_folder='static')
bcrypt = Bcrypt()


@usuarios.route("/login",methods=['POST'])
def login():
    login = request.form['login']
    senha = request.form['senha']
    print("Login: "+login)

    usuario_logado = Usuario()
    usuario_logado = UsuarioDAO.validaLogin(login,senha)
    if(usuario_logado == False):
        print("Falha ao logar")
        return redirect("/")
    else:
        session['usuarioLogado'] = usuario_logado.id
        session['tipo_usuario'] = usuario_logado.tipo
        return redirect(url_for('usuarios.principal'))


@usuarios.route('/principal')
def principal():
    id_usuario = session['usuarioLogado']
    usuarioDAO = UsuarioDAO()
    usuario_logado = usuarioDAO.recuperaUsuario(id_usuario)
    salaDAO = SalaDAO()
    arraySalas = salaDAO.recupera_salas_usuario(usuario_logado)
    salas = salaDAO.recupera_salas_usuario(usuario_logado)
    if(usuario_logado.tipo == "professor"):
        return redirect(url_for('professor.principal'))
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
    email = request.form['email']
    avatar = request.files['avatar_usuario']
    tipo_usuario = request.form['tipo-usuario']

    if(avatar.filename == ""):
        dataSave = ""
        endereco_arquivo="avatar.jpg"
    else:    
        dataSave = datetime.datetime.now().strftime('%d%m%Y%H%M%S')
        print(dataSave)
        avatar.save(f'avatar/{dataSave}_{avatar.filename}')
        endereco_arquivo = dataSave+'_'+avatar.filename

    print("usuario: "+usuario)
    print("senha: "+senha)
    print("email: "+email)
    print("tipo_usuario: "+tipo_usuario)
    print("avatar: "+endereco_arquivo)

    user = Usuario(nome=usuario,senha=senha,email=email,tipo=tipo_usuario,avatar=endereco_arquivo)

    usuarioDAO = UsuarioDAO()        
    usuarioDAO.adicionaUsuario(user)
    print("session: "+str(session))
    if('tipo_usuario' in session):
        if(session['tipo_usuario'] == "admin"):
            return redirect(url_for('usuarios.principal'))
    return redirect("/")
@usuarios.route("/tela_cadastro")
def telaCadastro():
    return render_template("tela_cadastro.html")


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
    usuarioDAO = UsuarioDAO()
    usuarioRecuperado = usuarioDAO.recuperaUsuario(id)
    return render_template("editarUsuario.html",usuario=usuarioRecuperado)

@usuarios.route("/editarUsuario/<int:id>",methods=['POST'])
def editarUsuario(id):
    print("Editar Usuario!")
    nome = request.form['usuario']
    senha = str(bcrypt.generate_password_hash(request.form['senha']).decode('utf-8'))
    email = request.form['email']
    avatar = request.files['avatar_usuario']
    tipo_usuario = request.form['tipo-usuario']

    if(avatar.filename == ""):
        dataSave = ""
        endereco_arquivo="avatar.jpg"
    else:    
        dataSave = datetime.datetime.now().strftime('%d%m%Y%H%M%S')
        print(dataSave)
        avatar.save(f'avatar/{dataSave}_{avatar.filename}')
        endereco_arquivo = dataSave+'_'+avatar.filename

    print("usuario: "+nome)
    print("senha: "+senha)
    print("email: "+email)
    print("tipo_usuario: "+tipo_usuario)
    print("avatar: "+endereco_arquivo)

    usuarioDAO = UsuarioDAO()        
    usuario =usuarioDAO.recuperaUsuario(id)
    usuario.nome = nome
    usuario.senha = senha
    usuario.email = email
    usuario.avatar = endereco_arquivo
    usuario.tipo = tipo_usuario

    usuarioDAO.editarUsuario(usuario)

   
    return redirect(url_for('usuarios.principal'))
   


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

@usuarios.route("/minhas_salas")
def minhas_salas():
        return redirect(url_for('usuarios.principal'))
