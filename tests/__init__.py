import os
import pytest

from src.Lexer import Lexer
from src.Parser import Parser

# Lista de tuplas (nome_arquivo, resultado_esperado)
test_cases = [
    ("input/atribuicao.meme", True),
]

@pytest.mark.parametrize("filename,expected", test_cases)
def test_parser(filename, expected):

    try:
        lexer = Lexer("input/input.meme")
        lexer.start()
        parser = Parser(lexer.tokens, lexer.context)
        
        parser.start()
        result = True
    except Exception as e:
        print(e)
        result = False

    assert result == expected
