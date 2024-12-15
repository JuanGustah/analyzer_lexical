class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.actualTokenPos = -1
        self.actualToken = []

    #incompleto
    def match(self, matchString):
        tokenString = self.actualToken[0][0]

        if(tokenString == 'id'):
            #lógica de ID (olhar tabela de simbolos)
            return True
        elif(tokenString == 'number'):
            #lógica de number (olhar se tem valor)
            return True
        elif(tokenString == matchString):
            return True
        
        return False
    
    def getNextToken(self):
        zeroIndexLength = len(self.tokens) - 1

        if(self.actualTokenPos < zeroIndexLength):
            self.actualTokenPos += 1
            self.actualToken = self.tokens[self.actualTokenPos]
            #token atual sendo mostrado
            print(self.actualToken)
    
    #melhorar tratativas de erros
    def start(self):
        if self.program():
            return print("Deu bom")
        
        return print("Deu ruim")
    
    def program(self):
        self.getNextToken()

        if self.subRoutineStep():
            return True
        elif self.mainBody():
            return True
        return False

    #incompleto 
    # <sub-routine-step> ::= (<declaration-procedure>; | <declaration-fuction>;)
    # [ <declaration-procedure>; | <declaration-fuction>;]*
    def subRoutineStep(self):      
        return False
    
    # ==================================== DECLARAÇÕES =============================================== #
    
    def type(self):
        if(self.match("int")):
            return True
        elif(self.match("bruh")):
            return True
        
        return False
    
    # Fazer mais declarações
    def declarationVariable(self):
        if(self.type()):
            if(self.identifier()):
                if(self.colon()):
                    #if para declaration variable dnv
                    return True
        return False
    
    #incompleto
    def declarationVariableStep(self):
        if(self.type()):
            if(self.assignStatement()):
                if self.colon():
                    return True
                else:
                    self.getNextToken()
                    
                    self.declarationVariableStep()
        return False

    
    
    def declarationParameters(self):
        if(self.type()):
            self.getNextToken()
            if(self.identifier()):
                self.getNextToken()
                self.match(',')
                self.declarationParameters()
                
                
        return True
    
    # <declaration-procedure> ::= void hora_do_show <identifier> ([<declaration-parameters>]*) <body>
    def declarationProcedure(self):
        if(self.match("void")):
            self.getNextToken()
            if(self.match('hora_do_show')):
                self.getNextToken()
                if(self.identifier()):
                    self.getNextToken()
                    if(self.match('(')):
                        self.getNextToken()
                        self.declarationParameters()
                        
                        if(self.match(')')):
                            self.getNextToken()
                            if(self.body()):
                                return True
                        
        return False
            
    def declarationFunction(self):
        if(self.type()):
            self.getNextToken()
            if(self.match('hora_do_show')):
                self.getNextToken()
                if(self.identifier()):
                    self.getNextToken()
                    if(self.match('(')):
                        self.getNextToken()
                        self.declarationParameters()
                        
                        if(self.match(')')):
                            self.getNextToken()
                            if(self.body()):
                                return True
        return False
    
    
    # ==================================== MAIN =============================================== #
    
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
            self.declarationVariableStep()

            #Valida se tem comandos
            if(self.statements()):
                self.getNextToken()

                #Valida se termina com "}"
                if(self.match("}")):
                    return True
        return False
    


    def statements(self):
        if(self.statement()):
            hasStatementsLeft = True
            while(hasStatementsLeft):
                self.getNextToken()

                hasStatementsLeft = self.statement()

            return True
        return False
    
    #completo mas precisar testar todos os casos
    def statement(self):
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
        return False
    
    #incompleto
    def conditionStatement(self):
        #não tá lendo o ?
        if(self.match("irineu_voce_sabe")):
            self.getNextToken()

            if(self.match("(")):
                self.getNextToken()

                if(self.expression()):
                    self.getNextToken()
                    
                    if(self.match(")")):
                        self.getNextToken()

                        if(self.body()):
                            #verificar se vale a pena fazer o else

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
                    self.getNextToken()
                    
                    if(self.match(")")):
                        self.getNextToken()

                        #validar como fazer um body diferente para permitir break e continue
                        if(self.body()):
                            return True
        return False

    def printStatement(self):
        if(self.match("amostradinho")):
            self.getNextToken()

            if(self.match("(")):
                self.getNextToken()
                
                if(self.expression()):
                    self.getNextToken()
                    
                    if(self.match(")")):
                        self.getNextToken()

                        
                        if(self.match(";")):
                            return True
        return False
    
    #não testado ainda por causa de identifier
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
                            return True
        return False

    #não testado ainda por causa de identifier e declarationParameters
    def callOrAssignStatement(self):
        if(self.assignStatement()):
            return True
        elif(self.callFunctionStatement()):
            return True
        
        return False

    #não testado ainda por causa de identifier
    def assignStatement(self):
        if(self.identifier()):
            self.getNextToken()

            if(self.match("=")):
                self.getNextToken()

                if(self.expression()):
                    self.getNextToken()

                    if(self.match(";")):
                        return True
        return False
    
    #incompleto
    def callFunctionStatement(self):
        if(self.identifier()):
            self.getNextToken()

            if(self.match("(")):
                self.getNextToken()

                #finalizar
                # if(self.declarationParameters()):
                #     self.getNextToken()

                #     if(self.match(")")):
                #         self.getNextToken()

                #         if(self.match(";")):
                #             return True
        return False

    def returnStatement(self):
        if(self.match("receba")):
            self.getNextToken()

            if(self.expression()):
                self.getNextToken()

                if(self.match(";")):
                    return True

        return False

    #incompleto
    def expression(self):
        if(self.simpleExpression()):
            
            self.getNextToken()
            
            if(self.assignStatement()):
                self.getNextToken()
                
                if(self.simpleExpression()):
                    return True
            else:
                self.getPreviousToken()
                return True
            return True
        return False

    #incompleto
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

    #incompleto
    def term(self):
        if(self.factor()):
            # self.getNextToken()

            #verificar outros termos

            return True
        return False
    
    #incompleto
    def factor(self):
        if(self.identifier()):
            return True
        elif(self.match("real")):
            return True
        elif(self.match("barça")):
            return True

        return False

    #incompleto
    def identifier(self):
        if(self.match("id")):
            return True
        
        return False
    
    def colon(self):
        if(self.match(";")):
            return True
        
        return False