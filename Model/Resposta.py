from helper.config import *

class Resposta(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividade.id'))
    resposta = db.Column(db.String,nullable=False)
    data_de_resposta = db.Column(db.Date,nullable=False)
    pontuacao_recebida = db.Column(db.Integer)
    
    usuario = db.relationship("Usuario", back_populates="respostas")
    atividade = db.relationship("Atividade", back_populates="respostas")