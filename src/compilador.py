from Lexer import Lexer
from Parser import Parser

if __name__ == "__main__":
    lexer = Lexer("input/code2.meme")
    lexer.start()
    #lexer.display_tokens()
    lexer.context.list_symbols()
    
    print('Leitura no Parser')
    #parser = Parser(lexer.tokens, lexer.symbol_table)
    #parser.start()

    #lexer.display_symbol_table()

    # parser.print_all()