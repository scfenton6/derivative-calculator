'''
Interpreter that visits an abstract syntax tree representing a
mathematical function and returns the function in string format.
Main program is Interpreter.interpret.
'''

import typing
from derivative_calculator.tokenizer import PLUS, MINUS, MUL, DIV, POW, FUNC
import derivative_calculator.utils as utils
from derivative_calculator.math_parser import UnaryOp, BinOp, Num, Var

Node = typing.Union[UnaryOp, BinOp, Num, Var]


class NodeVisitor:
    def visit(self, node: Node) -> str:
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name)
        return visitor(node)


class Interpreter(NodeVisitor):
    def __init__(self) -> None:
        self.prec = {PLUS: 1, MINUS: 1, MUL: 2, DIV: 2, POW: 3, FUNC: 4}

    def binOpHelper(self, node: BinOp, op: str, prec: int) -> str:
        '''
        Adds parentheses to binary operation if needed
        '''
        result = ''
        left, right = node.left, node.right

        if (utils.is_rational_number(left) or
                (isinstance(left, (UnaryOp, BinOp)) and self.prec[left.op.type] < prec)):
            result += r'(%s)%s' % (self.visit(left), op)
        else:
            result += r'%s%s' % (self.visit(left), op)
        if (utils.is_rational_number(right) or
                (isinstance(right, (UnaryOp, BinOp)) and self.prec[right.op.type] < prec)):
            result += r'(%s)' % self.visit(right)
        else:
            result += r'%s' % self.visit(right)
        return result

    def visit_BinOp(self, node: BinOp) -> str:  # type: ignore[return]
        '''
        Tool for visiting a binary operation.
        We try to simplify the expression if
        possible, and if not we call the pertaining
        helper function.
        '''
        left, right = node.left, node.right

        # simplify left and right nodes in case they are prefix sign expressions
        if utils.is_prefix_sign(left):
            left = utils.simplifyPrefixSign(left)

        if utils.is_prefix_sign(right):
            right = utils.simplifyPrefixSign(right)

        if utils.is_sum(node):
            if isinstance(left, Num) and isinstance(right, Num):
                return str(left.value + right.value)
            if utils.is_zero(left):
                return str(self.visit(right))
            if utils.is_zero(right):
                return str(self.visit(left))
            return self.binOpHelper(node, '+', 1)

        if utils.is_substr(node):
            if isinstance(left, Num) and isinstance(right, Num):
                return str(left.value - right.value)
            if utils.is_zero(left):
                return r'-(%s)' % self.visit(right)
            if utils.is_zero(right):
                return str(self.visit(left))
            return self.binOpHelper(node, '-', 1)

        elif utils.is_prod(node):
            if isinstance(left, Num) and isinstance(right, Num):
                return str(left.value * right.value)
            if utils.is_zero(left) or utils.is_zero(right):
                return '0'
            if utils.is_one(left):
                return str(self.visit(right))
            if utils.is_one(right):
                return str(self.visit(left))
            return self.binOpHelper(node, '*', 2)

        elif utils.is_div(node):
            if utils.is_zero(left):
                return '0'
            if utils.is_one(right):
                return str(self.visit(left))
            return self.binOpHelper(node, '/', 4)

        elif utils.is_pow(node):
            if isinstance(left, Num) and isinstance(right, Num):
                return str(left.value ** right.value)
            if (utils.is_one(left) or utils.is_zero(right)):
                return '1'
            if utils.is_zero(left):
                return '0'
            if utils.is_one(right):
                return str(self.visit(left))
            return self.binOpHelper(node, '**', 3)

    def visit_UnaryOp(self, node: UnaryOp) -> str:  # type: ignore[return]
        if utils.is_prefix_sign(node):
            simpl_node: UnaryOp | Num = utils.simplifyPrefixSign(node)
            if isinstance(simpl_node, Num):
                return str(self.visit(simpl_node))
            else:
                sign = simpl_node.op.value
                if isinstance(simpl_node, BinOp):
                    return r'%s(%s)' % (sign, self.visit(simpl_node.expr))
                else:
                    return r'%s%s' % (sign, self.visit(simpl_node.expr))
        if utils.is_func(node):
            return r'%s(%s)' % (node.op.value, self.visit(node.expr))

    def visit_Num(self, node: Num) -> str:  # type: ignore[return]
        return str(node.value)

    def visit_Var(self, node: Var) -> str:  # type: ignore[return]
        return str(node.value)

    def interpret(self) -> str:
        tree = self.parser.parse()
        if tree is None:
            return ''
        return self.visit(tree)
