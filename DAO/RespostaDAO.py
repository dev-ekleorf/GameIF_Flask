from Model.Sala import *
from Model.Usuario import *
from Model.Atividade import Atividade
from Model.Resposta import Resposta
from helper.config import *

class RespostaDAO():
    def remove_resposta(self,id):
        respostaRecuperada = self.recupera_resposta(id)
        db.session.delete(respostaRecuperada)
        db.session.commit()

    def recupera_resposta(self,id):
        respostaRecuperada = Resposta.query.get(id)
        return respostaRecuperada

    def grava_resposta(self,resposta):
        
        db.session.commit()
