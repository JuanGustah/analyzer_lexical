from Lexer import Lexer
from Parser import Parser

if __name__ == "__main__":
    lexer = Lexer("code3.meme")
    lexer.start()
    #lexer.display_tokens()
    #lexer.display_symbol_table()

    print('Leitura no Parser')
    parser = Parser(lexer.tokens, lexer.symbol_table)
    parser.start()