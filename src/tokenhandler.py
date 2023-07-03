# Operators
T_NUM = 'NUM'
T_DEC = 'FLOAT'
T_ADD = 'ADD'
T_MIN = 'MIN'
T_MUL = 'MUL'
T_DIV = 'DIV'
T_MOD = 'MOD'
T_EXP = 'EXP'
T_RPAREN = 'RPAREN'
T_LPAREN = 'LPAREN'
T_SQRT = 'SQRT'
T_EQU = 'EQU'
T_REM = 'REM'
T_EULER = 'e'
T_PI = 'PI'
T_LOG = 'LOG'
T_LN = 'LN'
T_INT = 'INTEG'
T_SIG = 'SIGMA'
T_PHI = 'PHI'
T_VAR = 'VAR'
T_DER = 'DER'

# Constants 
DIGITS = '0123456789'
VARIABLES = 'xyzwu'

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
                self.advance()
            elif self.current_char == 'd':
                self.advance()
                if self.current_char in VARIABLES:
                    tokens.append(T_DER + f" of {self.current_char}")
                    self.advance()
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
            elif self.current_char == "=":
                tokens.append(T_EQU)
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
        

class NumberNode:
    def __init__(self, token):
        self.token = token
        
    def __repr__(self):
        return f'{self.token}'

class BinaryNode:
    def __init__(self, op_token, left_node, right_node):
        self.op_token = op_token
        self.left_node = left_node
        self.right_node = right_node

    def __repr__(self):
        return f"({self.left_node}, {self.op_token}, {self.right_node})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.advance()

    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]

        return self.current_token
        
        
    def bin_operation(self, func, ops):
        left = func()

        while self.current_token.type in ops:
            operator = self.current_token
            self.advance()
            right = func()
            left = BinaryNode(operator,left,right)

        return left
        
    def parse(self):
        expr = self.expr()
        return expr
        
    def factor(self):
        token = self.current_token
        if token.type in (T_NUM,T_DEC):
            self.advance()
            return NumberNode(token)
        
    def term(self):
        return self.bin_operation(self.factor, (T_MUL,T_DIV))
        
    def expr(self):
        return self.bin_operation(self.term, (T_ADD,T_MIN))

# Running

def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    return ast, None