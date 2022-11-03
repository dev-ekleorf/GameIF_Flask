from flask import Flask
from flask import Blueprint
from flask import render_template,redirect, url_for, request, session,send_from_directory,jsonify

from Model.Sala import Sala
from Model.Atividade import Atividade

salas = Blueprint('salas', __name__,
                        template_folder='templates', static_folder='static')


@salas.route("/carregar_sala/<int:id>")
def carregar_sala(id):
    atividade1 = Atividade(1,"Atividade 1","Envie uma foto do livro x","Foto")
    atividade2 = Atividade(2,"Atividade 2","Fale sobre o livro x","RespostaLonga")
    array_atividades = []
    array_atividades.append(atividade1)
    array_atividades.append(atividade2)
    sala_selecionada = Sala(1,"Projeto de Leitura","Sala para incentrivar a leitura!","livros.webp",array_atividades,"")
    return render_template("sala_aluno.html",sala_selecionada=sala_selecionada)

@salas.route("/procurar_salas")
def procurar_salas():
    atividade1 = Atividade(1,"Atividade 1","Envie uma foto do livro x")
    atividade2 = Atividade(2,"Atividade 2","Fale sobre o livro x")
    array_atividades = []
    array_atividades.append(atividade1)
    array_atividades.append(atividade2)
    sala = Sala(1,"Projeto de Leitura","Sala para incentivar a leitura.","livros.webp",array_atividades,"")
    salas_disponiveis = []
    sala2 = Sala(1,"Eletrônica","isso é uma descrição","arduino.jfif",array_atividades,"")
    salas_disponiveis.append(sala2)
    salas_disponiveis.append(sala)
    return render_template("lista_salas.html",salas=salas_disponiveis)

@salas.route("/minhas_salas")
def minhas_salas():
    atividade1 = Atividade(1,"Atividade 1","Envie uma foto do livro x")
    atividade2 = Atividade(2,"Atividade 2","Fale sobre o livro x")
    array_atividades = []
    array_atividades.append(atividade1)
    array_atividades.append(atividade2)
    sala = Sala(1,"Projeto de Leitura","Sala para incentivar a leitura.","livros.webp",array_atividades,"")
    salas_disponiveis = []
    sala2 = Sala(1,"Eletrônica","isso é uma descrição","arduino.jfif",array_atividades,"")
    salas_disponiveis.append(sala2)
    salas_disponiveis.append(sala)
    return render_template("principal_aluno.html",arraySalas=salas_disponiveis)