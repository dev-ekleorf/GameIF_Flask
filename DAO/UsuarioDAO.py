from Model.Atividade import Atividade
from Model.Resposta import Resposta
from Model.Usuario import Usuario
from helper.config import *
from flask_bcrypt import Bcrypt
from sqlalchemy import func,desc

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

    def validaLogin(email,senha):
        print("Valida Login!")
        try:
            usuarioRecuperado = Usuario.query.filter_by(email=email).first()
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


    def calcular_pontuacao_total_aluno(aluno_id, sala_id):
        pontuacao_total = db.session.query(func.sum(Resposta.pontuacao_recebida)).\
            join(Resposta.atividade).\
            filter(Resposta.usuario_id == aluno_id, Atividade.sala_id == sala_id).scalar()

        return pontuacao_total or 0
    
    def obter_posicao_aluno(ranking, aluno_id):
        for aluno_info in ranking:
            if aluno_info['aluno_id'] == aluno_id:
                return aluno_info['posicao']
        return ""

