from flask import flash
from flask import Blueprint
from flask import render_template,redirect, url_for, request, session,send_from_directory
from DAO.AtividadeDAO import AtividadeDAO
from DAO.RespostaDAO import RespostaDAO
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
        print("Falha ao logar!")
        flash('Falha no Login. E-mail ou senha incorretos.', 'error')
        return redirect(url_for('index'))
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
    if(usuario_logado.tipo == "professor"):
        return redirect(url_for('professor.principal'))
    elif(usuario_logado.tipo == "aluno"):
        respostaDAO = RespostaDAO()
        atividades_realizadas = respostaDAO.atividades_realizadas_usuario(id_usuario)
        return render_template("principal_aluno.html",arraySalas=arraySalas,atividades_realizadas=atividades_realizadas)
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


@usuarios.route("/adicionar_usuario",methods=['POST'])
def adicionarUsuario():
    
    usuario = request.form['nome']
    apelido = request.form['apelido']
    senha = request.form['senha']
    confirme_senha = request.form['confirme-senha']
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
    print("apelido: "+apelido)
    print("senha: "+senha)
    print("confirme-senha: "+confirme_senha)
    print("email: "+email)
    print("tipo_usuario: "+tipo_usuario)
    print("avatar: "+endereco_arquivo)

    if(senha != confirme_senha):
        print("Senhas não conferem durante a criação do usuário.")
        flash('Falha na confirmação de senha, durante a criação do usuário.', 'error')
        return redirect(url_for('usuarios.tela_cadastro'))
    else:
        senha = str(bcrypt.generate_password_hash(senha).decode('utf-8'))

    user = Usuario(nome=usuario,apelido=apelido,senha=senha,email=email,tipo=tipo_usuario,avatar=endereco_arquivo)

    usuarioDAO = UsuarioDAO()        
    usuarioDAO.adicionaUsuario(user)
    print("session: "+str(session))
    if('tipo_usuario' in session):
        if(session['tipo_usuario'] == "admin"):
            return redirect(url_for('usuarios.principal'))
    return redirect("/")

@usuarios.route("/tela_cadastro")
def tela_cadastro():
    return render_template("tela_cadastro.html")


@usuarios.route("/telaAdicionarUsuario")
def telaAdicionarUsuario():
    return render_template("adicionarUsuario.html")

@usuarios.route("/excluirUsuario/<int:id>")
def excluirUsuario(id):
    usuarioDAO = UsuarioDAO()
    usuarioDAO.removeUsuario(id)
    return redirect(url_for('usuarios.listar_usuarios'))

@usuarios.route("/tela_editar_usuario/<int:id>")
def tela_editar_usuario(id):
    print("tela_editar_usuario: Id: "+str(id))
    usuarioDAO = UsuarioDAO()
    usuarioRecuperado = usuarioDAO.recuperaUsuario(id)
    return render_template("editarUsuario.html",usuario=usuarioRecuperado)

@usuarios.route("/editar_usuario/<int:id>",methods=['POST'])
def editar_usuario(id):
    print("Editar Usuario!")
    nome = request.form['nome']
    senha = request.form['senha']
    email = request.form['email']
    apelido = request.form['apelido']
    avatar = request.files['avatar_usuario']
    tipo_usuario = request.form['tipo-usuario']

    usuarioDAO = UsuarioDAO()        
    usuario =usuarioDAO.recuperaUsuario(id)

    if(usuario.senha != senha):
        senha = str(bcrypt.generate_password_hash(request.form['senha']).decode('utf-8'))
    else:
        senha = usuario.senha
        
    if(avatar.filename == ""):
        dataSave = ""
        endereco_arquivo=usuario.avatar
    else:    
        dataSave = datetime.datetime.now().strftime('%d%m%Y%H%M%S')
        print(dataSave)
        avatar.save(f'avatar/{dataSave}_{avatar.filename}')
        endereco_arquivo = dataSave+'_'+avatar.filename

    usuarioDAO = UsuarioDAO()        
    usuario =usuarioDAO.recuperaUsuario(id)
    usuario.nome = nome
    usuario.apelido = apelido
    usuario.senha = senha
    usuario.email = email
    usuario.avatar = endereco_arquivo
    usuario.tipo = tipo_usuario

    usuarioDAO.editarUsuario(usuario)

   
    return redirect(url_for('usuarios.meu_perfil'))
   


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
