from flask import Flask
from flask import Blueprint
from flask import render_template,redirect, url_for, request, session,send_from_directory
from DAO.AtividadeDAO import AtividadeDAO
from DAO.UsuarioDAO import UsuarioDAO
from DAO.SalaDAO import SalaDAO
from Model.Usuario import Usuario
from flask import json, jsonify
from flask_bcrypt import Bcrypt
from datetime import date

from Model.Sala import Sala
from Model.Atividade import Atividade
from Model.Usuario import Usuario
from Model.Resposta import Resposta

aluno = Blueprint('aluno', __name__,
                        template_folder='templates', static_folder='static')

@aluno.route("/procurar_salas")
def procurar_salas():
    salaDAO = SalaDAO()
    salas_disponiveis = salaDAO.listarSalas()
    return render_template("lista_salas.html",salas=salas_disponiveis)

@aluno.route("/participar/<int:id>")
def participar(id):
    salaDAO = SalaDAO()
    id_usuario = session['usuarioLogado']
    sala = salaDAO.recuperaSala(id)
    usuarioDAO = UsuarioDAO()
    sala.participantes.append(usuarioDAO.recuperaUsuario(id_usuario))
    salaDAO.editarSala(sala)
    return redirect(url_for('usuarios.minhas_salas',id_usuario=id_usuario))


@aluno.route("/sair_da_sala/<int:id_sala>")
def sair_da_sala(id_sala):
    id_usuario = session['usuarioLogado']
    salaDAO = SalaDAO()
    usuarioDAO = UsuarioDAO()
    usuario = usuarioDAO.recuperaUsuario(id_usuario)
    sala = salaDAO.recuperaSala(id_sala)
    sala.participantes.remove(usuario)
    salaDAO.editarSala(sala)
    salas = salaDAO.recupera_salas_usuario(usuario)
    return render_template("principal_aluno.html",arraySalas=salas)

@aluno.route("/carregar_sala/<int:id>")
def carregar_sala(id):
    salaDAO = SalaDAO()
    sala_selecionada = salaDAO.recuperaSala(id)
    pontuacao_sala = sum(atividade.pontuacao for atividade in sala_selecionada.atividades)
    aluno_id = session['usuarioLogado']
    pontuacao_aluno = UsuarioDAO.calcular_pontuacao_total_aluno(aluno_id,sala_selecionada.id)
    ranking =UsuarioDAO.gerar_ranking(id)
    posicao_no_ranking = UsuarioDAO.obter_posicao_aluno(ranking,aluno_id)
    porcentagem_preencher_imagem = (pontuacao_aluno*100)/pontuacao_sala
    print("porcentagem_preencher_imagem: "+str(porcentagem_preencher_imagem))
    return render_template("sala_aluno.html",sala_selecionada=sala_selecionada,pontuacao_aluno=pontuacao_aluno,pontuacao_sala=pontuacao_sala,posicao_no_ranking=posicao_no_ranking,porcentagem_preencher_imagem=porcentagem_preencher_imagem)

@aluno.route("/resolve_atividade/<int:atividade_id>",methods=['POST'])
def resolve_atividade(atividade_id):
    print("Resolve Atividade.")
    
    resposta = Resposta(usuario_id=session['usuarioLogado'],atividade_id=atividade_id,resposta=request.form['resposta'],data_de_resposta=date.today())
    atividadeDAO = AtividadeDAO()
    atividade = atividadeDAO.recupera_atividade(atividade_id)
    atividadeDAO.grava_resposta(resposta)
    sala_id = atividade.sala_id
    return redirect(url_for('aluno.carregar_sala',id=sala_id))