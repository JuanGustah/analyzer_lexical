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
    def __init__(self, nature: Tipo, alias = None):
        self.nature: Tipo = nature
        self.alias: str = alias

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
        else:
            self.actualToken = None
            print(f'SEM TOKEN PARA LEITURA')
    
    
    def start(self):
        if self.program():  
            #self.generator.print_instructions()
            return True
        else:
            return False

    # ================= Descrição BNF da Linguagem Simplificada ===================================== #
    
    
    def program(self):
        self.getNextToken()
        
        
        if self.checkType() or self.match('void'):
            self.subRoutineStep()
            # if self.subRoutineStep():
                # self.getNextToken()
                # continue
            # else:
                
            #     return False  

        ex = self.mainBody()

        return True

    
    def mainBody(self):
        
        if(self.match("meme")):
            self.next_context = 'meme'
            self.getNextToken()
            
            return self.body(ContextMetadata(Nature.MEME, 'meme'))
            
        
        self.throwSyntaxError()
    
    def enter_context(self, metadata: ContextMetadata = None, read_mode = False):
        if read_mode == True:
            next_c = self.current_context.get_subcontext(f"{self.current_context.parser_counter}_{self.next_context}")
            
            if next_c:
                    if(metadata):
                        next_c.nature = metadata.nature
                        next_c.alias = metadata.alias
                        
                    self.current_context = next_c
                    
        if self.next_context and read_mode == False:
            if self.current_context:
                next_c = self.current_context.get_subcontext(f"{self.current_context.parser_counter}_{self.next_context}")
                next_c.parent.parser_counter += 1

                if next_c:
                    if(metadata):
                        next_c.nature = metadata.nature
                        next_c.alias = metadata.alias
  
                    self.current_context = next_c
    
    def exit_context(self):
        self.current_context = self.current_context.parent
           
    def body(self, metadata: ContextMetadata = None, con: Context = None):
        
        if(self.match("{")):
            
            self.enter_context(metadata, False)
            self.getNextToken()

            if(self.checkType()):
                self.declarationVariableStep()
                    
                # while self.checkType():
                #     if self.declarationVariableStep():
                #         pass
                #     else:
                #         return False

            if self.hasStatement():
                last_statement_type = self.statements()

                if self.match("}"):
                    #Antes: 
                    #self.current_context = self.current_context.parent
                    #NOVO: Verificar o final do bloco, receba 
                    if metadata:
                        if metadata.nature == Nature.FUNC:
                            if last_statement_type != 'receba':
                                self.throwSemanticError(f"Função deve terminar com 'receba'")
                        # elif metadata.nature == Nature.PROC:
                        #     if last_statement_type == 'receba':
                        #         self.throwSemanticError("Procedimento não deve terminar com 'receba'")
                        self.exit_context()
                    return None
                
                if self.match(';'):
                    return None    
            
            self.throwSyntaxError()
            # if(self.statements()):
            #     if(self.match("}")):
            #         return True
            # else:
            #     return False
        self.throwSyntaxError()

    
    def subRoutineStep(self):
              
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
        
        self.declarationVariable()

        if(self.checkType()):
            self.declarationVariableStep()
    
    
    def callParameters(self, funcParams, paramsTemps):
        

        if(len(funcParams) == 0):
            self.throwSemanticError("Deve existir parametros")

        typeExpression, temp = self.expression()

        paramType, name = funcParams.pop(0)

        if(typeExpression != paramType):
            self.throwSemanticError(f"tipo da expressao {temp} != {paramType}")
        
        if(self.match(',')):
            self.getNextToken()

            paramsTemps.append(temp)
            self.callParameters(funcParams, paramsTemps)
            return paramsTemps
        elif len(funcParams) > 0:
            self.throwSemanticError("len(funcParams) > 0")
        else:
            paramsTemps.append(temp)
            return paramsTemps
        
    
    # ==================================== DECLARAÇÕES =============================================== #
    def checkType(self):
        if(self.match("int")):
            return Tipo.INT
        elif(self.match("bruh")):
            return Tipo.BRUH
        
        return False
    
    
    def declarationVariable(self):
        
        declarationVariableType = self.checkType()
        if declarationVariableType: 
            
            self.getNextToken()  

            if self.identifier(declarationVariableType):
                self.checkIdDuplicated(self.actualToken)
                idToken = self.actualToken
                self.getNextToken()  

                if self.match("="):
                    typeAssignment, temp = self.assignStatement()

                    if(typeAssignment != declarationVariableType):
                        self.throwSemanticError(f"{typeAssignment} != {declarationVariableType}")

                    self.generator.emit(f"{idToken.lexema} = {temp}")
                    self.setIdType(idToken, typeAssignment)

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
    
    # Novo
    def moveIdentifierToCorrectContext(self, idetifier_nome):
        registro_no_pai = self.current_context.lookupByName(idetifier_nome)
        self.current_context.symbol_table.add(registro_no_pai)
        self.current_context.parent.symbol_table.removeByCod(registro_no_pai.cod)
        
    def declarationParameters(self, funcName):
        
        tipo_variavel = self.checkType()
        if(tipo_variavel):
            self.getNextToken()
            
            if(self.identifier(tipo_variavel)):
                paramName = self.actualToken.lexema
                
                self.addParamInSymbolTable(funcName,paramName,tipo_variavel)
                # Novo
                self.moveIdentifierToCorrectContext(paramName) #to em 0_hora_do_show
                self.getNextToken()
            else:
                self.throwSyntaxError()
                
            if(self.match(',')):
                self.getNextToken()

                if(self.checkType()):
                    return self.declarationParameters(funcName)
                self.throwSyntaxError()
            else:
                return None
    
    
    def declarationFunction(self):
        

        tipo = self.checkType()
        if tipo:  
            self.getNextToken()
            if self.match('hora_do_show'):
                self.getNextToken()
                if self.identifier(tipo):
                    funcName = self.actualToken.lexema

                    #adicionar tipo de retorno da tabela de simbolos do id da função (global)
                    # simbolo tbm pode ser BRUH
                    # MODIFICAÇÃO
                    #self.setIdType(self.actualToken, Tipo.INT, self.global_context)
                    # Novo
                    self.setIdType(self.actualToken, tipo, self.global_context)

                    self.generator.emit(f"func begin {funcName}")

                    self.next_context = "hora_do_show" 
                    # Novo
                    self.enter_context(ContextMetadata(Nature.FUNC, funcName), True)
                    
                    self.getNextToken()
                    if self.match('('):  
                        self.getNextToken()
                        
                        self.declarationParameters(funcName)

                        if self.match(')'): 
                            # Novo
                            self.exit_context()
                            self.getNextToken()

                            self.body(ContextMetadata(Nature.FUNC, funcName))
                            
                            self.generator.emit(f"func end")

                            self.getNextToken()

                            return None
                            
        self.throwSyntaxError()

    
    def declarationProcedure(self):
        
        if self.match("void"):
            self.getNextToken()
            if self.match('hora_do_show'):
                self.getNextToken()
                if self.identifier():
                    funcName = self.actualToken.lexema
                    self.generator.emit(f"proc begin {funcName}")

                    self.next_context = "hora_do_show"
                    
                    # Novo
                    self.enter_context(ContextMetadata(Nature.PROC, funcName), True)
                    
                    self.getNextToken()
                    if self.match('('):  
                        self.getNextToken()

                        self.declarationParameters(funcName)

                        if self.match(')'):
                            # Novo
                            self.exit_context()  
                            self.getNextToken()

                            self.body(ContextMetadata(Nature.PROC, funcName))
                            
                            self.generator.emit(f"proc end")
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

    
    # def statements(self):
        
    #     typeStatement = self.statement()
    
    #     if self.hasStatement():
    #         self.statements()
        
    #     return typeStatement
    
    #NOVO:
    def statements(self):
        if self.hasStatement():
            typeStatement = self.statement()
            if self.hasStatement():
                return self.statements()
            else:
                return typeStatement
        return None
    
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
            if(self.current_context.nature != Nature.FUNC):
                self.throwSemanticError(f"só existe receba dentro de funcao: {self.current_context.nature} != {Nature.FUNC}")
                return False
            
            return True
        elif(self.match("papapare")):
            if(self.current_context.nature != Nature.LOOP):
                self.throwSemanticError(f"{self.current_context.nature} != {Nature.LOOP}")
                return False

            return True
        elif(self.match("ate_outro_dia")):
            if(self.current_context.nature != Nature.LOOP):
                self.throwSemanticError(f"{self.current_context.nature} != {Nature.LOOP}")
                return False

            return True
        elif(self.match("id")):
            return True
        return False
    
    
    # def statement(self):
    #     if(self.match("papapare") or self.match("ate_outro_dia")):
    #         return self.jumpStopStatement()
    #     elif(self.match("irineu_voce_sabe")):
    #         return self.conditionStatement()
    #     elif(self.match("here_we_go_again")):
    #         return self.loopStatement()
    #     elif(self.match("amostradinho")):
    #         return self.printStatement()
    #     elif(self.match("casca_de_bala")):
    #         return self.readStatement()
    #     elif(self.match("receba")):
    #         return self.returnStatement()
    #     elif(self.match("id")):
    #         #falta finalizar a parte de chamada de função
    #         return self.callOrAssignStatement()

    #     self.throwSyntaxError()
    # NOVO: Retornar o nome do statement
    def statement(self):
        if self.match("papapare") or self.match("ate_outro_dia"):
            self.jumpStopStatement()
            return 'jump_stop'
        elif self.match("irineu_voce_sabe"):
            self.conditionStatement()
            return 'condition'
        elif self.match("here_we_go_again"):
            self.loopStatement()
            return 'loop'
        elif self.match("amostradinho"):
            self.printStatement()
            return 'amostradinho'
        elif self.match("casca_de_bala"):
            self.readStatement()
            return 'casca_de_bala'
        elif self.match("receba"):
            type_return = self.returnStatement()
            return 'receba'
        elif self.match("id"):
            return self.callOrAssignStatement()
        self.throwSyntaxError()
    
    def conditionStatement(self):
        
        if(self.match("irineu_voce_sabe")):
            self.getNextToken()

            if(self.match("(")):
                self.getNextToken()

                expressionType, temp = self.expression()
                # if(self.expression()):

                # irineu_voce_sabe (x == 2) - comparar inteiros
                if(expressionType != Tipo.BRUH):
                    self.throwSemanticError(f"{expressionType} != {Tipo.BRUH}")

                if(self.match(")")):
                    self.getNextToken()
                    
                    label_else = self.generator.gen_label()
                    label_end = self.generator.gen_label()
                    #self.generator.emit(f"if {temp} == 0 goto {label_else}")
                    self.generator.emit(f"if {temp} goto {label_else}")
                    
                    self.next_context = "irineu_voce_sabe"
                    self.body(ContextMetadata(Nature.IF, 'irineu_voce_sabe'))
                    
                    self.generator.emit(f"goto {label_end}")
                    self.generator.emit(f'{label_else}:')
                    
                    # if():
                    self.getNextToken()

                    # if(self.lookAhead("nem_eu")):
                    if(self.match("nem_eu")):
                        self.getNextToken()

                        self.next_context = "nem_eu"
                        self.body(ContextMetadata(Nature.ELSE, 'nem_eu'))
                        
                        self.generator.emit(f'{label_end}')
                        
                        # if():
                        return None

                    return None
        self.throwSyntaxError()
    
    
    def loopStatement(self):
        
        if(self.match("here_we_go_again")):
            self.getNextToken()

            if(self.match("(")):
                
                label_start = self.generator.gen_label()
                label_end = self.generator.gen_label()
                self.generator.emit(f'{label_start}:')

                self.getNextToken()
                
                expressionType, temp = self.expression()

                if(expressionType != Tipo.BRUH):
                    self.throwSemanticError()

                if(self.match(")")):
                    
                    #self.generator.emit(f'if {temp} == 0 goto {label_end}')
                    self.generator.emit(f'if {temp} goto {label_end}')
                    
                    self.getNextToken()

                    # if():
                    self.next_context = "here_we_go_again"
                    self.body(ContextMetadata(Nature.LOOP, 'here_we_go_again'))
                    
                    self.generator.emit(f'goto {label_start}')
                    self.generator.emit(f'{label_end}:')
                    self.getNextToken()

                    return None
                        
        self.throwSyntaxError()
    
    
    def jumpStopStatement(self):
        
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
        
        if(self.match("receba")):
            self.getNextToken()

            typeReturnExpresison, temp = self.expression()
            
            funcName = self.current_context.alias
            funcSymbolTable = self.global_context.symbol_table.lookup(funcName)
            
            if(typeReturnExpresison != funcSymbolTable.tipo):
                self.throwSemanticError(f"{typeReturnExpresison} != {funcSymbolTable.tipo}")


            self.generator.emit(f"return {temp}")
            # if(self.expression()):

            if(self.match(";")):
                self.getNextToken()
                return "Receba", typeReturnExpresison
            
                
        self.throwSyntaxError()
    
    
    def callOrAssignStatement(self):
        """
            <call-or-assign-statement> ::= 
            <identifier> ( <assign-statement> | <call-function-statement> )
            id = 2;
            id(2);
        """
        if(self.identifier()):
            identificador_tipo = self.current_context.lookupByName(self.actualToken.lexema).tipo
            identificador_token = self.actualToken
            identificador_nome = self.actualToken.lexema
            
            self.getNextToken()  
            
            if(self.match("=")):
                self.checkIfIsDeclared(identificador_token)
                # ele volta depois do soma então o token é (
                typeAssignment, temp = self.assignStatement()

                #validar se id tem tipo igual ao da expressão
                if(identificador_tipo != typeAssignment):
                    self.throwSemanticError(f"{identificador_tipo} != {typeAssignment}")

                self.generator.emit(f"{identificador_nome} = {temp}")

                if(self.match(";")):
                    self.getNextToken()
                    return identificador_tipo
                elif self.match("("):
                    funcRegister = self.global_context.symbol_table.lookup(temp)
                    return self.callFunctionStatement(funcRegister)
                else:
                    self.throwSyntaxError()
            
            elif(self.match('(')):
                funcRegister = self.global_context.symbol_table.lookup(identificador_nome)

                if funcRegister:
                    self.callFunctionStatement(funcRegister)
                else:
                    self.throwSemanticError(f'funcRegister não existe')
                    
                if(self.match(";")):
                    self.getNextToken()

                if funcRegister.tipo:
                    return funcRegister.tipo
                else:
                    return None
        self.throwSyntaxError()

    
    def assignStatement(self):
        
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
    
    
    def callFunctionStatement(self, funcRegister):
        
        if(self.match("(")):
            self.getNextToken()

            paramsCopy = funcRegister.params[:]
            paramsTemps = []
            if(not self.match(")")):
                paramsTemps = self.callParameters(paramsCopy,[])
            else:
                if(len(paramsCopy) != 0):
                    self.throwSemanticError(f"paramentros para copiar {len(paramsCopy)} != 0")
            
            # if(self.identifier()):
            #     self.getNextToken()

            #     while self.match(','):
            #         self.getNextToken()
            #         self.identifier()
            #         self.getNextToken()

            #passa quando não tem parametros e quanto tem parametros, não remover!
            if(self.match(")")):
                self.getNextToken()

                #print de chamada de função
                for temp in paramsTemps:
                    self.generator.emit(f'param {temp}')

                self.generator.emit(f'{funcRegister.nome},{len(paramsTemps)}')
                self.generator.emit(f'return')
                return True
        return False

    # ==================================== EXPRESSÕES =============================================== #
    
    
    def expression(self):
        

        # if(self.simpleExpression()):
        typeFirstExpression, temp1 = self.simpleExpression()
        operator, operatorType = self.assignOperator()
        if operator:
            self.getNextToken()
                
            typeAnotherExpression, temp2 = self.simpleExpression()
            
            if typeFirstExpression != typeAnotherExpression:
                self.throwSemanticError(f'tipo exp1{typeFirstExpression} != tipo exp2 {typeAnotherExpression}')
            elif typeFirstExpression != operatorType and operatorType != None:
                self.throwSemanticError(f"operador tipo {operatorType} != None")

            temp = self.generator.gen_temp()
            self.generator.emit(f'{temp} = {temp1} {operator} {temp2}')
            
            return Tipo.BRUH, temp
        
        return typeFirstExpression, temp1

    
    def simpleExpression(self):
        
        typeUnaryOperator, unaryOperator = self.unaryOperator()
        
        
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
            return typeTerm, new_temp
        
        return typeTerm, temp

    
    def unaryOperator(self):
        
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
        
        if self.match("=="):
            return "==", None
        elif self.match("!="):
            return "!=", None
        elif self.match("<"):
            return "<", Tipo.INT
        elif self.match("<="):
            return "<=", Tipo.INT
        elif self.match(">"):
            return ">", Tipo.INT
        elif self.match(">="):
            return ">=", Tipo.INT
        elif self.match("and"):
            return "and", Tipo.BRUH
        elif self.match("or"):
            return "or", Tipo.BRUH
        return None, None
    
    
    def term(self):
        
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
            token = self.actualToken
            self.checkIfIsDeclared(self.actualToken)
            
            self.getNextToken()

            return self.getIdentifier(token.lexema), token.lexema
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
        self.throwSyntaxError()

    # ==================================== NÚMEROS E IDENTIFICADORES =============================================== #
    def identifier(self, tipo=None):
        
        if(self.match("id")):
            return True
        
        return False
    
    def number(self):
        if(self.match('number')):
            return True
        
        return False
    
    ###############################################  HELPERS   ############################################
    def getIdentifier(self, idName):
        registro = self.current_context.lookupByName(idName)
        
        if registro:
            return registro
        else:
            return None


    def checkIdDuplicated(self, token: Token):
        tokenLinha = token.linha
        tokenColuna = token.coluna

        # ele acha ele mesmo
        registro = self.current_context.symbol_table.lookup(token.lexema)

        if not registro:
            self.throwSemanticError(f"Variavel não existe")

        registroLinha = registro.linha
        registroColuna = registro.coluna

        #para validar se a declaração de variavel esta duplicada é necessário validar
        #se o local que eu estou lendo (token) é diferente do local que ele foi declarado (registro)
        if tokenLinha != registroLinha or tokenColuna != registroColuna:
            self.throwSemanticError("Variavel duplicada")

    
    def checkIfIsDeclared(self, token: Token):
        tokenLinha = token.linha
        tokenColuna = token.coluna
        
        registro = self.current_context.lookupByName(token.lexema)

        if not registro:
            self.throwSemanticError(f"Variavel não declarada")

        registroLinha = registro.linha
        registroColuna = registro.coluna
        
        #para validar se o id foi declarado é necessário validar
        #se o local que eu estou lendo (token) é igual o local que ele foi declarado (registro)
        #pois aqui estou apenas usando a variavel, portanto não devem ser o mesmo lugar a leitura e decl
        if tokenLinha == registroLinha and tokenColuna == registroColuna:
            self.throwSemanticError(f"Variavel {registro.nome} Não Declarada")

    def setIdType(self, idToken, newType, context = None):
        if(context):
            context.setType(idToken, newType)
            
        self.current_context.setType(idToken, newType)
    
    def addParamInSymbolTable(self, funcName, paramName, paramType):
        registro = self.global_context.symbol_table.addParam(funcName, paramName, paramType)
        
        # Novo
        #registro.tipo = paramType
        registro = self.current_context.lookupByName(paramName) 
        registro.tipo = paramType
        

    def throwSyntaxError(self, msg=None):
        error_msg = f"SyntaxError → {self.actualToken}"
        if msg:
            error_msg += f": {msg}"

        raise Exception(error_msg)
    
    def throwSemanticError(self, msg=None):
        error_msg = f"SemanticError → "
        if msg:
            error_msg += f": {msg}"
        raise Exception(f"\033[91m{error_msg}\033[0m")