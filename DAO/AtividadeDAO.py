from Model.Sala import *
from Model.Usuario import *
from Model.Atividade import Atividade
from helper.config import *

class AtividadeDAO():
    def remove_atividade(self,id):
        atividadeRecuperada = self.recupera_atividade(id)
        db.session.delete(atividadeRecuperada)
        db.session.commit()

    def recupera_atividade(self,id):
        atividadeRecuperada = Atividade.query.get(id)
        return atividadeRecuperada

    def grava_resposta(self,resposta):
        db.session.add(resposta)
        db.session.commit()

    def salvar_atividade(self):
        db.session.commit()
