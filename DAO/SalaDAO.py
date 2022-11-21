from Model.Sala import Sala
from Model.Atividade import Atividade
from helper.config import *

class SalaDAO:
    def __init__(self):
        pass

    def adicionaSala(self,sala):
        db.session.add(sala)
        db.session.commit()
    
    def listarSalas(self):
        vetSalas = Sala.query.all()
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

    def recupera_salas_usuario(id_usuario):
        salasRecuperada = Sala.query.get(id_usuario)


        atividade1 = Atividade(id=1,nome="Atividade 1",descricao="Envie uma foto do livro x")
        atividade2 = Atividade(id=1,nome="Atividade 2",descricao="Fale sobre o livro x")
        array_atividades = []
        array_atividades.append(atividade1)
        array_atividades.append(atividade2)
        sala = Sala(id=1,nome="Projeto de Leitura",logo="livros.webp",atividades=array_atividades)
        arraySalas = []
        arraySalas.append(sala)
        sala2 = Sala(id=1,nome="Eletrônica",logo="arduino.jfif",atividades=array_atividades)
        arraySalas.append(sala2)

        return arraySalas
