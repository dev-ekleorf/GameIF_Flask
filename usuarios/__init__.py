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
        salas = SalaDAO.recupera_salas_usuario(usuario_logado.id)
        if(usuario_logado.tipo == "professor"):
            return render_template("principal_professor.html",arraySalas=salas)
        elif(usuario_logado.tipo == "aluno"):
            print("Vai para a tela de Principal Aluno")
            for sala in salas:
                print(sala.nome)
            return render_template("principal_aluno.html",arraySalas=salas)
        elif(usuario_logado.tipo == "administrador"):
            return render_template("principal_administrador.html")
    return redirect("/")

@usuarios.route('/principal/<int:id>')
def principal(id):

    atividade1 = Atividade(1,"Atividade 1","Envie uma foto do livro x")
    atividade2 = Atividade(1,"Atividade 2","Fale sobre o livro x")
    array_atividades = []
    array_atividades.append(atividade1)
    array_atividades.append(atividade2)
    sala = Sala(1,"Projeto de Leitura","","livros.webp",array_atividades,"")
    arraySalas = []
    arraySalas.append(sala)
    sala2 = Sala(1,"Eletrônica","","arduino.jfif",array_atividades,"")
    arraySalas.append(sala2)
    print(sala.getNome())
    return render_template("principal_aluno.html",arraySalas = arraySalas)

@usuarios.route('/listar_usuarios') 
def listar_usuarios():
    try: 
        print("")
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
    #usuarioDAO = UsuarioDAO()
    #usuarioDAO.removeUsuario(id)
    return redirect(url_for('usuarios.listarUsuarios'))

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
    usuario = Usuario(session['usuarioLogado'],"Erik","teste")
    print(usuario)
    return render_template("meu_perfil.html",usuario=usuario)