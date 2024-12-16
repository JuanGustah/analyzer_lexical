import lexer
import parser

if __name__ == "__main__":
    lexer = lexer.Lexer("code2.meme")
    lexer.start()
    #lexer.display_tokens()
    #lexer.display_symbol_table()

    print('Leitura no Parser')
    parser = parser.Parser(lexer.tokens,lexer.symbol_table)
    parser.start()