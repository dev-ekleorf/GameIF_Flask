from flask import Flask
from flask import Blueprint
from flask import render_template,redirect, url_for, request, session,send_from_directory,jsonify

from Model.Sala import Sala
from Model.Atividade import Atividade

salas = Blueprint('salas', __name__,
                        template_folder='templates', static_folder='static')


@salas.route("/carregar_sala/<int:id>")
def carregar_sala(id):
    atividade1 = Atividade(1,"Atividade 1","Envie uma foto do livro x")
    atividade2 = Atividade(1,"Atividade 2","Fale sobre o livro x")
    array_atividades = []
    array_atividades.append(atividade1)
    array_atividades.append(atividade2)
    sala_selecionada = Sala(1,"teste","19112021013321_51yHBMzxszL._AC_SY445_.jpg",array_atividades,"")
    return render_template("sala_aluno.html",sala_selecionada=sala_selecionada)