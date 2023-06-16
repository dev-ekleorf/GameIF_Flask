from sqlalchemy import func
from Model.Sala import *
from Model.Usuario import *
from Model.Atividade import Atividade
from Model.Resposta import Resposta
from helper.config import *

class RespostaDAO():
    def remove_resposta(self,id):
        print("Remove Resposta")
        print("id recebidoÇ "+str(type(id)))
        respostaRecuperada = self.recupera_resposta(id)
        db.session.delete(respostaRecuperada)
        db.session.commit()

    def recupera_resposta(self,id):
        print("Recupera Resposta")
        respostaRecuperada = Resposta.query.get(id)
        return respostaRecuperada

    def grava_resposta(self,resposta):
        
        db.session.commit()

    def atividades_realizadas_usuario(self,id_usuario):
        sala_atividades_respondidas = db.session.query(
        Sala.id,
        Usuario.id,
        func.count(Resposta.id).label('atividades_respondidas')
         ).select_from(Sala).join(Atividade).join(Resposta).join(Usuario).filter(Usuario.id == id_usuario).group_by(Sala.id, Usuario.id).all()

        atividades_realizadas = {(sala_id): count for sala_id, usuario_id, count in sala_atividades_respondidas}

        print("atividades_realizadas"+str(atividades_realizadas))
        return atividades_realizadas

   
    def obter_lista_pontuacao_aluno(self, sala_id, usuario_id):
        pontuacoes = db.session.query(Atividade.id, Resposta.id, Resposta.pontuacao_recebida).\
            join(Sala).join(Resposta, db.and_(Resposta.atividade_id == Atividade.id, Resposta.usuario_id == usuario_id)).\
            filter(Sala.id == sala_id).all()

        lista_pontuacoes = []

        for atividade_id, resposta_id, pontuacao in pontuacoes:
            pontuacao_info = {
                'atividade_id': atividade_id,
                'resposta_id': resposta_id,
                'pontuacao': pontuacao if pontuacao is not None else 0
            }
            lista_pontuacoes.append(pontuacao_info)

        return lista_pontuacoes