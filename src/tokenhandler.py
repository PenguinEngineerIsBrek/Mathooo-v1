# Operators
T_NUM = 'NUM'
T_DEC = 'DEC'
T_ADD = 'ADD'
T_MIN = 'MIN'
T_MUL = 'MUL'
T_DIV = 'DIV'
T_MOD = 'MOD'
T_EXP = 'EXP'
T_RPAREN = 'RPAREN'
T_LPAREN = 'LPAREN'
T_SQRT = 'SQRT'

# Constants 
DIGITS = '0123456789'

# Errors
class Error:
    def __init__(self, err_name, details):
        self.err_name = err_name
        self.details = details
    
    def as_string(self):
        r = f'{self.err_name}:{self.details}'

class IllegalCharERR(Error):
    def __init__(self, details):
        super().__init__("Illegal Character Error", details)

# Classes
class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
    
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if(self.pos < len(self.text)) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(T_ADD))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(T_MIN))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(T_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(T_DIV))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(T_MOD))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(T_EXP))
                self.advance()
            elif self.current_char == '(':
                tokens.append(T_LPAREN)
                self.advance()
            elif self.current_char == ")":
                tokens.append(T_RPAREN)
                self.advance()
            else:
                char = self.current_char
                self.advance
                return [], IllegalCharERR("'" + char + "'")

        return tokens, None
    
    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if (self.current_char == '.'):
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if(dot_count == 0):
            return Token(T_NUM, int(num_str))
        else:
            return Token(T_DEC, float(num_str))
        

# Running

def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()

    return tokens, error