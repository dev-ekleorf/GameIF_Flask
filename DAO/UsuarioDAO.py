from Model.Usuario import Usuario
from helper.config import *
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
class UsuarioDAO:

    def __init__(self):
        pass

    def adicionaUsuario(self,usuario):
        db.session.add(usuario)
        db.session.commit()
    
    def listarUsuarios():
        vetUsuarios = Usuario.query.all()
        return vetUsuarios

    def validaLogin(nome,senha):
        print("Valida Login!")
        try:
            usuarioRecuperado = Usuario.query.filter_by(nome=nome).first()
            if(usuarioRecuperado is not None):
                print("senha do usuarioRecuperado: "+usuarioRecuperado.senha)
                print("senha digitada: "+senha)
                bcrypt.check_password_hash(usuarioRecuperado.senha, senha)
                if(bcrypt.check_password_hash(usuarioRecuperado.senha, senha)):
                    print("Usuario Encontrado no banco.")
                    print("usuario encontrado: "+str(usuarioRecuperado.id))
                    print("tipo usuario: "+usuarioRecuperado.tipo)
                    return usuarioRecuperado
                else:
                    return False
            return False
        except:
            print("Não foi possível encontrar usuário.")
            return False

    def removeUsuario(self,id):
        usuarioRecuperado = self.recuperaUsuario(id)
        db.session.delete(usuarioRecuperado)
        db.session.commit()

    def editarUsuario(self,usuario):
        db.session.commit()

    def recuperaUsuario(self,id):
        usuarioRecuperado = Usuario.query.get(id)
        return usuarioRecuperado
