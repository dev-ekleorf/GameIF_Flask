from Model.Usuario import Usuario
import requests
import json

link = "https://gameif-ekleorf-default-rtdb.firebaseio.com"
    
class UsuarioDAO:

    def __init__(self):
        pass
        
    def listar_usuarios(self):
        requisicao = requests.get(f'{link}/usuarios/.json')
        print(requisicao.json())
        return requisicao
