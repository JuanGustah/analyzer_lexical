import re

D = '[0-9]'
W = '[a-zA-Z_]'

class SymbolTable:
    def __init__(self):
        self.table: dict = {}

    def add(self, id: str, attributes: any):
        self.table[id] = attributes

    def lookup(self, id: str):
        return self.table.get(id)

    def update(self, id: str, attributes: any):
        self.table[id].update(attributes)
      
    def listar(self):
        print("\nTabela de Símbolos:")
        for id, attributes in self.table.items():
            print(f"Identificador: {id}")
            for key, value in attributes.items():
                print(f"  {key}: {value}")

def reserved_words(token, word):
    words = ['meme', 'int', 'bruh', 'hora_do_show', 'irineu_voce_sabe', 'suprise_mtfk', 
             'here_we_go_again', 'amostradinho', 'casca_de_bala', 'receba', 'papapare', 'ate_outro_dia', 'real', 'barça']

    if word in words: 
        return (word.upper(), word)  
    else:
        return ('ID', word) 

class Lexer:
    def __init__(self, file_path: str):
        self.file_path = file_path

        # variáveis de controle do Lexer
        self.head_position = 0
        self.num_line = 1
        self.line = ''
        self.symbols_table = SymbolTable()
        # Idealmente uma tupla com token, valor e linha
        self.tokens = []
        self.current_word = ''
        # bootstrap
        self.main_loop()

    def main_loop(self):
        file = open(self.file_path, "r")
        self.line = file.readline()

        # loop principal
        while self.line != "":
            # valida se aquela linha tem que ser analizada (linha em branco) e se já acabou a linha
            self.check_line()

            # Lê linha a linha
            self.line = file.readline()

            # Reseta o cabeçote da máquina pro inicio da nova linha
            self.num_line += 1
            self.head_position = 0

        # Não vazar memória, se bem que é python e esse lixo vaza de toda forma
        file.close()
    
    def read_actual_char(self):
        """Lê o caractere atual, pulando espaços e tabulações."""
        #while (
        #    self.head_position < len(self.line) and
        #    self.line[self.head_position] in {' ', '\t'}
        #):
        self.forward_head()
        if self.head_position < len(self.line):
            return self.line[self.head_position]
        return None  # Retorna None se atingir o final da entrada

    def forward_head(self):
        self.forward_head()
    
    def check_line(self):
        # Valida se não chegou ao fim da linha
        while(self.head_position < len(self.line) and self.read_actual_char() != '\n'):
            # Valida se ele reconheceu algum lexema
            if not self.q0():
                raise ValueError(f"Token inválido na linha {self.num_line}:{self.line[self.head_position]}")

    def q0(self):
        char = self.read_actual_char()
        if char is None:
            return False
        
        if re.match(W, char):
            self.current_word = char
            self.forward_head()
            return self.q1()
        elif re.match(D, char):
            self.current_word = char
            self.forward_head()
            return self.q3()
        elif char == '(':
            self.forward_head()
            return self.q90()
        elif char == ')':
            self.forward_head()
            return self.q91()
        elif char == '{':
            self.forward_head()
            return self.q92()
        elif char == '}':
            self.forward_head()
            return self.q93()
        elif char == '=':
            self.forward_head()
            return self.q94()
        elif char == ';':
            self.forward_head()
            return self.q95()
        
        elif char in ' \t':
            self.forward_head()
            return True
        else:
            return False

    def q1(self):
        char = self.read_actual_char()

        if re.match(W, char):
            self.forward_head()
            self.current_word += char
            return self.q1()
        else:
            return self.q2()
    
    def q2(self):
        token, word = reserved_words('ID', self.current_word) 
        self.tokens.append((token, word, self.num_line))
        self.current_word = '' 
        #self.current_word = '' return True
        #self.tokens.append(('WORD', self.num_line))
        return True
    
    def q3(self):
        char = self.read_actual_char()

        if re.match(D, char):
            self.forward_head()
            self.current_word += char
            return self.q3()
        else:
            return self.q4()
        
    def q4(self):
        self.tokens.append(('NUMBER', self.current_word, self.num_line))
        return True
    
    def q90(self):
        self.tokens.append(('(', self.num_line))
        return True
    
    def q91(self):
        self.tokens.append((')', self.num_line))
        return True
    
    def q92(self):
        self.tokens.append(('{', self.num_line))
        return True
    
    def q93(self):
        self.tokens.append(('}', self.num_line))
        return True
    
    def q94(self):
        self.tokens.append(('=', self.num_line))
        return True
    
    def q95(self):
        self.tokens.append((';', self.num_line))
        return True
    
    def display_tokens(self):
        print("\nTokens:")
        for token in self.tokens:
            print(token)

# Teste do Lexer
if __name__ == "__main__":
    analisador_lexico = Lexer("code.meme")
    analisador_lexico.display_tokens()
