from typing import List
from tabulate import tabulate

from tipos import Identifier

class SymbolTable:
    def __init__(self):
        self.table: List[Identifier] = []

    def add(self, registro: Identifier):
        if registro:
            self.table.append(registro)
            return registro
        
        return None
    
    def lookup(self, nome: str):
        for i in self.table:
            if nome == i.nome:
                return i
            
        return None

    
    def setType(self, cod, newType):
        for i in self.table:
            if cod == i.nome:
                i.tipo = newType
                return True
            
        return False

    def list(self):
        headers = ["Indice", "Lexema", "Linha", "Coluna", "Tipo"]
        data = [[symbol.cod, symbol.nome, symbol.linha, symbol.coluna, symbol.tipo] for symbol in self.table]
        print("\nTabela de Símbolos:")
        print(tabulate(data, headers=headers, tablefmt="grid"))