import datetime
from flask import Flask
from flask import Blueprint
from flask import render_template,redirect, url_for, request, session,send_from_directory
from DAO.AtividadeDAO import AtividadeDAO
from DAO.RespostaDAO import RespostaDAO
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
    id_usuario = session['usuarioLogado']
    salaDAO = SalaDAO()
    salas_disponiveis = salaDAO.listar_salas_para_participar(id_usuario)
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
    respostaDAO = RespostaDAO()
    atividades_realizadas = respostaDAO.atividades_realizadas_usuario(id_usuario)
    return render_template("principal_aluno.html",arraySalas=salas,atividades_realizadas=atividades_realizadas)

@aluno.route("/carregar_sala/<int:id>")
def carregar_sala(id):
    salaDAO = SalaDAO()
    respostaDAO = RespostaDAO()
    sala_selecionada = salaDAO.recuperaSala(id)
    pontuacao_sala = sum(atividade.pontuacao for atividade in sala_selecionada.atividades)
    aluno_id = session['usuarioLogado']
    pontuacao_aluno = UsuarioDAO.calcular_pontuacao_total_aluno(aluno_id,sala_selecionada.id)
    
    atividades_realizadas = respostaDAO.atividades_realizadas_usuario(aluno_id)
    print("atividades_realizadas: "+str(atividades_realizadas))
    print("atividades realizadas na sala: "+str(atividades_realizadas.get(id)))
    porcentagem_preencher_imagem = calcula_porcentagem_preencher_imagem(atividades_realizadas,sala_selecionada,id)

    print("porcentagem_preencher_imagem: "+str(porcentagem_preencher_imagem))
    ranking = salaDAO.gerar_ranking(sala_selecionada.id)
    ranking = salaDAO.preencher_ranking_nao_respondentes(sala_selecionada.id,aluno_id)
    ranking = popula_ranking_com_preencher_imagem(ranking,sala_selecionada.id)
    print("Ranking com porcentagem de sala: "+str(ranking))
    lista_pontuacao_aluno = respostaDAO.obter_lista_pontuacao_aluno(sala_selecionada.id,aluno_id)
    print("lista_pontuacao_aluno: "+str(lista_pontuacao_aluno))
    posicao_no_ranking = UsuarioDAO.obter_posicao_aluno(ranking,aluno_id)
    data_atual = date.today()
    return render_template("sala_aluno.html",sala_selecionada=sala_selecionada,pontuacao_aluno=pontuacao_aluno,pontuacao_sala=pontuacao_sala,posicao_no_ranking=posicao_no_ranking,porcentagem_preencher_imagem=porcentagem_preencher_imagem,ranking=ranking,lista_pontuacao_aluno=lista_pontuacao_aluno,data_atual=data_atual)

def popula_ranking_com_preencher_imagem(ranking,sala_id):
    respostaDAO = RespostaDAO()
    salaDAO = SalaDAO()
    sala_selecionada = salaDAO.recuperaSala(sala_id)
    for posicao in ranking:
        print("aqui: "+str(posicao))
        atividades_realizadas = respostaDAO.atividades_realizadas_usuario(posicao['aluno_id'])
        posicao['porcentagem_avatar']=calcula_porcentagem_preencher_imagem(atividades_realizadas,sala_selecionada,sala_selecionada.id)
        print("posicao['porcentagem_avatar']? "+str(posicao['porcentagem_avatar']))
    return ranking

def calcula_porcentagem_preencher_imagem(atividades_realizadas,sala_selecionada,id):
    try:
        if(atividades_realizadas.get(id) is None):
            print("Nenhuma atividade Realizada.")
            porcentagem_preencher_imagem = 0
        else:
            porcentagem_preencher_imagem = (atividades_realizadas.get(id)*100)/len(sala_selecionada.atividades)
        print("deu certo no try")
        return porcentagem_preencher_imagem
    except Exception as erro:
        print("entrou no except: "+str(erro))
        porcentagem_preencher_imagem = 100
        return porcentagem_preencher_imagem

@aluno.route("/resolve_atividade/<int:atividade_id>",methods=['POST'])
def resolve_atividade(atividade_id):
    print("Resolve Atividade.")
    atividadeDAO = AtividadeDAO()
    atividade = atividadeDAO.recupera_atividade(atividade_id)
    

    if(atividade.tipo == "envio-arquivo"):
        resposta = request.files.get('resposta')
            
        dataSave = datetime.datetime.now().strftime('%d%m%Y%H%M%S')
        print(dataSave)
        resposta.save(f'respostas/{dataSave}_{resposta.filename}')
        endereco_arquivo = dataSave+'_'+resposta.filename
        resposta = endereco_arquivo

    else:
        resposta=request.form['resposta']

    resposta = Resposta(usuario_id=session['usuarioLogado'],atividade_id=atividade_id,resposta=resposta,data_de_resposta=date.today())
    
    
    
    
    atividadeDAO.grava_resposta(resposta)
    sala_id = atividade.sala_id




    return redirect(url_for('aluno.carregar_sala',id=sala_id))


@aluno.route("/excluir_resposta/<int:id_sala>/<int:id_resposta>")
def excluir_resposta(id_sala,id_resposta):
    print("id_sala:"+str(id_sala))
    print("id_resposta:"+str(id_resposta))
    respostaDAO = RespostaDAO()
    respostaDAO.remove_resposta(id_resposta)
    
    return redirect(url_for('aluno.carregar_sala',id=id_sala))
