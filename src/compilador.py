from Lexer import Lexer
from Parser import Parser

if __name__ == "__main__":
    lexer = Lexer("input/input.meme")
    lexer.start()
    #lexer.display_tokens()
    #lexer.context.list_symbols()
    lexer.context.context_hierarchy(lexer.context)
    #print('Leitura no Parser')
    parser = Parser(lexer.tokens, lexer.context)
    parser.start()

    #lexer.display_symbol_table()

    # parser.print_all()