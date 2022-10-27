class Usuario():
    def __init__(self,id="",nome="", senha=""):
        self.__id = id
        self.__nome = nome
        self.__senha = senha
    
    def getId(self):
        return self.__id

    def getNome(self):
        return self.__nome
    
    def getSenha(self):
        return self.__senha