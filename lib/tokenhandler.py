# Imports
from string_with_arrows import *
import math

# The bane of my existence


class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


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
T_PI = 'PI'
T_E = 'e'
T_I = "i"
T_LOG = 'LOG'
T_LN = 'LN'
T_INT = 'INTEG'
T_SIG = 'SIGMA'
T_PHI = 'PHI'
T_VAR = 'VAR'
T_DER = 'DER'

T_EOF = 'EOF'

# Constants

DIGITS = '0123456789'
VARIABLES = 'xyzwu'

#Symbols

sqrt = '√'

# Errors


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + \
            string_with_arrows(self.pos_start.ftxt,
                               self.pos_start, self.pos_end)
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)


class RTError(Error):
	def __init__(self, pos_start, pos_end, details, context):
		super().__init__(pos_start, pos_end, 'Runtime Error', details)
		self.context = context

	def as_string(self):
		result  = self.generate_traceback()
		result += f'{self.error_name}: {self.details}'
		result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
		return result

	def generate_traceback(self):
		result = ''
		pos = self.pos_start
		ctx = self.context

		while ctx:
			result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
			pos = ctx.parent_entry_pos
			ctx = ctx.parent

		return 'Traceback (most recent call last):\n' + result


# Classes


class Token:
    def __init__(self, type, value=None, pos_start=None, pos_end=None):
        self.type = type
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        if pos_end:
            self.pos_end = pos_end

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(T_ADD, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(T_MIN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(T_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(T_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(T_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(T_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(T_EXP, pos_start=self.pos))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(T_MOD, pos_start=self.pos))
                self.advance()
            elif self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(T_EQU, pos_start=self.pos))
                    self.advance()
                else:
                    pos_start = self.pos.copy()
                    char = self.current_char
                    self.advance()
                    return [], InvalidSyntaxError(pos_start, self.pos, "Can not set the value of a constant, did you mean '=='?")
            elif self.current_char == 'p':
                self.advance()
                if self.current_char == 'i':
                    tokens.append(Token(T_PI, pos_start=self.pos))
                    self.advance()
                else:
                    pos_start = self.pos.copy()
                    char = self.current_char
                    self.advance()
                    return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
            elif self.current_char == 'e':      
                tokens.append(Token(T_E, pos_start=self.pos))        
                self.advance()
            elif self.current_char == 'i':
                tokens.append(Token(T_I, pos_start=self.pos))        
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(T_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(T_NUM, int(num_str), pos_start, self.pos)
        else:
            return Token(T_DEC, float(num_str), pos_start, self.pos)


class NumberNode:
    def __init__(self, token):
        self.token = token
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'{self.token}'


class BinaryNode:
    def __init__(self, op_token, left_node, right_node):
        self.op_token = op_token
        self.left_node = left_node
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f"({self.left_node}, {self.op_token}, {self.right_node})"


class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f"({self.op_tok}, {self.node})"

class Complex(complex):
  def __repr__(self):
    if self.real:
      if self.imag:
        return f"{int(self.real)} + {int(self.imag)}i"
      else:
         return f"{int(self.real)}"
    else:
      if self.imag:
        return f"{int(self.imag)}i"
      else:
        return '0'

  def __str__(self):
    return self.__repr__()
  


# Parse result(also the bane of my existence)


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node

        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self, ):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != T_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected a valid operator"
            ))
        return res

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (T_ADD, T_MIN):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))

        elif tok.type in (T_NUM, T_DEC):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == T_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == T_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))
        elif tok.type == T_E:
            res.register(self.advance())
            return res.success(ENode(tok.value))
        elif tok.type == T_PI:
            res.register(self.advance())
            return res.success(PINode(tok.value))
        elif tok.type == T_I:
            res.register(self.advance())
            return res.success(INode(tok.value))
        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int or float"
        ))


    def expcon(self):
        return self.bin_op(self.factor, (T_EXP, T_E))

    def term(self):
        return self.bin_op(self.expcon, (T_MUL, T_DIV, T_MOD))

    def expr(self):
        return self.bin_op(self.term, (T_ADD, T_MIN, T_EQU))

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error:
                return res
            left = BinaryNode(op_tok, left, right)

        return res.success(left)

# Number

class returned_string:
    def __init__(self, value):
        self.value = value
        self.set_pos()
    
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def set_context(self, context=None):
        self.context = context
        return self


    def __repr__(self):
        return str(self.value)

class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subbed_to(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multiplied_by(self, other):
        if isinstance(other, PINode): 
            return Number(self.value * math.pi).set_context(self.context), None
        elif isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Division By Zero',
                    self.context
                )
            return Number(self.value / other.value).set_context(self.context), None

    def powered_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None

    def mod_by(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value).set_context(self.context), None

    def equal_to(self, other):
        if isinstance(other, Number):
            if self.value == other.value:
                return returned_string("True").set_context(self.context), None
            return returned_string("False").set_context(self.context), None


    def __repr__(self):

        return str(self.value)

class ENode(Number):
    def __init__(self, value, pos_start=None, pos_end=None):
         self.value = value
         self.pos_start = pos_start
         self.pos_end = pos_end

class PINode(Number):
    def __init__(self, value, pos_start=None, pos_end=None):
         self.value = value
         self.pos_start = pos_start
         self.pos_end = pos_end

class INode(Number):
    def __init__(self, value, pos_start=None, pos_end=None):
         self.value = value
         self.pos_start = pos_start
         self.pos_end = pos_end

#Context

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos

# Interpreter


class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_BinaryNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        right = res.register(self.visit(node.right_node, context))
        if res.error:
            return res
        if node.op_token.type == T_ADD:
            result, error = left.added_to(right)
        elif node.op_token.type == T_MIN:
            result, error = left.subbed_to(right)
        elif node.op_token.type == T_MUL:
            result, error = left.multiplied_by(right)
        elif node.op_token.type == T_DIV:
            result, error = left.divided_by(right)
        elif node.op_token.type == T_EXP:
            result, error = left.powered_by(right)
        elif node.op_token.type == T_MOD:
            result, error = left.mod_by(right)
        elif node.op_token.type == T_EQU:
            result, error = left.equal_to(right)
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error:
            return res

        if node.op_tok.type == T_MIN:
            number, error = number.multiplied_by(Number(-1))

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_ENode(self, node, context):
        return RTResult().success(
            Number(math.e).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    def visit_PINode(self, node, context):
        return RTResult().success(
            Number(math.pi).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    def visit_INode(self, node, context):
        return RTResult().success(
            Number(Complex(1j)).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
# RT


class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error:
            self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

# Running


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    interpreter = Interpreter()
    context = Context('<program>')
    result = interpreter.visit(ast.node, context)

    return result.value, result.error