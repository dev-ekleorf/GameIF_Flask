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


    def calcular_pontuacao_total_aluno(aluno_id, sala_id):
        pontuacao_total = db.session.query(func.sum(Resposta.pontuacao_recebida)).\
            join(Resposta.atividade).\
            filter(Resposta.usuario_id == aluno_id, Atividade.sala_id == sala_id).scalar()

        return pontuacao_total or 0
    
    from sqlalchemy import desc

    def gerar_ranking(sala_id):
        # Consulta as pontuações dos alunos da sala específica
        pontuacoes = db.session.query(Usuario.id, Usuario.nome, func.sum(Resposta.pontuacao_recebida).label('pontuacao_total')).\
            join(Usuario.respostas).\
            join(Resposta.atividade).\
            filter(Atividade.sala_id == sala_id).\
            group_by(Usuario.id, Usuario.nome).\
            order_by(desc('pontuacao_total')).all()

        # Cria uma lista de dicionários contendo as informações de cada aluno no ranking
        ranking = []
        posicao = 1
        for aluno_id, aluno_nome, pontuacao_total in pontuacoes:
            aluno_info = {
                'posicao': posicao,
                'aluno_id': aluno_id,
                'aluno_nome': aluno_nome,
                'pontuacao_total': pontuacao_total
            }
            ranking.append(aluno_info)
            posicao += 1

        print("ranking: "+str(ranking))
        return ranking
    
    def obter_posicao_aluno(ranking, aluno_id):
        for aluno_info in ranking:
            if aluno_info['aluno_id'] == aluno_id:
                return aluno_info['posicao']
        return "Fora do Ranking"

