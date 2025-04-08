from typing import List, Optional
from tabulate import tabulate

from tipos import Identifier, Tipo, Token

class SymbolTable:
    def __init__(self):
        self.table: List[Identifier] = []

    def add(self, registro: Identifier) -> Optional[Identifier]:
        if registro:
            self.table.append(registro)
            return registro
        
        return None
    
    def removeByCod(self, cod: int):
        for idx, item in enumerate(self.table):
            if item.cod == cod:
                del self.table[idx]
                break
                 
        
    def findByCod(self, cod: int) -> Optional[Identifier]:
        for i in self.table:
            if cod == i.cod:
                return i
            
        return None
    
    def lookup(self, nome: str) -> Optional[Identifier]:
        for i in self.table:
            if nome == i.nome:
                return i
            
        return None

    def setReg(self, reg: Identifier) -> bool:
        for idx, i in enumerate(self.table):
            if reg.nome == i.nome:
                self.table[idx].coluna = reg.coluna
                self.table[idx].linha = reg.linha
                self.table[idx].nome = reg.nome
                self.table[idx].tipo = reg.tipo
                return True
            
        return False
    
    def addParam(self, func, param, paramType):
        for i in self.table:
            if func == i.nome:
                i.params.append((paramType, param))
                return i
        

    def list(self):
        headers = ["Indice", "Lexema", "Linha", "Coluna", "Tipo", "Params"]
        data = [[symbol.cod, symbol.nome, symbol.linha, symbol.coluna, symbol.tipo, symbol.params] for symbol in self.table]
        print("\nTabela de Símbolos:")
        print(tabulate(data, headers=headers, tablefmt="grid"))