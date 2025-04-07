import logging
from functools import wraps
from typing import List

from CodeGenerator import CodeGenerator
from tipos import Context, Nature, Tipo, Token

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [INFO] - %(message)s',
        handlers=[logging.StreamHandler()]
)

class ContextMetadata:
    def __init__(self, nature, alias = None):
        self.nature = nature
        self.alias = alias



class Parser:
    def __init__(self, tokens, context):
        self.tokens:            List[Token] = tokens
        self.global_context:    Context = context
        self.current_context:   Context = context
        self.next_context:      Context = None
        self.actualTokenPos:    int = -1
        self.actualToken:       Token = None
        self.generator:         CodeGenerator = CodeGenerator()
        self.logs:              bool = False
        
    def match(self, match):
        if self.actualToken is None:
            return False
        
        tipo = self.actualToken.tipo

        if(tipo == 'id' and match == 'id'):
            # idIndex = self.actualToken[1]
            # if(self.current_context.symbol_table.lookup(idIndex)):
            return True
        elif(tipo == 'number' and match == 'number'):
            value = self.actualToken.lexema
            if(value is not None):
                return True
            return True
        elif(tipo == match):
            return True
        return False
    
    
    def getNextToken(self): 
        if self.actualTokenPos + 1 < len(self.tokens):
            self.actualTokenPos += 1
            self.actualToken = self.tokens[self.actualTokenPos]
            print('\n')
            logging.info(f"Obtendo próximo token (index={self.actualTokenPos}): '{self.actualToken}'")
        else:
            self.actualToken = None
            logging.info(f'Sem tokens para leitura')
    
    
    def start(self):
        try:

            if self.program():
                logging.info("\033[92m[ok] Execução bem-sucedida: Deu bom!\033[0m")  
                self.generator.print_instructions()
                return True
            else:
                
                logging.info("\033[91m[err] :Execução falhou:\033[0m")
                logging.info(f"\033[91m[err] :{self.actualToken}\033[0m")  
                return False
        except Exception as e:
            print(e)

    # ================= Descrição BNF da Linguagem Simplificada ===================================== #
    
    
    def program(self):
        self.getNextToken()
        
        logging.info(f'Program')
        
        if self.checkType() or self.match('void'):
            self.subRoutineStep()
            # if self.subRoutineStep():
                # self.getNextToken()
                # continue
            # else:
                
            #     return False  

        self.mainBody()

        return True

    
    def mainBody(self):
        logging.info(f'mainBody')
        if(self.match("meme")):
            self.next_context = 'meme'
            self.getNextToken()

            return self.body()
            
        
        self.throwSyntaxError()
    
    
    def body(self, metadata: ContextMetadata = None):
        logging.info(f'Body')
        if(self.match("{")):
            if self.next_context:
                next_c = self.current_context.get_subcontext(f"{self.current_context.parser_counter}_{self.next_context}")
                next_c.parent.parser_counter += 1

                if next_c:
                    if(metadata):
                        next_c.nature = metadata.nature
                        next_c.alias = metadata.alias
                    self.current_context = next_c
            
            self.getNextToken()

            if(self.checkType()):
                self.declarationVariableStep()
                    
                # while self.checkType():
                #     if self.declarationVariableStep():
                #         pass
                #     else:
                #         return False

            if self.hasStatement():
                self.statements()

                if self.match("}"):
                    self.current_context = self.current_context.parent
                    return None
            
            self.throwSyntaxError()
            # if(self.statements()):
            #     if(self.match("}")):
            #         return True
            # else:
            #     return False
        self.throwSyntaxError()

    
    def subRoutineStep(self):
        logging.info(f'subRoutineStep')      
        if(self.match('void')):
            self.declarationProcedure()
        elif(self.checkType()):
            self.declarationFunction()

        if(self.checkType() or self.match('void')):
            self.subRoutineStep()
        # if self.declarationFunctionProcedure():
        #     return True
        
        # return False
    
    
    def declarationVariableStep(self):
        logging.info(f'declarationVariableStep')
        self.declarationVariable()

        if(self.checkType()):
            self.declarationVariableStep()
    
    
    def callParameters(self):
        logging.info(f'callParameters')
        typeFirstExpression, temp = self.expression()

        self.getNextToken()
        
        if(self.match(',')):
            self.getNextToken()
            self.declarationVariableStep()
        
    
    # ==================================== DECLARAÇÕES =============================================== #
    def checkType(self):
        logging.info(f'tipo de token: {self.actualToken.lexema} == (int/bruh)')
        if(self.match("int")):
            return Tipo.INT
        elif(self.match("bruh")):
            return Tipo.BRUH
        
        return False
    
    
    def type(self):
        logging.info(f'verificando tipo de : {self.actualToken.lexema} == (int/bruh)')
        if(self.match("int")):
            return Tipo.INT
        elif(self.match("bruh")):
            return Tipo.BRUH
        
        self.throwSemanticError()
    
    
    def declarationVariable(self):
        logging.info(f'declarationVariable')
        declarationVariableType = self.checkType()
        if declarationVariableType: 
            
            self.getNextToken()  

            if self.identifier(declarationVariableType):
                #self.checkIdDuplicated(self.actualToken)
                idToken = self.actualToken
                self.getNextToken()  

                if self.match("="):
                    # if self.assignStatement(): 

                    typeAssignment, temp = self.assignStatement()

                    if(typeAssignment != declarationVariableType):
                        self.throwSemanticError()

                    self.generator.emit(f"{idToken.lexema} = {temp}")
                    #self.setIdType(idToken, typeAssignment)

                    if self.match(";"):
                        self.getNextToken()  

                    return None

                if self.match(";"):
                    self.setIdType(idToken, declarationVariableType)

                    if(declarationVariableType == Tipo.BRUH):
                        self.generator.emit(f"{idToken.lexema} = barca") #default value
                    elif(declarationVariableType == Tipo.INT):
                        self.generator.emit(f"{idToken.lexema} = 0")


                    self.getNextToken()  
                    return None
            # return False
        # return False
    
    
    def declarationParameters(self):
        logging.info(f'declarationParameters')
        tipo_variavel = self.checkType()
        if(tipo_variavel):
            self.getNextToken()
            
            if(self.identifier(tipo_variavel)):
                self.getNextToken()
            else:
                self.throwSyntaxError()
                
            if(self.match(',')):
                self.getNextToken()

                if(self.checkType()):
                    return self.declarationParameters()
                self.throwSyntaxError()
            else:
                return None
    
    
    def declarationFunction(self):
        logging.info(f'declarationFunction')
        tipo = self.checkType()
        if tipo:  
            self.getNextToken()
            if self.match('hora_do_show'):
                self.getNextToken()
                if self.identifier(tipo):
                    funcName = self.actualToken.lexema

                    #adicionar tipo de retorno da tabela de simbolos do id da função (global)
                    self.setIdType(self.actualToken, Tipo.INT, self.global_context)

                    self.next_context = "hora_do_show" 

                    self.getNextToken()
                    if self.match('('):  
                        self.getNextToken()

                        self.declarationParameters()

                        if self.match(')'): 
                            self.getNextToken()

                            self.body(ContextMetadata(Nature.FUNC, funcName))
                            
                            self.getNextToken()

                            return None
                            
        self.throwSyntaxError()

    
    def declarationProcedure(self):
        logging.info(f'declarationProcedure')
        if self.match("void"):
            self.getNextToken()
            if self.match('hora_do_show'):
                self.getNextToken()
                if self.identifier():
                    self.next_context = "hora_do_show"
                    self.getNextToken()
                    if self.match('('):  
                        self.getNextToken()

                        self.declarationParameters()

                        if self.match(')'):  
                            self.getNextToken()

                            self.body(ContextMetadata(Nature.PROC))
                            
                            self.getNextToken()

                            return None
                            
        self.throwSyntaxError()
    
    # ==================================== COMANDOS =============================================== #
    
    # 
    #def statements(self):
    #     if(self.statement()):
    #         hasStatementsLeft = True
    #         while(hasStatementsLeft):
    #             self.getNextToken()
                
    #             if(self.match(";")):
    #                 self.getNextToken()
                    
    #                 if(self.match("}")):
    #                     return True
                    
    #                 if not self.statement():
    #                     return False
    #             else:
    #                 hasStatementsLeft = False
    #         return True
    #     return False

    
    def statements(self):
        #adicionar validação para return/receba e chamada de função
        typeStatement = self.statement()

        print('BESTEIRAAa')
        
        if self.hasStatement():
            self.statements()

    
    def hasStatement(self):
        if(self.match("irineu_voce_sabe")):
            return True
        elif(self.match("here_we_go_again")):
            return True
        elif(self.match("amostradinho")):
            return True
        elif(self.match("casca_de_bala")):
            return True
        elif(self.match("receba")):
            #deve validar se está em contexto de função
            if(self.current_context.nature != Nature.FUNC):
                self.throwSemanticError()
                return False
            
            return True
        elif(self.match("papapare")):
            if(self.current_context.nature != Nature.LOOP):
                self.throwSemanticError()
                return False

            return True
        elif(self.match("ate_outro_dia")):
            if(self.current_context.nature != Nature.LOOP):
                self.throwSemanticError()
                return False

            return True
        elif(self.match("id")):
            return True
        return False
    
    
    def statement(self):
        if(self.match("papapare") or self.match("ate_outro_dia")):
            return self.jumpStopStatement()
        elif(self.match("irineu_voce_sabe")):
            return self.conditionStatement()
        elif(self.match("here_we_go_again")):
            return self.loopStatement()
        elif(self.match("amostradinho")):
            return self.printStatement()
        elif(self.match("casca_de_bala")):
            return self.readStatement()
        elif(self.match("receba")):
            return self.returnStatement()
        elif(self.match("id")):
            #falta finalizar a parte de chamada de função
            return self.callOrAssignStatement()

        self.throwSyntaxError()

        # if(self.jumpStopStatement()):
        #     return True
        # if(self.conditionStatement()):
        #     return True
        # elif(self.loopStatement()):
        #     return True
        # elif(self.printStatement()):
        #     return True
        # elif(self.readStatement()):
        #     return True
        # elif(self.callOrAssignStatement()):
        #     return True
        # elif(self.returnStatement()):
        #     return True
        # return False
    
    
    def conditionStatement(self):
        logging.info(f'conditionStatement')
        if(self.match("irineu_voce_sabe")):
            self.getNextToken()

            if(self.match("(")):
                self.getNextToken()

                expressionType, temp = self.expression()
                # if(self.expression()):

                # irineu_voce_sabe (x == 2) - comparar inteiros
                # if(expressionType != Tipo.BRUH):
                #     self.throwSemanticError()

                if(self.match(")")):
                    self.getNextToken()
                    
                    label_else = self.generator.gen_label()
                    label_end = self.generator.gen_label()
                    print(f"CIMAAAAAAAA if {temp} goto {label_else}")
                    #self.generator.emit(f"if {temp} == 0 goto {label_else}")
                    self.generator.emit(f"if {temp} goto {label_else}")
                    
                    self.next_context = "irineu_voce_sabe"
                    self.body()
                    
                    self.generator.emit(f"goto {label_end}")
                    self.generator.emit(f'{label_else}:')
                    
                    # if():
                    self.getNextToken()

                    # if(self.lookAhead("nem_eu")):
                    if(self.match("nem_eu")):
                        self.getNextToken()

                        self.next_context = "nem_eu"
                        self.body()
                        
                        self.generator.emit(f'{label_end}')
                        
                        # if():
                        return None

                    return None
        self.throwSyntaxError()
    
    
    def loopStatement(self):
        logging.info(f'loopStatement')
        if(self.match("here_we_go_again")):
            self.getNextToken()

            if(self.match("(")):
                
                label_start = self.generator.gen_label()
                label_end = self.generator.gen_label()
                self.generator.emit(f'{label_start}:')

                self.getNextToken()
                
                expressionType, temp = self.expression()
                # To testando here_we_go_again (x > 0) isso eé bruh 
                # if(expressionType != Tipo.BRUH):
                #     self.throwSemanticError()

                if(self.match(")")):
                    
                    #self.generator.emit(f'if {temp} == 0 goto {label_end}')
                    self.generator.emit(f'if {temp} goto {label_end}')
                    
                    self.getNextToken()

                    # if():
                    self.next_context = "here_we_go_again"
                    self.body(ContextMetadata(Nature.LOOP))
                    
                    self.generator.emit(f'goto {label_start}')
                    self.generator.emit(f'{label_end}:')
                    self.getNextToken()

                    return None
                        
        self.throwSyntaxError()
    
    
    def jumpStopStatement(self):
        logging.info(f'jumpStopStatement')
        if(self.match("papapare")):
            self.getNextToken()

            if(self.match(";")):
                self.getNextToken()
                return None
        if(self.match("ate_outro_dia")):
            self.getNextToken()

            if(self.match(";")):
                self.getNextToken()
                return None
        
        self.throwSyntaxError()
    
    
    def printStatement(self):
        logging.info(f'printStatement')
        if(self.match("amostradinho")):
            self.getNextToken()

            if(self.match("(")):
                self.getNextToken()
                
                typeExpression, temp = self.expression()
                
                self.generator.emit(f"print {temp}")

                if(self.match(")")):
                    self.getNextToken()

                    if(self.match(";")):
                        self.getNextToken()
                        return None
        self.throwSyntaxError()
    
    
    def readStatement(self):
        logging.info(f'readStatement')
        if(self.match("casca_de_bala")):
            self.getNextToken()

            if(self.match("(")):
                self.getNextToken()

                if(self.identifier()):
                    token = self.actualToken
                    self.checkIfIsDeclared(self.actualToken)

                    self.generator.emit(f'read {token.lexema}')
                    
                    self.getNextToken()
                    
                    if(self.match(")")):
                        self.getNextToken()

                        if(self.match(";")):
                            self.getNextToken()
                            return None
                        
        self.throwSyntaxError()
    
    
    def returnStatement(self):
        logging.info(f'returnStatement')
        if(self.match("receba")):
            self.getNextToken()

            typeReturnExpresison, temp = self.expression()
            
            funcName = self.current_context.alias
            funcSymbolTable = self.global_context.symbol_table.lookup(funcName)

            if(typeReturnExpresison != funcSymbolTable.tipo):
                self.throwSemanticError()

            # if(self.expression()):

            if(self.match(";")):
                self.getNextToken()
            
            return typeReturnExpresison
                
        self.throwSyntaxError()
    
    
    def callOrAssignStatement(self):
        """
            <call-or-assign-statement> ::= 
            <identifier> ( <assign-statement> | <call-function-statement> )
            id = 2;
            id(2);
        """
        if(self.identifier()):
            
            identificador_tipo = self.current_context.symbol_table.lookup(self.actualToken.lexema).tipo
            identificador_token = self.actualToken
            identificador_nome = self.actualToken.lexema
            token = self.actualToken
            
            self.getNextToken()  
            print(f'ATUALLLLLLLLLLLLL {self.actualToken}')
            
            if(self.match("=")):
                self.checkIfIsDeclared(identificador_token)
                typeAssignment, temp = self.assignStatement()
                print(f"TIPOOOOOOOOOOOO: {typeAssignment}")
                print(f"TIPOOOOOOOOOOOO: {identificador_tipo}")

                #validar se id tem tipo igual ao da expressão
                if(identificador_tipo != typeAssignment):
                    self.throwSemanticError()

                if(self.match(";")):
                    self.getNextToken()

                return identificador_tipo
            
            elif(self.match('(')):
                self.identifier()
                
                result = self.global_context.lookup(token)
                if result:
                    self.callFunctionStatement()

                else:
                    self.throwSemanticError()
                    
                if(self.match(";")):
                    self.getNextToken()
                
                    return True 
        self.throwSyntaxError()

    
    def assignStatement(self):
        logging.info(f'assignStatement')
        # teste: int result |= a + b * c;
        # erro com a = 1;
        if(self.match("=")):
            self.getNextToken() # a

            typeExpression, temp = self.expression() 
            
            return typeExpression, temp
            # if(self.expression()):
            #     return True
        # return False
        self.throwSyntaxError()
    
    
    def callFunctionStatement(self):
        logging.info(f'callFunctionStatement')
        if(self.match("(")):
            self.getNextToken()

            self.callParameters()
            
            # if(self.identifier()):
            #     self.getNextToken()

            #     while self.match(','):
            #         self.getNextToken()
            #         self.identifier()
            #         self.getNextToken()

            if(self.match(")")):
                return True
        return False

    # ==================================== EXPRESSÕES =============================================== #
    
    
    def expression(self):
        logging.info(f'expression')

        # if(self.simpleExpression()):
        typeFirstExpression, temp1 = self.simpleExpression()
        operator = self.assignOperator()
        #verificar a frente se tem  + - * /
        if operator:
            #X é inteiro entao throw? --> here_we_go_again (x > 0) x tem que ser inteiro aqui
            # if(typeFirstExpression == Tipo.INT):
            #     self.throwSemanticError()

            self.getNextToken()
                
            typeAnotherExpression, temp2 = self.simpleExpression()
            # here_we_go_again (x > 0) 
            # if(typeFirstExpression == Tipo.INT):
            #     self.throwSemanticError()

            temp = self.generator.gen_temp()
            print(f'EMITRRRR {temp} = {temp1} {operator} {temp2}')
            self.generator.emit(f'{temp} = {temp1} {operator} {temp2}')
            
            return typeAnotherExpression, temp
        
        return typeFirstExpression, temp1

    
    def simpleExpression(self):
        logging.info(f'simpleExpression')
        typeUnaryOperator, unaryOperator = self.unaryOperator()
        
        logging.info(f"unaryOperator is {unaryOperator}")
        typeTerm, temp = self.term()
        #se ativar quebra na declaracao de var
        # deixar desativado quebra em a + b * c;
        # if(self.term()): 
        #     return True
        
        if(typeUnaryOperator != None and typeUnaryOperator != typeTerm):
            self.throwSemanticError()
        
        if typeUnaryOperator:
            new_temp = self.generator.gen_temp()
            self.generator.emit(f"{new_temp} = {unaryOperator} {temp}")
        
        return typeTerm, temp

    
    def unaryOperator(self):
        logging.info(f'unaryOperator')
        if self.match("+"):
            self.getNextToken()
            return Tipo.INT, "+"
        elif self.match("-"):
            self.getNextToken()
            return Tipo.INT,"-"
        elif self.match("!"):
            self.getNextToken()
            return Tipo.BRUH, "!"
        return None, None
    
    
    def assignOperator(self):
        logging.info(f'call assignOP {self.actualToken.lexema}')
        if self.match("=="):
            return "=="
        elif self.match("!="):
            return "!="
        elif self.match("<"):
            return "<"
        elif self.match("<="):
            return "<="
        elif self.match(">"):
            return ">"
        elif self.match(">="):
            return ">="
        elif self.match("AND"):
            return "AND"
        elif self.match("OR"):
            return "OR"
        return None
    
    
    def term(self):
        logging.info(f'term {self.actualToken.lexema}')
        typeFactor, temp1 = self.factor()

        if(self.match('+') or self.match('-') or self.match('*') or self.match('/')):
            operator = self.actualToken.lexema
            self.getNextToken()
            typeTerm, temp2 = self.term()
            
            # se for numeros de identificadores
            # a + b * c;
            # if(typeTerm == Tipo.BRUH or typeFactor == Tipo.BRUH):
            #     self.throwSemanticError()
                
            temp = self.generator.gen_temp()
            self.generator.emit(f"{temp} = {temp1} {operator} {temp2}")
            temp1 = temp
            
        #verificar se é chamado de funcao

            
        return typeFactor, temp1
        # if(self.factor()):
        #     while self.match('+') or self.match('-') or self.match('*') or self.match('/'):
        #         self.getNextToken()
        #         self.term()

        #     return True
        # return False
    
    
    def factor(self):
        logging.info(f'factor {self.actualToken.lexema}')
        if(self.match("real") or self.match("barca")):
            temp = self.generator.gen_temp()
            self.generator.emit(f"{temp} = {self.actualToken.lexema}")
            self.getNextToken()
            return Tipo.BRUH, temp
        elif(self.number()):
            temp = self.generator.gen_temp()
            self.generator.emit(f"{temp} = {self.actualToken.lexema}")
            self.getNextToken()

            return Tipo.INT, temp
        elif(self.identifier()):
            #TODO: Existe em parentes acima, já foi declarado
            token = self.actualToken
            #self.checkIfIsDeclared(self.actualToken)
            
            self.getNextToken()
            if token.tipo == 'id':
                return self.getIdentifier(token), token.lexema
            # int result = soma(a, b);
            # nesse ponto estamos lendo o ( de soma
            self.callParameters()
            
            #remover para simplificar
            # if(self.callFunctionStatement()):
            #     self.getNextToken()
            #     return True
            
            # return True
        elif(self.match("(")):
            self.getNextToken()

            insideParenthesisType, temp = self.expression()

            if(self.match(")")):
                self.getNextToken()
                return insideParenthesisType, temp

            # if(self.expression()):
            #     if(self.match(")")):
            #         self.getNextToken()
            #         return True

        # return False
        #self.throwSyntaxError()

    # ==================================== NÚMEROS E IDENTIFICADORES =============================================== #
    
    
    
    def identifier(self, tipo=None):
        logging.info(f"identificador do token: {self.actualToken.lexema} == id")
        if(self.match("id")):
            
            # verificar se existe e atribuir 
            if not self.handleDuplicates():
                self.current_context.setType(self.actualToken, tipo)
                
            return True
        
        return False
    
    
    
    def number(self):
        if(self.match('number')):
            return True
        
        return False
    
    #############################################################################################
    def handleDuplicates(self):
        #TODO: se for funcao, erro
        
        
        # se for var, copiar para contexto interno.
        result = self.current_context.lookup(self.actualToken)
        if result:
            self.current_context.symbol_table.setReg(result)
            return True
        return False
    
    def getIdentifier(self, token: Token):
        # DEVE PEGAR O TIPO DE ONDE ELE É DECLARADO/PRIMEIRA VEZ QUE APARECE
        registro = self.current_context.symbol_table.lookup(token.lexema)
        if registro:
            return registro.tipo 


    
    def checkIdDuplicated(self, token: Token):

        registro = self.current_context.symbol_table.lookup(token.lexema)

        if not registro:
            self.throwSemanticError()

    
    def checkIfIsDeclared(self, token: Token):
        #TODO: Verificar nos contextos parent.
        registro = self.current_context.lookup(token)
        
        if not registro:
            self.throwSemanticError()

    def setIdType(self, idToken, newType, context = None):
        
        # if(context):
        #     context.symbol_table.setType(idToken, newType)
            
        self.current_context.setType(idToken, newType)

    def throwSyntaxError(self):
        logging.error(f"SyntaxError → {self.actualToken}")
        raise Exception(f"SyntaxError → {self.actualToken}")
    
    def throwSemanticError(self):
        logging.error(f"SyntaxError → {self.actualToken}")
        raise Exception(f"SemanticError → {self.actualToken}")
