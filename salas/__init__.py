from flask import Flask
from flask import Blueprint
from flask import render_template,redirect, url_for, request, session,send_from_directory,jsonify

from Model.Sala import Sala

salas = Blueprint('salas', __name__,
                        template_folder='templates', static_folder='static')


@salas.route("/carregar_sala/<int:id>")
def carregar_sala(id):
    sala_selecionada = Sala(1,"teste","19112021013321_51yHBMzxszL._AC_SY445_.jpg","","")
    return render_template("sala_aluno.html",sala_selecionada=sala_selecionada)