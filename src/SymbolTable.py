from tabulate import tabulate

class SymbolTable:
    def __init__(self):
        self.table: list = []

    def add(self, id_name: str, linha: int, coluna: int):
        index = len(self.table)
        self.table.append({'id': id_name, 'linha': linha, 'coluna': coluna})
        return index

    def lookup(self, idx: int):
        if idx < len(self.table):
            return self.table[idx]
        return None

    def list(self):
        headers = ["idx", "id", "linha", "coluna"]
        data = [[i, symbol['id'], symbol['linha'], symbol['coluna']] for i, symbol in enumerate(self.table)]
        print("\nTabela de Símbolos:")
        print(tabulate(data, headers=headers, tablefmt="grid"))