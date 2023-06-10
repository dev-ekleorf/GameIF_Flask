from helper.config import *

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, unique=True, nullable=False)
    apelido = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    senha = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String, nullable=True)
    tipo = db.Column(db.String, nullable=False)
    respostas = db.relationship("Resposta", back_populates="usuario")
    salas = db.relationship('Sala',secondary="participacoes",back_populates="participantes")

