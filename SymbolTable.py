# Tabela de símbolos = output
class SymbolTable:
    def __init__(self):
        self.table: dict = []

    def add(self, attributes: any):
        index=len(self.table)
        self.table.append(attributes)
        return index

    def lookup(self, idx: str):
        return self.table and idx < len(self.table)

    def list(self):
        print("\nTabela de Símbolos:")
        print("idx|id")
        for i in range(len(self.table)):
            print(f"  {i}|{self.table[i]}")