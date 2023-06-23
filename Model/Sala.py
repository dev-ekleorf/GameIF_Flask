from helper.config import *

class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, unique=True, nullable=False)
    logo = db.Column(db.String, nullable=True)
    descricao = db.Column(db.String, nullable=True)
    atividades = db.relationship("Atividade")
    participantes = db.relationship('Usuario', secondary="participacoes", back_populates='salas')
    
        
    def getId(self):
        return self.__id

    def getNome(self):
        return self.__nome

    def getDescricao(self):
        return self.__descricao
    
    def getLogo(self):
        return self.__logo

    def getAtividades(self):
        return self.__atividades
    
    def getParticipantes(self):
        return self.__participantes
    

    def getProfessor(self):
        for participante in self.participantes:
            if participante.tipo == "professor":
                return participante
        return ""
    
