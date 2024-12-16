class Parser:
    def __init__(self, tokens, symbol_table):
        self.tokens = tokens
        self.symbol_table = symbol_table
        self.actualTokenPos = -1
        self.actualToken = []

    #incompleto
    def match(self, matchString):
        tokenString = self.actualToken[0][0]

        if(tokenString == 'id' and matchString== 'id'):
            idIndex = self.actualToken[0][1]
            if(self.symbol_table.lookup(idIndex)):
                return True
        elif(tokenString == 'number' and matchString== 'number'):
            value = self.actualToken[0][1]
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
            print(f"[Token Atual]: {self.actualToken}")
            
        else:
            self.actualToken = None
    
    #melhorar tratativas de erros
    def start(self):
        if self.program():
            print("\033[92m[ok] Execução bem-sucedida: Deu bom!\033[0m")  
            return True
        else:
            print("\033[91m[err] Execução falhou: Deu ruim.\033[0m")  
            return False

    # ================= Descrição BNF da Linguagem Simplificada ===================================== #
    
    def program(self):
        self.getNextToken()
        
        # Processa todas as sub-rotinas (funções ou procedimentos)
        while self.type() or self.match('void'):
            if not self.subRoutineStep():
                return False
            # Avança para o próximo token para verificar mais sub-rotinas
            self.getNextToken()
        
        # Processa o corpo principal (mainBody)
        if self.mainBody():
            return True  # Retorna sucesso se o corpo principal foi processado corretamente
        
        return False  # Falha se não encontrou ou não processou corretamente

        
    
    def mainBody(self):
        if(self.match("meme")):
            self.getNextToken()

            if(self.body()):
                return True
        return False 
    
    def body(self):
        #Valida se termina começa com "{"
        if(self.match("{")):
            self.getNextToken()

            #Valida se tem variáveis declaradas [<variable-declaration-step>]
            if(self.type()):
                if(self.declarationVariableStep()):
                    
                    while self.type():
                        if self.declarationVariableStep():
                            pass
                        else:
                            return False

            if(self.statements()):
                if(self.match("}")):
                    return True
            else:
                return False
        return False

    #incompleto 
    def subRoutineStep(self):      
        if self.declarationFunctionProcedure():
            return True
        
        return False
    
    #incompleto
    def declarationVariableStep(self):
    
        if self.declarationVariable():
            return True
        return False
    
    # ==================================== DECLARAÇÕES =============================================== #
    # ok
    def type(self):
        if(self.match("int")):
            return True
        elif(self.match("bruh")):
            return True
        
        return False
    
    # Ok
    def declarationVariable(self):
        if self.type(): 
            self.getNextToken()  

            if self.identifier():  
                self.getNextToken()  

                if self.match("="):
                    # Errado, precisa pegar oque esta antes do =
                    if self.assignStatement():  
                        self.getNextToken()  
                        #if not self.match(";"):  
                        #    return False
                        #self.getNextToken() 
                        return True

                if self.match(";"):
                    self.getNextToken()     
                    return True
            return False
        return False
    
    def declarationParameters(self):
        if(self.type()):
            self.getNextToken()
            if(self.identifier()):
                self.getNextToken()
                
            while self.match(','):
                self.getNextToken()
                self.declarationParameters()
                
            return True
        
        return False
    
    # <declaration-procedure> ::= void hora_do_show <identifier> ([<declaration-parameters>]*) <body>
    def declarationFunctionProcedure(self):
    # Procedimento com 'void hora_do_show'
        if self.match("void"):
            self.getNextToken()
            if self.match('hora_do_show'):
                self.getNextToken()
                if self.identifier():  # Nome do procedimento
                    self.getNextToken()
                    if self.match('('):  # Início dos parâmetros
                        self.getNextToken()
                        if self.declarationParameters():  # Verifica os parâmetros
                            pass  # Parâmetros são opcionais
                        if self.match(')'):  # Fechamento dos parâmetros
                            self.getNextToken()
                            if self.body():  # Corpo do procedimento
                                return True
            return False

        # Função com tipo de retorno e 'hora_do_show'
        if self.type():  # Tipo de retorno
            self.getNextToken()
            if self.match('hora_do_show'):
                self.getNextToken()
                if self.identifier():  # Nome da função
                    self.getNextToken()
                    if self.match('('):  # Início dos parâmetros
                        self.getNextToken()
                        if self.declarationParameters():  # Verifica os parâmetros
                            pass  # Parâmetros são opcionais
                        if self.match(')'):  # Fechamento dos parâmetros
                            self.getNextToken()
                            if self.body():  # Corpo da função
                                return True
        return False

            
    
    # ==================================== COMANDOS =============================================== #
    
    def statements(self):
        if(self.statement()):
            hasStatementsLeft = True
            while(hasStatementsLeft):
                self.getNextToken()
                
                if(self.match(";")):
                    self.getNextToken()
                    
                    if(self.match("}")):
                        return True
                    
                    if not self.statement():
                        return False
                else:
                    hasStatementsLeft = False
            return True
        return False
    
    #completo mas precisar testar todos os casos
    def statement(self):
        if(self.jumpStopStatement()):
            return True
        if(self.conditionStatement()):
            return True
        elif(self.loopStatement()):
            return True
        elif(self.printStatement()):
            return True
        elif(self.readStatement()):
            return True
        elif(self.callOrAssignStatement()):
            return True
        elif(self.returnStatement()):
            return True
        return False
    
    #incompleto
    def conditionStatement(self):
        if(self.match("irineu_voce_sabe")):
            self.getNextToken()

            if(self.match("(")):
                self.getNextToken()

                if(self.expression()):
                    if(self.match(")")):
                        self.getNextToken()

                        if(self.body()):
                            self.getNextToken() #problema
                            if(self.match("nem_eu")):
                                self.getNextToken()

                                if(self.body()):
                                    return True

                            #validar como corrigir
                            return True
        return False
    
    #incompleto
    def loopStatement(self):
        #validar se vale a pena fazer o do-while
        if(self.match("here_we_go_again")):
            self.getNextToken()

            if(self.match("(")):
                self.getNextToken()

                if(self.expression()):
                    if(self.match(")")):
                        self.getNextToken()

                        #validar como fazer um body diferente para permitir break e continue
                        if(self.body()):
                            return True
        return False
    
    def jumpStopStatement(self):
        if(self.match("papapare")):
            return True
        if(self.match("ate_outro_dia")):
            return True
        return False
    
    def printStatement(self):
        if(self.match("amostradinho")):
            self.getNextToken()

            if(self.match("(")):
                self.getNextToken()
                
                if(self.expression()):
                    if(self.match(")")):
                        return True
        return False
    
    def readStatement(self):
        if(self.match("casca_de_bala")):
            self.getNextToken()

            if(self.match("(")):
                self.getNextToken()

                if(self.identifier()):
                    self.getNextToken()
                    
                    if(self.match(")")):
                        return True
        return False
    
    def returnStatement(self):
        if(self.match("receba")):
            self.getNextToken()

            if(self.expression()):
                return True
        return False
    
    #não testado ainda por causa de declarationParameters
    def callOrAssignStatement(self):
        if(self.identifier()):
            self.getNextToken()

            #assignStatement
            if(self.match("=")):
                self.getNextToken()

                if(self.expression()):
                    return True
            elif(self.callFunctionStatement()):
                return True
        
        return False

    def assignStatement(self):
        if(self.match("=")):
            self.getNextToken()

            if(self.expression()):
                return True
        return False
    
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
        if(self.simpleExpression()):
            # self.getNextToken()
            
            if(self.assignOperator()):
                self.getNextToken()
                
                if(self.simpleExpression()):
                    return True
            else:
                return True
            return True
        return False

    def simpleExpression(self):
        self.unaryOperator()
        
        if(self.term()):
            return True
        
        return False

    def unaryOperator(self):
        if(self.match("+")):
            self.getNextToken()
            return True
        elif(self.match("-")):
            self.getNextToken()
            return True
        elif(self.match("!")):
            self.getNextToken()
            return True

        return False
    
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
        if(self.factor()):
            while self.match('+') or self.match('-') or self.match('*') or self.match('/'):
                self.getNextToken()
                self.term()

            return True
        return False
    
    #incompleto
    def factor(self):
        if(self.match("real")):
            self.getNextToken()
            return True
        elif(self.match("barca")):
            self.getNextToken()
            return True
        elif(self.number()):
            self.getNextToken()
            return True
        elif(self.identifier()):
            self.getNextToken()
            
            if(self.callFunctionStatement()):
                self.getNextToken()
                return True
            return True
        elif(self.match("(")):
            self.getNextToken()
            if(self.expression()):
                if(self.match(")")):
                    self.getNextToken()
                    return True

        return False

    # ==================================== NÚMEROS E IDENTIFICADORES =============================================== #
    
    def identifier(self):
        if(self.match("id")):
            return True
        
        return False
    
    def number(self):
        if(self.match('number')):
            return True
        
        return False
    
    def colon(self):
        if(self.match(";")):
            return True
        
        return False
    
    def comment(self):
        if(self.match("//")):
            return True
        
        return False