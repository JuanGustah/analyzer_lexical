import re
from symtable import SymbolTable

class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.tokens = []
        self.symbol_table = SymbolTable()
        self.reserved_words = {
            'meme': 'meme', 
            'int': 'int', 
            'bruh': 'bruh', 
            'hora_do_show': 'hora_do_show', 
            'irineu_voce_sabe': 'irineu_voce_sabe', 
            'nem_eu': 'nem_eu',
            'here_we_go_again': 'here_we_go_again', 
            'suprise_mtfk': 'suprise_mtfk', 
            'amostradinho': 'amostradinho', 
            'casca_de_bala': 'casca_de_bala',
            'receba': 'receba', 
            'papapare': 'papapare', 
            'ate_outro_dia': 'ate_outro_dia'
        }
        self.symbols = {
            '{': 'LBRACE', 
            '}': 'RBRACE', 
            '(': 'LPAREN', 
            ')': 'RPAREN',
            '=': 'ASSIGN', 
            ';': 'SEMI', 
            '+': 'PLUS', 
            '-': 'MINUS', 
            '*': 'TIMES',
            '/': 'DIVIDE', 
            ',': 'COMMA', 
            '==': 'EQUALS', 
            '!=': 'NOT_EQUALS',
            '<': 'LT', 
            '<=': 'LE', 
            '>': 'GT', 
            '>=': 'GE', 
            'AND': 'AND', 
            'OR': 'OR'
        }
        self.token_regex = [
            (r'[ \t\n]+', None), 
            (r'//.*', None),  
            (r'\d+', 'NUMBER'),  
            (r'[a-zA-Z_][a-zA-Z0-9_]*', 'ID'),  
            (r'[{}();,+\-*/=<>]', 'SYMBOL'), 
            (r'==|!=|<=|>=|AND|OR', 'SYMBOL') 
        ]

    def tokenize(self):

        lines = self.code.splitlines()

        for num_line, line in enumerate(lines):
            for word in line.split():
                match = None
                for regex, token_type in self.token_regex:
                    match = re.match(regex, word)
                    if match:
                        lexeme = match.group(0)
                        if token_type == 'ID':
                            
                            if lexeme in self.reserved_words:
                                self.tokens.append(('RESERVED', lexeme, num_line))
                            else:
                                self.tokens.append(('ID', lexeme, num_line))
                                # Todo identificador deve estar na tabela de simbolos 
                                if self.symbol_table.lookup(lexeme) is None:
                                    self.symbol_table.add(lexeme, {'type': None, 'line': num_line})
                                    
                        elif token_type == 'NUMBER':
                            self.tokens.append(('NUMBER', lexeme, num_line))
                        elif token_type == 'SYMBOL':
                            self.tokens.append((self.symbols.get(lexeme, 'SYMBOL'), lexeme, num_line))
                        break
                if not match:
                    raise ValueError(f"Token inválido na linha {num_line}: {word}")

    def display_tokens(self):
        print("\nTokens:")
        for token in self.tokens:
            print(token)


# Teste do Lexer
# if __name__ == "__main__":
#     program_code = """
#     meme {
#         int x = 1;
#         int y = 2;
#         irineu_voce_sabe(x == 1) {
#             amostradinho(x + y);
#             x = 15;
#         }
#     }
#     """

#     lexer = Lexer(program_code)
#     lexer.tokenize()
#     lexer.display_tokens()
#     lexer.symbol_table.listar()
