class Sala():
    def __init__(self,id="",nome="", descricao="",logo="",atividades=[],participantes=[]):
        self.__id = id
        self.__nome = nome
        self.__logo = logo
        self.__descricao = descricao
        self.__atividades = atividades
        self.__participantes = participantes
    
    def getId(self):
        return self.__id

    def getNome(self):
        return self.__nome

    def getDescricao(self):
        return self.__descricao
    
    def getLogo(self):
        return self.__logo

    def getAtividades(self):
        return self.__atividades
    
    def getParticipantes(self):
        return self.__participantes
    
