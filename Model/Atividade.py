class Atividade():
    def __init__(self,id="",nome="", descricao="",tipo=""):
        self.__id = id
        self.__nome = nome
        self.__descricao = descricao
        self.__tipo = tipo
  
    
    def getId(self):
        return self.__id

    def getNome(self):
        return self.__nome
    
    def getDescricao(self):
        return self.__descricao
    
    def getTipo(self):
        return self.__tipo   
