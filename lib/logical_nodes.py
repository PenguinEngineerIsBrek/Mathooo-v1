from error_management import *
import math
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

class IfNode:
	def __init__(self, cases, else_case):
		self.cases = cases
		self.else_case = else_case

		self.pos_start = self.cases[0][0].pos_start
		self.pos_end = (self.else_case or self.cases[len(self.cases) - 1][0]).pos_end

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

    def is_true(self):
        return self.value != 0

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
