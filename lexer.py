import re

# Constantes para identificação de padrões
DIGIT = r'[0-9]'
WORD = r'[a-zA-Z0-9_]'
RESERVED_WORDS = {
    'meme', 'int', 'bruh', 'hora_do_show', 'irineu_voce_sabe',
    'suprise_mtfk', 'here_we_go_again', 'amostradinho',
    'casca_de_bala', 'receba', 'papapare', 'ate_outro_dia',
    'real', 'barça', 'and', 'or'
}

class Lexer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tokens = []
        self.current_word = ''
        self.line_number = 0
        self.head_position = 0
        self.line = ''

    def start(self):
        with open(self.file_path, 'r') as file:
            for self.line_number, line in enumerate(file, start=1):
                self.line = line.strip()
                self.head_position = 0
                self.processar_linha()

    def processar_linha(self):
        while self.head_position < len(self.line):
            if not self.q0():
                char = self.line[self.head_position]
                raise ValueError(f"Caractere inválido '{char}' na linha {self.line_number}.")
            
    def verificar_space_tab(self, char):
        return char in {' ', '\t'}
    
    def q0(self):
        char = self.current_char()
        if char is None:
            return False

        if char in {'!'}:
            self.forward_head()
            return self.q05()
        elif char in {'='}:
            self.forward_head()
            return self.q06()
        elif char in {'<'}:
            self.forward_head()
            return self.q07()
        elif char in {'>'}:
            self.forward_head()
            return self.q08()
        elif char in {'+'}:
            self.forward_head()
            return self.q09()
        elif char == '(': 
            self.forward_head() 
            return self.q10() 
        elif char == ')': 
            self.forward_head() 
            return self.q11() 
        elif char == '{': 
            self.forward_head() 
            return self.q12() 
        elif char == '}': 
            self.forward_head() 
            return self.q13() 
        elif char == ';': 
            self.forward_head() 
            return self.q14() 
        elif char == '/': 
            self.forward_head() 
            return self.q15() 
        elif char == '-': 
            self.forward_head() 
            return self.q16() 
        elif char == '*': 
            self.forward_head() 
            return self.q17()
        elif re.match(DIGIT, char):
            self.current_word = char
            self.forward_head()
            return self.q03()
        elif re.match(WORD, char):
            self.current_word = char
            self.forward_head()
            return self.q01()
        elif self.verificar_space_tab(char):
            self.forward_head()
            return True
        return False

    def q01(self):
        while (char := self.current_char()) and re.match(WORD, char):
            self.current_word += char
            self.forward_head()
        return self.q02()

    def q02(self):
        token_type = self.get_reserved_or_id(self.current_word)
        current_word = self.current_word if token_type == "id" else None

        self.add_token(token_type, current_word)
        self.current_word = ''

        return True

    def q03(self):
        while (char := self.current_char()) and re.match(DIGIT, char):
            self.current_word += char
            self.forward_head()
        return self.q04()

    def q04(self):
        self.add_token('number', self.current_word)
        self.current_word = ''
        return True
        
    def q05(self):
        char = self.current_char()
        if char == '=':
            self.forward_head()
            self.add_token('!=')
        else:
            self.add_token('!')
        return True
        
    def q06(self):
        char = self.current_char()
        if char == '=':
            self.forward_head()
            self.add_token('==')
        else:
            self.add_token('=')
        return True
    
    def q07(self):
        char = self.current_char()
        if char == '=':
            self.forward_head()
            self.add_token('<=')
        else:
            self.add_token('<')
        return True
    
    def q08(self):
        char = self.current_char()
        if char == '=':
            self.forward_head()
            self.add_token('>=')
        else:
            self.add_token('>')
        return True
    
    def q09(self):
        # char = self.current_char()
        # if char == '+':
        #     self.forward_head()
        #     self.add_token('INCREMENTO', '++')
        # else:
        self.add_token('+')
        return True
    
    def q10(self): 
        self.add_token('(') 
        return True
    
    def q11(self): 
        self.add_token(')') 
        return True
    
    def q12(self): 
        self.add_token('{') 
        return True
    
    def q13(self): 
        self.add_token('}') 
        return True
    
    def q14(self): 
        self.add_token(';') 
        return True
    
    def q15(self): 
        self.add_token('/') 
        return True
    
    def q16(self): 
        self.add_token('-') 
        return True
    
    def q17(self): 
        self.add_token('*') 
        return True
    
    def get_reserved_or_id(self, word):
        return word if word in RESERVED_WORDS else 'id'

    def add_token(self, token_type, value=None):
        self.tokens.append(([token_type, value], self.line_number))

    def current_char(self):
        return self.line[self.head_position] if self.head_position < len(self.line) else None

    def forward_head(self):
        self.head_position += 1

    def display_tokens(self):
        print("\nTokens:")
        for token in self.tokens:
            print(token)
