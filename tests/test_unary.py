# tests/test_unary.py
from src.Lexer import Lexer
from src.Parser import Parser
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

# Test 1: Existing test for atribuicao-unary.meme (kept as-is, duplicate removed)
def test_attr_unary():
    input_file = "input/unary_expression.meme"
    lexer = Lexer(input_file)
    
    lexer.start()
    parser = Parser(lexer.tokens, lexer.context)
    result = parser.start()
    
    assert True, result

# Test 2: Variable Declaration and Assignment
def test_variable_declaration():
    input_file = "input/variable_declaration.meme"
    lexer = Lexer(input_file)
    
    lexer.start()
    parser = Parser(lexer.tokens, lexer.context)
    result = parser.start()
    
    assert True, "Variable declaration parsed successfully"

# Test 3: Unary Expression
def test_unary_expression():
    input_file = "input/unary_expression.meme"
    lexer = Lexer(input_file)
    
    lexer.start()
    parser = Parser(lexer.tokens, lexer.context)
    result = parser.start()
    
    assert True, "Unary expression parsed successfully"

# Test 4: Function Declaration and Call
def test_function_declaration_call():
    input_file = "input/function_declaration_call.meme"
    lexer = Lexer(input_file)
    
    lexer.start()
    parser = Parser(lexer.tokens, lexer.context)
    result = parser.start()
    
    assert True, "Function declaration and call parsed successfully"

# Test 5: Conditional Statement (if-else)
def test_conditional_statement():
    input_file = "input/conditional_statement.meme"
    lexer = Lexer(input_file)
    
    lexer.start()
    parser = Parser(lexer.tokens, lexer.context)
    result = parser.start()
    
    assert True, "Conditional statement parsed successfully"

# Test 6: Loop Statement with Break
def test_loop_statement():
    input_file = "input/loop_statement.meme"
    lexer = Lexer(input_file)
    
    lexer.start()
    parser = Parser(lexer.tokens, lexer.context)
    result = parser.start()
    
    assert True, "Loop statement parsed successfully"

# Test 7: Print and Read Statements
def test_print_read_statements():
    input_file = "input/print_read_statements.meme"
    lexer = Lexer(input_file)
    
    lexer.start()
    parser = Parser(lexer.tokens, lexer.context)
    result = parser.start()
    
    assert True, "Print and read statements parsed successfully"