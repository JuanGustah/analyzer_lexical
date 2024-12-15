import lexer
import parser

if __name__ == "__main__":
    lexer = lexer.Lexer("code.alt.meme")
    lexer.start()
    #lexer.display_tokens()

    parser = parser.Parser(lexer.tokens)
    parser.start()