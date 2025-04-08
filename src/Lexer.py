import re

from typing import List
from tabulate import tabulate

from tipos import Identifier, Token, Context

# Constantes para identificação de padrões
DIGIT = r'[0-9]'
WORD = r'[a-zA-Z0-9_]'
RESERVED_WORDS = {
    'meme', 'int', 'bruh', 'hora_do_show', 'irineu_voce_sabe', 
    'suprise_mtfk', 'here_we_go_again', 'amostradinho',
    'casca_de_bala', 'receba', 'papapare', 'ate_outro_dia',
    'real', 'barca', 'and', 'or', 'nem_eu', 'void'
}

class Lexer:
    def __init__(self, file_path):
        self.file_path:                 str         = file_path
        self.tokens:                    List[Token] = []
        self.current_word:              str         = ''
        self.line_number:               int         = 0
        self.head_position:             int         = 0
        self.line:                      str         = ''
        self.context:                   Context     = Context('global')
        self.next_context_to_create:    str         = ''

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
            new_context = self.next_context_to_create 
            
            if not new_context: 
                return
                
            new_context = self.context.generate_unique_name(new_context)
            
            self.context.add_subcontext(new_context)
            self.context = self.context.get_subcontext(new_context)
            ## Pegar o identificador mais proximo anterior
            self.next_context_to_create = None
            
            self.forward_head() 
            return self.q12() 
        elif char == '}':
            self.context = self.context.parent 
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
        elif char == ',': 
            self.forward_head() 
            return self.q18()
        elif char == "#":
            self.forward_head() 
            return self.q19()
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
        token_lexema = self.current_word
        current_word = self.current_word if token_type == "id" else None
            
        if token_lexema in ['meme', 'hora_do_show', 'irineu_voce_sabe', 'nem_eu', 'surprise_mtfk', 'here_we_go_again']:
            self.next_context_to_create = token_lexema

        self.add_token(token_type, self.current_word, current_word)
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
            self.add_token('!=', '!=')
        else:
            self.add_token('!', '!')
        return True
        
    def q06(self):
        char = self.current_char()
        if char == '=':
            self.forward_head()
            self.add_token('==', '==')
        else:
            self.add_token('=', '=')
        return True
    
    def q07(self):
        char = self.current_char()
        if char == '=':
            self.forward_head()
            self.add_token('<=', '<=')
        else:
            self.add_token('<', '<')
        return True
    
    def q08(self):
        char = self.current_char()
        if char == '=':
            self.forward_head()
            self.add_token('>=', '>=')
        else:
            self.add_token('>', '>')
        return True
    
    def q09(self):
        # char = self.current_char()
        # if char == '+':
        #     self.forward_head()
        #     self.add_token('INCREMENTO', '++')
        # else:
        self.add_token('+', '+')
        return True
    
    def q10(self): 
        self.add_token('(', '(') 
        return True
    
    def q11(self): 
        self.add_token(')', ')') 
        return True
    
    def q12(self): 
        self.add_token('{', '{') 
        return True
    
    def q13(self): 
        self.add_token('}', '}') 
        return True
    
    def q14(self): 
        self.add_token(';', ';') 
        return True
    
    def q15(self): 
        self.add_token('/', '/') 
        return True
    
    def q16(self): 
        self.add_token('-', '-') 
        return True
    
    def q17(self): 
        self.add_token('*', '*') 
        return True
    
    def q18(self): 
        self.add_token(',', ',') 
        return True
    
    def q19(self): 
        char = self.current_char()
        while(char != "#"):
            #print("char",char)
            self.forward_head()
            char = self.current_char()

        self.forward_head()
        return True
    
    def get_reserved_or_id(self, word):
        return word if word in RESERVED_WORDS else 'id'
        
    def add_token(self, token_type, lexema=None, value=None):
        # verificar se o token é identificador sim = salvar na tabela de simbolos
        insertedRegCode = None
        if token_type == 'id':
            previousToken = self.look_previous_token()

            register = Identifier(
                self.line_number+self.head_position, 
                lexema, 
                self.line_number, 
                self.head_position, 
                None
            )
            
            inserted_reg = self.context.add_reg(
                register, 
                self.checkIfTokenIdIsForDeclaration(previousToken)
            )

            insertedRegCode = inserted_reg.cod
        
        self.tokens.append(
            Token(
                token_type, 
                lexema, 
                insertedRegCode, 
                self.line_number, 
                self.head_position
            )
        )

    def current_char(self):
        return self.line[self.head_position] if self.head_position < len(self.line) else None

    def forward_head(self):
        self.head_position += 1

    def look_previous_token(self):
        if(self.head_position > 0):
            return self.tokens[-1]
        
    def checkIfTokenIdIsForDeclaration(self, previousToken:Token):
        if(previousToken.lexema == "int" or previousToken.lexema == "bruh"):
            return True
        else:
            return False

    def display_tokens(self):
        print('\t\t\t TOKENS')
        headers = ["Tipo", "Lexema", "Indice", "Linha", "Coluna"]
        table = [
            [token.tipo, token.lexema, token.indice_tabela, token.linha, token.coluna]
            for token in self.tokens
        ]
        print(tabulate(table, headers=headers, tablefmt="grid"))
