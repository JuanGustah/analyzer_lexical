class Token:
    def __init__(self, tipo, lexema, indice_tabela, linha, coluna):
        self.tipo:              str = tipo
        self.lexema:            str = lexema
        self.indice_tabela:     int = indice_tabela
        self.linha:             int = linha
        self.coluna:            int = coluna

    
    def __str__(self):
        return f"Token(tipo='{self.tipo}', lexema='{self.lexema}', indice_tabela={self.indice_tabela}, linha={self.linha}, coluna={self.coluna})"