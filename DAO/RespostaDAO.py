from Model.Sala import *
from Model.Usuario import *
from Model.Atividade import Atividade
from Model.Resposta import Resposta
from helper.config import *

class RespostaDAO():
    def remove_resposta(self,id):
        atividadeRecuperada = self.recupera_atividade(id)
        db.session.delete(atividadeRecuperada)
        db.session.commit()

    def recupera_resposta(self,id):
        respostaRecuperada = Resposta.query.get(id)
        return respostaRecuperada

    def grava_resposta(self,resposta):
        
        db.session.commit()
