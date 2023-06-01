from helper.config import *

class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    descricao = db.Column(db.String, nullable=False)
    pontuacao = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String, nullable=False)
    sala_id = db.Column(db.Integer, db.ForeignKey("sala.id"))
  
    
    def getId(self):
        return self.__id

    def getNome(self):
        return self.__nome
    
    def getDescricao(self):
        return self.__descricao
    
    def getTipo(self):
        return self.__tipo   
