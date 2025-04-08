from Lexer import Lexer
from Parser import Parser

if __name__ == "__main__":
    try:
        lexer = Lexer("input/function_declaration_call.meme")
        lexer.start()
        #lexer.display_tokens()
        #lexer.context.list_symbols()
        #lexer.context.context_hierarchy(lexer.context)
        #print('Leitura no Parser')
        parser = Parser(lexer.tokens, lexer.context)
        
        parser.start()
        parser.generator.print_instructions()
        
        if parser:
            print(f"\033[92m[OK] passou!\033[0m")
        else:
            print(f"\033[91m[FALHOU] teve erros de parsing\033[0m")
        
    except Exception as e:
        print(f"\033[91m[ERRO] falhou:\033[0m")
        print(f"→ {str(e)}")
    