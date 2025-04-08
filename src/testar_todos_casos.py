import os
import logging
from Lexer import Lexer
from Parser import Parser

# Configuração básica de logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[logging.StreamHandler()]
)

def test_files():
    input_dir = "input"
    passed = 0
    total = 0

    # Lista todos os arquivos .meme no diretório de input
    for filename in os.listdir(input_dir):
        if filename.endswith(".meme"):
            total += 1
            filepath = os.path.join(input_dir, filename)
            print(f"\n--- Testando: {filename} ---")

            try:
                # Processa cada arquivo
                lexer = Lexer(filepath)
                lexer.start()
                
                parser = Parser(lexer.tokens, lexer.context)
                success = parser.start()
                
                if success:
                    print(f"\033[92m[OK] {filename} passou!\033[0m")
                    passed += 1
                else:
                    print(f"\033[91m[FALHOU] {filename} teve erros de parsing\033[0m")

            except Exception as e:
                print(f"\033[91m[ERRO] {filename} falhou:\033[0m")
                print(f"→ {str(e)}")

    print(f"\nResultado: {passed}/{total} arquivos passaram")

if __name__ == "__main__":
    test_files()