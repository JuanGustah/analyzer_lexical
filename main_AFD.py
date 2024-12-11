class Lexer:
    def __init__(self, file_path: str):
        self.file_path = file_path

        # variáveis de controle do Lexer
        self.head_position = 0
        self.num_line = 1
        self.line = ''

        # Idealmente uma tupla com token, valor e linha
        self.tokens = []

        # bootstrap
        self.main_loop()

    def main_loop(self):
        # Lê arquivo
        file = open("code.meme", "r")

        # Lê linha a linha
        self.line = file.readline()

        # loop principal
        while self.line != "":
            # valida se aquela linha tem que ser analizada (linha em branco) e se já acabou a linha
            self.check_line()

            # Lê linha a linha
            self.line = file.readline()

            # Reseta o cabeçote da máquina pro inicio da nova linha
            self.num_line += 1
            self.head_position = 0

        # Não vazar memória, se bem que é python e esse lixo vaza de toda forma
        file.close()

    # Lê o char no cabeçote
    def read_actual_char(self):
        print("CHAR IS",self.line[self.head_position])
        return self.line[self.head_position]
    
    # Avança o cabeçote na linha lida
    def forward_head(self):
        self.head_position += 1
    
    def check_line(self):
        # Valida se não chegou ao fim da linha
        while(self.head_position<len(self.line) and self.read_actual_char() != '\n'):
            # Valida se ele reconheçou algum lexema
            if not self.q0():
                raise ValueError(f"Token inválido na linha {self.num_line}:{self.line[self.head_position]}")

    # ponto inicial do autômato, deve possuir todos os terminais
    def q0(self):
        d = {'i': self.q1, '(': self.q2, ')': self.q3, '{': self.q4, '}': self.q5, 'b': self.q8, 'n': self.q27, 'c': self.q33, 's': self.q46, 'a': self.q59, 'r': self.q71, 'p': self.q77, 'm': self.q97}
        char = self.read_actual_char()
        
        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False

    # estado que finaliza um "if"
    def q1(self):
        d = {'n': self.q6, 'r': self.q12}
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
    
    # estado que lê um "("
    def q2(self):
        self.tokens.append(('(', self.num_line))
        return True
    
    # estado que lê um ")"
    def q3(self):
        self.tokens.append((')', self.num_line))
        return True
    
    # estado que lê um "{"
    def q4(self):
        self.tokens.append(('{', self.num_line))
        return True
    
    # estado que lê um "}"
    def q5(self):
        self.tokens.append(('}', self.num_line))
        return True
    
    def q6(self):
        d = {'t': self.q7}
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
        
    def q7(self):
        self.tokens.append(('INT', self.num_line))
        #self.forward_head()
        return True
    
    def q8(self):
        d = {'r': self.q9}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
        
    def q9(self):
        d = {'u': self.q10}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
        
    def q10(self):
        d = {'h': self.q11}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
        
    def q11(self):
        self.tokens.append(('BRUH', self.num_line))
        #self.forward_head()
        return True
    
    def q12(self):
        d = {'i': self.q13}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
        
    def q13(self):
        d = {'n': self.q14}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
        
    def q14(self):
        d = {'e': self.q15}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
        
    def q15(self):
        d = {'u': self.q16}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
        
    def q16(self):
        d = {'_': self.q17}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
        
    def q17(self):
        d = {'v': self.q18}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
        
    def q18(self):
        d = {'o': self.q19}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
        
    def q19(self):
        d = {'c': self.q20}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
      
    def q20(self):
        d = {'e': self.q21}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False      
    def q21(self):
        d = {'_': self.q22}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False    
    def q22(self):
        d = {'s': self.q23}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
    def q23(self):
        d = {'a': self.q24}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
    def q24(self):
        d = {'b': self.q25}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
    def q25(self):
        d = {'e': self.q26}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
        
    def q26(self):
        self.tokens.append(('IRINEU_VOCE_SABE', self.num_line))
        #self.forward_head()
        return True
    def q27(self):
        d = {'e': self.q28}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
    def q28(self):
        d = {'m': self.q29}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
    def q29(self):
        d = {'_': self.q30}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
    def q30(self):
        d = {'e': self.q31}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
    def q31(self):
        d = {'u': self.q32}
        
        char = self.read_actual_char()

        if char in d:
            self.head_position +=1
            return d[char]()
        else:
            return False
    def q32(self):
        self.tokens.append(('NEM_EU', self.num_line))
        #self.forward_head()
        return True
    def q33(self):
        d = {'a': self.q34}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q34(self):
        d = {'s': self.q35}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q35(self):
        d = {'c': self.q36}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q36(self):
        d = {'a': self.q37}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q37(self):
        d = {'_': self.q38}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q38(self):
        d = {'d': self.q39}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q39(self):
        d = {'e': self.q40}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q40(self):
        d = {'_': self.q41}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q41(self):
        d = {'b': self.q42}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q42(self):
        d = {'a': self.q43}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q43(self):
        d = {'l': self.q44}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q44(self):
        d = {'a': self.q45}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q45(self):
        self.tokens.append(('CASCA_DE_BALA', self.num_line))
        return True

    def q46(self):
        d = {'u': self.q47}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q47(self):
        d = {'r': self.q48}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q48(self):
        d = {'p': self.q49}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q49(self):
        d = {'r': self.q50}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q50(self):
        d = {'i': self.q51}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q51(self):
        d = {'s': self.q52}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q52(self):
        d = {'e': self.q53}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q53(self):
        d = {'_': self.q54}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q54(self):
        d = {'m': self.q55}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q55(self):
        d = {'t': self.q56}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q56(self):
        d = {'f': self.q57}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q57(self):
        d = {'k': self.q58}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q58(self):
        self.tokens.append(('SURPRISE_MTFK', self.num_line))
        return True    
        
    def q59(self):
        d = {'m': self.q60, 't': self.q85}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q60(self):
        d = {'o': self.q61}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q61(self):
        d = {'s': self.q62}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q62(self):
        d = {'t': self.q63}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q63(self):
        d = {'r': self.q64}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q64(self):
        d = {'a': self.q65}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q65(self):
        d = {'d': self.q66}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q66(self):
        d = {'i': self.q67}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q67(self):
        d = {'n': self.q68}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q68(self):
        d = {'h': self.q69}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q69(self):
        d = {'o': self.q70}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q70(self):
        self.tokens.append(('AMOSTRADINHO', self.num_line))
        return True
    def q71(self):
        d = {'e': self.q72}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q72(self):
        d = {'c': self.q73}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q73(self):
        d = {'e': self.q74}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q74(self):
        d = {'b': self.q75}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q75(self):
        d = {'a': self.q76}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q76(self):
        self.tokens.append(('RECEBA', self.num_line))
        return True
    
    def q77(self):
        d = {'a': self.q78}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q78(self):
        d = {'p': self.q79}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q79(self):
        d = {'a': self.q80}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q80(self):
        d = {'p': self.q81}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q81(self):
        d = {'a': self.q82}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q82(self):
        d = {'r': self.q83}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q83(self):
        d = {'e': self.q84}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q84(self):
        self.tokens.append(('PAPAPARE', self.num_line))
        return True

    def q85(self):
        d = {'e': self.q86}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q86(self):
        d = {'_': self.q87}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q87(self):
        d = {'o': self.q88}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q88(self):
        d = {'u': self.q89}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q89(self):
        d = {'t': self.q90}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q90(self):
        d = {'r': self.q91}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q91(self):
        d = {'o': self.q92}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q92(self):
        d = {'_': self.q93}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q93(self):
        d = {'d': self.q94}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q94(self):
        d = {'i': self.q95}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q95(self):
        d = {'a': self.q96}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q96(self):
        self.tokens.append(('ATE_OUTRO_DIA', self.num_line))
        return True
    
    def q97(self):
        d = {'e': self.q98}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q98(self):
        d = {'m': self.q99}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q99(self):
        d = {'e': self.q100}

        char = self.read_actual_char()

        if char in d:
            self.head_position += 1
            return d[char]()
        else:
            return False

    def q100(self):
        self.tokens.append(('MEME', self.num_line))
        return True

    def display_tokens(self):
        print("\nTokens:")
        for token in self.tokens:
            print(token)

# Teste do Lexer
if __name__ == "__main__":
    analisador_lexico = Lexer("code.meme")
    analisador_lexico.display_tokens()