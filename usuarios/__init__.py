from flask import Flask
from flask import Blueprint
from flask import render_template,redirect, url_for, request, session,send_from_directory,jsonify

from Model.Sala import Sala
from Model.Atividade import Atividade

usuarios = Blueprint('usuarios', __name__,
                        template_folder='templates', static_folder='static')


@usuarios.route("/login",methods=['POST'])
def login():
    login = request.form['login']
    senha = request.form['senha']

    #bypass Login
    #Implementar!
    print("Login: "+login)

    if(login == "Raquel"):
        session['usuarioLogado'] = 1
        return render_template("principal_professor.html")
    elif(login == "Erik"):
        
        atividade1 = Atividade(1,"Atividade 1","Envie uma foto do livro x")
        atividade2 = Atividade(1,"Atividade 2","Fale sobre o livro x")
        array_atividades = []
        array_atividades.append(atividade1)
        array_atividades.append(atividade2)
        sala = Sala(1,"teste","19112021013321_51yHBMzxszL._AC_SY445_.jpg",array_atividades,"")
        arraySalas = []
        arraySalas.append(sala)
        print(sala.getNome())
        session['usuarioLogado'] = 2
        return render_template("principal_aluno.html",arraySalas = arraySalas)
    else:
        return redirect("/")

    #usuarioDAO = UsuarioDAO()
    #id = usuarioDAO.validaLogin(login,senha)
    print("Usuario logado: "+str(id))
    #if(id):
        #session['usuarioLogado'] = id
       # return redirect(url_for("principal"))
    #else:
       # return redirect("/")

@usuarios.route('/principal/<int:id>')
def principal(id):
    if(id == 2):
        return render_template("principal_professor.html")

    elif(id == 1):
        return render_template("principal_aluno.html")

@usuarios.route('/listar_usuarios') 
def listar_usuarios():
    try: 
        print("")
    except Exception as e: 
        return f"Ocorreu um erro: {e}"

@usuarios.route("/adicionarUsuario",methods=['POST'])
def adicionarUsuario():
    
    usuario = request.form['usuario']
    #senha = str(bcrypt.generate_password_hash(request.form['senha']).decode('utf-8'))
    print("usuarioform: "+usuario)
    #print("senhaform: "+senha)

    #user = Usuario(nome=usuario,senha=senha)
    
    #print("usuariomodel: "+user.nome)
   # print("senhamodel: "+user.senha)
    #usuarioDAO = UsuarioDAO()    
    
    #usuarioDAO.adicionaUsuario(user)

    return redirect("usuarios")

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