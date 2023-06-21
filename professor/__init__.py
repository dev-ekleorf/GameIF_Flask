from flask import Flask, send_file
from flask import Blueprint
from flask import render_template,redirect, url_for, request, session,send_from_directory
from DAO.RespostaDAO import RespostaDAO
from DAO.UsuarioDAO import UsuarioDAO
from DAO.SalaDAO import SalaDAO
from DAO.AtividadeDAO import AtividadeDAO
from Model.Usuario import Usuario
from flask import json, jsonify
from flask_bcrypt import Bcrypt
import datetime

from Model.Sala import Sala
from Model.Atividade import Atividade
from Model.Usuario import Usuario

professor = Blueprint('professor', __name__,
                        template_folder='templates', static_folder='static')
bcrypt = Bcrypt()


@professor.route("/carregar_sala/<int:id>")
def carregar_sala(id):
    salaDAO = SalaDAO()
    sala_selecionada = salaDAO.recuperaSala(id)
    ranking = salaDAO.gerar_ranking(id)
    return render_template("sala_professor.html",sala_selecionada=sala_selecionada,ranking=ranking)

@professor.route('/principal')
def principal():
    print("Principal Professor")
    id_usuario = session['usuarioLogado']
    usuarioDAO = UsuarioDAO()
    usuario_logado = usuarioDAO.recuperaUsuario(id_usuario)
    salaDAO = SalaDAO()
    arraySalas = salaDAO.recupera_salas_usuario(usuario_logado)
    if(usuario_logado.tipo == "professor"):
        return render_template("principal_professor.html",arraySalas=arraySalas)

@professor.route("/excluir_sala/<int:id>")
def excluir_sala(id):
    salaDAO = SalaDAO()
    salaDAO.removeSala(id)
    id_usuario = session['usuarioLogado']
    return redirect(url_for('usuarios.principal'))

@professor.route("/criar_sala",methods=['POST'])
def criar_sala():
    print("Criar Sala.")

    logo = request.files['logo']
    if(logo.filename == ""):
        dataSave = ""
        enderecoArquivo="logo_gameIF.jpeg"
    else:    
        dataSave = datetime.datetime.now().strftime('%d%m%Y%H%M%S')
        print(dataSave)
        logo.save(f'logos/{dataSave}_{logo.filename}')
        enderecoArquivo = dataSave+'_'+logo.filename
    
    sala = Sala(nome=request.form['nome_sala'],descricao=request.form['descricao'],logo=enderecoArquivo,atividades=[])
    usuarioDAO = UsuarioDAO()
    sala.participantes.append(usuarioDAO.recuperaUsuario(session['usuarioLogado']))
    salaDAO = SalaDAO()
    salaDAO.adicionarSala(sala)
    print("session['usuarioLogado']: "+str(session['usuarioLogado']))
    id_usuario = session['usuarioLogado']
    return redirect(url_for('professor.principal'))

@professor.route("/tela_criar_sala")
def tela_criar_salas():
    return render_template("adicionar_sala.html")

@professor.route("/tela_criar_atividade/<int:id_sala>")
def tela_criar_atividade(id_sala):
    data_min = datetime.date.today().strftime('%Y-%m-%d')
    return render_template("adicionar_atividade.html", id_sala=id_sala,data_min=data_min)

@professor.route("/adicionar_atividade/<int:id_sala>",methods=['POST'])
def adicionar_atividade(id_sala):
    print("Criar atividade.")
    nome=request.form['nome_atividade']
    descricao=request.form['descricao']
    pontuacao=request.form['pontuacao']
    data_entrega=request.form['data_entrega']
    tipo_atividade=request.form['tipo_atividade']
    print("nome: "+nome)
    print("descricao: "+descricao)
    print("pontuacao: "+pontuacao)
    print("data final entrega: "+data_entrega)
    print("tipo_atividade: "+tipo_atividade)
    atividade = Atividade(nome=nome,descricao=descricao,pontuacao=pontuacao,data_final=data_entrega,tipo=tipo_atividade)
    salaDAO = SalaDAO()
    sala = salaDAO.recuperaSala(id_sala)
    sala.atividades.append(atividade)
    salaDAO.adicionarSala(sala)
    
    return redirect(url_for('professor.carregar_sala',id=id_sala))

