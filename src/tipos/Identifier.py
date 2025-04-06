class Identifier:
    def __init__(self, cod, nome, linha, coluna, tipo=None):
        self.cod:       int = cod
        self.nome:      str = nome
        self.linha:     int = linha
        self.coluna:    int = coluna
        self.tipo:      str = tipo
        
    def __str__(self):
        return f"Identifier(cod={self.cod}, nome='{self.nome}', linha={self.linha}, coluna={self.coluna}, tipo={self.tipo})"