class Sala():
    def __init__(self,id="",nome="", logo="",atividades="",participantes=""):
        self.__id = id
        self.__nome = nome
        self.__logo = logo
        self.__atividades = atividades
        self.__participantes = participantes
    
    def getId(self):
        return self.__id

    def getNome(self):
        return self.__nome
    
    def getLogo(self):
        return self.__logo

    def getAtividades(self):
        return self.__atividades
    
    def getParticipantes(self):
        return self.__participantes
    
