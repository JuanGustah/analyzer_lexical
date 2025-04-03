from tabulate import tabulate

# Tabela de símbolos = output
class SymbolTable:
    def __init__(self):
        # Corrigindo a anotação de tipo: de 'dict' para 'list'
        self.table: list = []

    def add(self, id_name: str, linha: int, coluna: int):
        # Adiciona um dicionário com id, linha e coluna
        index = len(self.table)
        self.table.append({'id': id_name, 'linha': linha, 'coluna': coluna})
        return index

    def lookup(self, idx: int):
        # Retorna o dicionário completo ou None se o índice não existir
        if idx < len(self.table):
            return self.table[idx]
        return None

    def list(self):
        headers = ["idx", "id", "linha", "coluna"]
        data = [[i, symbol['id'], symbol['linha'], symbol['coluna']] for i, symbol in enumerate(self.table)]
        print("\nTabela de Símbolos:")
        print(tabulate(data, headers=headers, tablefmt="grid"))