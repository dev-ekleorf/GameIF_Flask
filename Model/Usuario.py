from helper.config import *

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, unique=True, nullable=False)
    senha = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String, nullable=True)
    tipo = db.Column(db.String, nullable=False)
    participando = db.relationship('Sala', secondary="usuario_participa_sala", backref='participantes')

