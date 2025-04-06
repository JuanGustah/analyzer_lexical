from tabulate import tabulate

class SymbolTable:
    def __init__(self):
        self.table: list = [] # identificadores

    def add(self, id_name: str, linha: int, coluna: int):
        index = len(self.table)
        self.table.append({'id': id_name, 'linha': linha, 'coluna': coluna, 'type': None, 'nature': None})
        return index
    
    def return_last_inserted(self):
        return self.table[-1]['id'] 
    
    def lookup(self, idx: int):
        if idx < len(self.table):
            return self.table[idx]
        return None
    
    def setType(self,idx,newType):
        self.table[idx]['type'] = newType

    def setNature(self,idx,newNature):
        self.table[idx]['nature'] = newNature

    def findIdIdx(self, idName):
        for i in range(len(self.table)):
            if self.table[i]['id'] == idName:
                return i
        return None
    
    def list(self):
        headers = ["idx", "id", "linha", "coluna", "type", "nature"]
        data = [[i, symbol['id'], symbol['linha'], symbol['coluna'], symbol['type'], symbol['nature']] for i, symbol in enumerate(self.table)]
        print("\nTabela de Símbolos:")
        print(tabulate(data, headers=headers, tablefmt="grid"))