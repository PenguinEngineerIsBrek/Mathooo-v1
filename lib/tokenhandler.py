# Imports
from string_with_arrows import *
from variables import *
from keywords_iden import *
from operators import *
from error_management import *
from constants import *
from position import *
from logical_nodes import *
from context import *
from runtime_result import *
import math


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

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

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
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
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
                    tokens.append(Token(T_COMP, pos_start=self.pos))
                    self.advance()
                else:
                    tokens.append(Token(T_EQU, pos_start=self.pos))
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

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        tok_type = T_KEYWORD if id_str in KEYWORDS else T_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)





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
        
        elif tok.type == T_IDENTIFIER:
            res.register(self.advance())
            return res.success(VarAccessNode(tok))

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
        res = ParseResult()
        if self.current_tok.matches(T_KEYWORD, 'var'):
            res.register(self.advance())
            if self.current_tok.type != T_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Expected identifier'
                ))
            var_name = self.current_tok
            res.register(self.advance())
            if self.current_tok.type != T_EQU:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '='"
                ))
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))
        return self.bin_op(self.term, (T_ADD, T_MIN, T_COMP))

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
        elif node.op_token.type == T_COMP:
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
