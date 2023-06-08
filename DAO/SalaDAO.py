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