@professor.route("/excluir_atividade/<int:id_sala>/<int:id_atividade>")
def excluir_atividade(id_sala,id_atividade):
    print("Excluir atividade.")
    atividadeDAO = AtividadeDAO() 
    atividadeDAO.remove_atividade(id_atividade)
    
    return redirect(url_for('professor.carregar_sala',id=id_sala))

@professor.route("/avaliar_atividade/<int:id_atividade>")
def avaliar_atividade(id_atividade):
    atividadeDAO = AtividadeDAO()
    atividade_selecionada = atividadeDAO.recupera_atividade(id_atividade)
    return render_template("avaliacao_da_atividade.html",atividade_selecionada=atividade_selecionada)

@professor.route("/atribuir_nota/<int:id_resposta>",methods=['POST'])
def atribuir_nota(id_resposta):
    print("Foi até aqui")
    respostaDAO = RespostaDAO()
    resposta_selecionada = respostaDAO.recupera_resposta(id_resposta)
    resposta_selecionada.pontuacao_recebida = request.form['nota']
    respostaDAO.grava_resposta(resposta_selecionada)
    atividadeDAO = AtividadeDAO()
    
    atividade_selecionada = atividadeDAO.recupera_atividade(resposta_selecionada.atividade.id)
    return render_template("avaliacao_da_atividade.html",atividade_selecionada=atividade_selecionada)

@professor.route("/tela_editar_sala/<id_sala>")
def tela_editar_salas(id_sala):
    salaDAO = SalaDAO()
    sala_recuperada = salaDAO.recuperaSala(id_sala)
    return render_template("editar_sala.html",sala_selecionada=sala_recuperada)

@professor.route("/editar_sala/<id_sala>",methods=['POST'])
def editar_sala(id_sala):
    print("Editar Sala.")
    salaDAO = SalaDAO()
    sala_recuperada = salaDAO.recuperaSala(id_sala)

    logo = request.files['logo']
    if(logo.filename == ""):
        dataSave = ""
        enderecoArquivo=sala_recuperada.logo
    else:    
        dataSave = datetime.datetime.now().strftime('%d%m%Y%H%M%S')
        print(dataSave)
        logo.save(f'logos/{dataSave}_{logo.filename}')
        enderecoArquivo = dataSave+'_'+logo.filename
    
    
    sala_recuperada.nome = request.form['nome_sala']
    sala_recuperada.descricao = request.form['descricao']
    sala_recuperada.logo=enderecoArquivo
    salaDAO.editarSala(sala_recuperada)
    return redirect(url_for('professor.principal'))

@professor.route("/tela_editar_atividade/<id_atividade>")
def tela_editar_atividade(id_atividade):
    atividadeDAO = AtividadeDAO()
    atividade_recuperada = atividadeDAO.recupera_atividade(id_atividade)
    return render_template("editar_atividade.html",atividade_selecionada=atividade_recuperada)

@professor.route("/editar_atividade/<int:id_atividade>",methods=['POST'])
def editar_atividade(id_atividade):
    print("Editar atividade.")

    atividadeDAO = AtividadeDAO()
    atividade = atividadeDAO.recupera_atividade(id_atividade)

    nome=request.form['nome_atividade']
    descricao=request.form['descricao']
    pontuacao=request.form['pontuacao']
    data_entrega=request.form['data_entrega']
    tipo_atividade=request.form['tipo_atividade']
    print("nome: "+nome)
    print("descricao: "+descricao)
    print("pontuacao: "+pontuacao)
    print("tipo_atividade: "+tipo_atividade)
    
    atividade.nome = nome
    atividade.descricao = descricao
    atividade.data_final = data_entrega
    atividade.pontuacao = pontuacao
    atividade.tipo = tipo_atividade

    atividadeDAO.salvar_atividade()    
    return redirect(url_for('professor.carregar_sala',id=atividade.sala_id))

@professor.route("/excluir_resposta/<int:id_atividade>/<int:id_resposta>")
def excluir_resposta(id_atividade,id_resposta):
    print("Excluir Resposta.")
    respostaDAO = RespostaDAO() 
    respostaDAO.remove_resposta(id_resposta)
    return redirect(url_for('professor.avaliar_atividade',id_atividade=id_atividade))

@professor.route("/download_resposta/<int:id_resposta>")
def download_resposta(id_resposta):
    
    respostaDAO = RespostaDAO()
    resposta = respostaDAO.recupera_resposta(id_resposta)
    arquivo_path = 'respostas\\'+resposta.resposta

    return send_file(arquivo_path, as_attachment=True)
