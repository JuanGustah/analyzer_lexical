from tabulate import tabulate
from enum import Enum

class Type(Enum):
    BRUH = 1
    INT = 2

class Context(Enum):
    FUNCTION = 1
    LOOP = 2

class Parser:
    def __init__(self, tokens, symbol_table):
        self.tokens = tokens
        self.symbol_table = symbol_table
        self.actualTokenPos = -1
        self.actualToken = []
        self.structure_print = []

    def print_all(self):
        
        print(tabulate(self.structure_print, headers=["Tipo", "Valor", "Lexema", "Linha"], tablefmt="grid"))

    def match(self, matchString):
        tokenString, line = self.actualToken[0], self.actualToken[1]
        
        if(tokenString == 'id' and matchString== 'id'):
            idIndex = self.actualToken[1]
            if(self.symbol_table.lookup(idIndex)):
                return True
        elif(tokenString == 'number' and matchString == 'number'):
            value = self.actualToken[1]
            if(value is not None):
                return True
            return True
        elif(tokenString == matchString):
            return True
        return False
    
    def getNextToken(self):
        if self.actualTokenPos + 1 < len(self.tokens):
            self.actualTokenPos += 1
            self.actualToken = self.tokens[self.actualTokenPos]

            self.structure_print.append([
                 self.actualToken[0],  # Tipo 
                 self.actualToken[1], #Valor
                 self.actualToken[2],   # lexema
                 self.actualToken[3]    # linha 
            ])
        else:
            self.actualToken = None

    def lookAhead(self, matchString):
        if self.actualTokenPos + 1 < len(self.tokens):
            tokenString = self.tokens[self.actualTokenPos+1][0][0]

            isEqual = tokenString == matchString

            if(isEqual):
                self.getNextToken()
                return True
            return False
        else:
            return False
    
    def start(self):
        try:

            if self.program():
                print("\033[92m[ok] Execução bem-sucedida: Deu bom!\033[0m")  
                return True
            else:
                
                print("\033[91m[err] Execução falhou:\033[0m")
                print(f"\033[91m[err] Token = {self.actualToken[2]}, Linha = {self.actualToken[3]}\033[0m")  
                return False
        except Exception as e:
            print(e)

    # ================= Descrição BNF da Linguagem Simplificada ===================================== #
    
    def program(self):
        self.getNextToken()
        
        while self.checkType() or self.match('void'):  
            if self.subRoutineStep():
                self.getNextToken()
                continue
            else:
                
                return False  

        if self.mainBody(): 
            return True
        return False

    def mainBody(self):
        if(self.match("meme")):
            self.getNextToken()

            if(self.body()):
                return True
        return False 
    
    def body(self, context = None):
        if(self.match("{")):
            self.getNextToken()

            if(self.checkType()):
                self.declarationVariableStep()
                    
                # while self.checkType():
                #     if self.declarationVariableStep():
                #         pass
                #     else:
                #         return False

            if self.hasStatement(context):
                self.statements(context)
                if self.match("}"):
                    return True
            
            return False
            # if(self.statements()):
            #     if(self.match("}")):
            #         return True
            # else:
            #     return False
        return False

    def subRoutineStep(self):      
        if self.declarationFunctionProcedure():
            return True
        
        return False
    
    def declarationVariableStep(self):
        self.declarationVariable()

        if(self.checkType()):
            self.declarationVariableStep()
    
    # ==================================== DECLARAÇÕES =============================================== #
    def checkType(self):
        if(self.match("int")):
            return True
        elif(self.match("bruh")):
            return True
        
        return False
    
    def type(self):
        if(self.match("int")):
            return Type.INT
        elif(self.match("bruh")):
            return Type.BRUH
        
        self.throwSemanticError()
    
    def declarationVariable(self):
        if self.checkType(): 
            declarationVariableType = self.type()
            self.getNextToken()  

            if self.identifier():
                id = self.getId()

                self.getNextToken()  

                if self.match("="):
                    # if self.assignStatement(): 
                    typeAssignment = self.assignStatement()

                    if(typeAssignment != declarationVariableType):
                        self.throwSemanticError()

                    self.setIdType(id, typeAssignment)
                    self.getNextToken()  

                    if self.match(";"):
                        self.getNextToken()  

                    # return True

                if self.match(";"):
                    self.setIdType(id, declarationVariableType)
                    self.getNextToken()     
                    # return True
            # return False
        # return False
    
    def declarationParameters(self):
        if(self.checkType()):
            self.getNextToken()
            if(self.identifier()):
                self.getNextToken()
                
            while self.match(','):
                self.getNextToken()
                self.declarationParameters()
                
            return True
        
        return False
    
    def declarationFunctionProcedure(self):
        if self.match("void"):
            self.getNextToken()
            if self.match('hora_do_show'):
                self.getNextToken()
                if self.identifier(): 
                    self.getNextToken()
                    if self.match('('):  
                        self.getNextToken()
                        if self.declarationParameters():  
                            pass  
                        if self.match(')'):  
                            self.getNextToken()
                            if self.body():  
                                return True
            return False

        if self.checkType():  
            self.getNextToken()
            if self.match('hora_do_show'):
                self.getNextToken()
                if self.identifier(): 
                    self.getNextToken()
                    if self.match('('):  
                        self.getNextToken()
                        if self.declarationParameters():  
                            pass  
                        if self.match(')'): 
                            self.getNextToken()
                            if self.body():
                                return True
            return False

            
    
    # ==================================== COMANDOS =============================================== #
    
    # def statements(self):
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

    def statements(self, context = None):
        #adicionar validação para return/receba e chamada de função
        # print(self.actualToken)
        typeStatement = self.statement()

        if self.hasStatement(context):
            self.statements()

    def hasStatement(self, context = None):
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
            return True
        elif(self.match("papapare")):
            if(context != Context.LOOP):
                self.throwSemanticError()
                return False

            return True
        elif(self.match("ate_outro_dia")):
            if(context != Context.LOOP):
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
            #falta finalizar
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
        if(self.match("irineu_voce_sabe")):
            self.getNextToken()

            if(self.match("(")):
                self.getNextToken()

                expressionType = self.expression()
                # if(self.expression()):

                if(expressionType != Type.BRUH):
                    self.throwSemanticError()

                if(self.match(")")):
                    self.getNextToken()

                    if(self.body()):
                        self.getNextToken()
                        # if(self.lookAhead("nem_eu")):
                        if(self.match("nem_eu")):
                            self.getNextToken()

                            if(self.body()):
                                return None

                        return None
        self.throwSyntaxError()
    
    def loopStatement(self):
        if(self.match("here_we_go_again")):
            self.getNextToken()

            if(self.match("(")):
                self.getNextToken()

                if(self.expression()):
                    if(self.match(")")):
                        self.getNextToken()

                        if(self.body(Context.LOOP)):
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
                
                if(self.expression()):
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

            typeReturnExpresison = self.expression()
            # if(self.expression()):

            if(self.match(";")):
                self.getNextToken()
            
            return typeReturnExpresison
                
        self.throwSyntaxError()
    
    def callOrAssignStatement(self):
        if(self.identifier()):
            idType = self.getTypeId(self.actualToken)

            self.getNextToken()  

            if(self.match("=")):
                typeAssignment = self.assignStatement()

                #validar se id tem tipo declarado

                #validar se id tem tipo igual ao da expressão
                if(idType != typeAssignment):
                    self.throwSemanticError()

                return idType
            elif(self.callFunctionStatement()):
                return True
        
        self.throwSyntaxError()

    def assignStatement(self):
        if(self.match("=")):
            self.getNextToken()

            typeExpression = self.expression()
            return typeExpression
            # if(self.expression()):
            #     return True
        # return False
        self.throwSyntaxError()
    
    def callFunctionStatement(self):
        if(self.match("(")):
            self.getNextToken()

            if(self.identifier()):
                self.getNextToken()

                while self.match(','):
                    self.getNextToken()
                    self.identifier()
                    self.getNextToken()

                if(self.match(")")):
                    return True
        return False

    # ==================================== EXPRESSÕES =============================================== #
    
    def expression(self):
        # if(self.simpleExpression()):
        typeFirstExpression = self.simpleExpression()

        if(self.assignOperator()):
            if(typeFirstExpression == Type.INT):
                self.throwSemanticError()

            self.getNextToken()
                
            typeAnotherExpression = self.simpleExpression()

            if(typeFirstExpression == Type.INT):
                self.throwSemanticError()

            return typeAnotherExpression
        
        return typeFirstExpression

    def simpleExpression(self):
        typeUnaryOperator = self.unaryOperator()
        
        typeTerm = self.term()

        # if(self.term()):
        #     return True

        if(typeUnaryOperator!= None and typeUnaryOperator != typeTerm):
            self.throwSemanticError()
        
        return typeTerm

    def unaryOperator(self):
        if(self.match("+")):
            self.getNextToken()
            return Type.INT
        elif(self.match("-")):
            self.getNextToken()
            return Type.INT
        elif(self.match("!")):
            self.getNextToken()
            return Type.BRUH

        return None
    
    def assignOperator(self):
        if(self.match("==")):
            return True
        elif(self.match("!=")):
            return True
        elif(self.match("<")):
            return True
        elif(self.match("<=")):
            return True
        elif(self.match(">")):
            return True
        elif(self.match(">=")):
            return True
        elif(self.match("AND")):
            return True
        elif(self.match("OR")):
            return True

        return False
    
    def term(self):
        typeFactor = self.factor()

        if(self.match('+') or self.match('-') or self.match('*') or self.match('/')):
            if(typeFactor == Type.BRUH):
                self.throwSemanticError()
            
            self.getNextToken()
            typeTerm = self.term()
            
            if(typeTerm == Type.BRUH):
                self.throwSemanticError()
        
        return typeFactor
        # if(self.factor()):
        #     while self.match('+') or self.match('-') or self.match('*') or self.match('/'):
        #         self.getNextToken()
        #         self.term()

        #     return True
        # return False
    
    def factor(self):
        if(self.match("real")):
            self.getNextToken()
            return Type.BRUH
            # return True
        elif(self.match("barca")):
            self.getNextToken()
            return Type.BRUH
            # return True
        elif(self.number()):
            self.getNextToken()

            return Type.INT
            # return True
        elif(self.identifier()):
            self.getNextToken()

            idType = self.getTypeId(self.actualToken)

            return idType

            #remover para simplificar
            # if(self.callFunctionStatement()):
            #     self.getNextToken()
            #     return True
            
            # return True
        elif(self.match("(")):
            self.getNextToken()

            insideParenthesisType = self.expression()

            if(self.match(")")):
                self.getNextToken()
                return insideParenthesisType

            # if(self.expression()):
            #     if(self.match(")")):
            #         self.getNextToken()
            #         return True

        # return False
        self.throwSyntaxError()

    # ==================================== NÚMEROS E IDENTIFICADORES =============================================== #
    
    def identifier(self):
        if(self.match("id")):
            return True
        
        return False
    
    def number(self):
        if(self.match('number')):
            return True
        
        return False
    
    def getTypeId(self, idToken):
        idIdx = idToken
        symbolTableId = self.symbol_table.lookup(idIdx)
        type = symbolTableId['type']
        return type

    def getId(self):
        return self.actualToken
    
    def setIdType(self, id, newType):
        #id actualToken antigo
        #actualToken[1] = idx da symbolTable
        self.symbol_table.setType(id[1],newType)

    def throwSyntaxError(self):
        raise Exception(f"SyntaxError → Token = {self.actualToken[2]}, Linha = {self.actualToken[3]}")
    
    def throwSemanticError(self):
        raise Exception(f"SemanticError →  Token = {self.actualToken[2]}, Linha = {self.actualToken[3]}")
