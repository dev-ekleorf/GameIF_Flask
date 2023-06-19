from sqlalchemy import desc, func, not_
from DAO.UsuarioDAO import UsuarioDAO
from Model.Resposta import Resposta
from Model.Sala import *
from Model.Usuario import *
from Model.Atividade import Atividade
from helper.config import *

class SalaDAO:
    def __init__(self):
        pass

    def adicionarSala(self,sala):
        db.session.add(sala)
        db.session.commit()
    
    def listarSalas(self):
        vetSalas = Sala.query.all()
        if(vetSalas is None):
            return []
        return vetSalas
    
    def listar_salas_para_participar(self,id_aluno):
        vetSalas = Sala.query.filter(not_(Sala.participantes.any(id=id_aluno))).all()
        if(vetSalas is None):
            return []
        return vetSalas
    

    def removeSala(self,id):
        salaRecuperada = self.recuperaSala(id)
        db.session.delete(salaRecuperada)
        db.session.commit()

    def editarSala(self,sala):
        db.session.commit()
    

    def recuperaSala(self,id):
        salaRecuperada = Sala.query.get(id)
        return salaRecuperada

    def recupera_salas_usuario(self,usuario):
        salas_recuperadas = usuario.salas
        print("sala_recuperadas: "+str(salas_recuperadas))
        if salas_recuperadas is None:
            salas_recuperadas = []
        return salas_recuperadas

    from sqlalchemy import desc

    def gerar_ranking(self,sala_id):
        # Consulta as pontuações dos alunos da sala específica
        pontuacoes = db.session.query(Usuario.id, Usuario.nome, Usuario.apelido,Usuario.avatar, func.sum(Resposta.pontuacao_recebida).label('pontuacao_total')).\
            join(Usuario.respostas).\
            join(Resposta.atividade).\
            filter(Atividade.sala_id == sala_id).\
            group_by(Usuario.id, Usuario.nome).\
            order_by(desc('pontuacao_total')).all()

        # Cria uma lista de dicionários contendo as informações de cada aluno no ranking
        ranking = []
        posicao = 1
        for aluno_id, aluno_nome, aluno_apelido,aluno_avatar, pontuacao_total in pontuacoes:
            aluno_info = {
                'posicao': posicao,
                'aluno_id': aluno_id,
                'aluno_nome': aluno_nome,
                'aluno_apelido':aluno_apelido,
                'aluno_avatar':aluno_avatar,
                'pontuacao_total': pontuacao_total
            }
            ranking.append(aluno_info)
            posicao += 1



        print("ranking: "+str(ranking))
        return ranking
    
    def preencher_ranking_nao_respondentes(self,id_sala,id_usuario):
        ranking = self.gerar_ranking(id_sala)

        usuarioDAO = UsuarioDAO()
        usuario = usuarioDAO.recuperaUsuario(id_usuario)
        flag = ""
        for aluno_info in ranking:
            if aluno_info['aluno_id'] == usuario.id:
                print("dentro do ranking!")
                flag=True
                break
            else:
                print("fora do ranking")
                
                flag=False

        if(flag == False):
            aluno_info = {
                    'posicao': len(ranking),
                    'aluno_id': usuario.id,
                    'aluno_nome': usuario.nome,
                    'aluno_apelido':usuario.apelido,
                    'aluno_avatar':usuario.avatar,
                    'pontuacao_total': 0
                }
            ranking.append(aluno_info)

        print("Está no ranking: "+str(flag))
        return ranking