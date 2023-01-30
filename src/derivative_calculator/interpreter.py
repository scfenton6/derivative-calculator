'''
Interpreter that visits an abstract syntax tree representing a
mathematical function and returns the function in string format.
Main program is Interpreter.interpret.
'''

from derivative_calculator.tokenizer import PLUS, MINUS, MUL, DIV, POW, FUNC
import derivative_calculator.utils as utils


class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name)
        return visitor(node)


class Interpreter(NodeVisitor):
    def __init__(self):
        self.prec = {PLUS: 1, MINUS: 1, MUL: 2, DIV: 2, POW: 3, FUNC: 4}

    def binOpHelper(self, node, op, prec):
        '''
        Adds parentheses to binary operation if needed
        '''
        result = ''
        if (not utils.is_atomic(node.left) and
                self.prec[node.left.op.type] < prec):
            result += r'(%s)%s' % (self.visit(node.left), op)
        else:
            result += r'%s%s' % (self.visit(node.left), op)
        if (not utils.is_atomic(node.right) and
                self.prec[node.right.op.type] < prec):
            result += r'(%s)' % self.visit(node.right)
        else:
            result += r'%s' % self.visit(node.right)
        return result

    def visit_BinOp(self, node):
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
            if utils.is_number(left) and utils.is_number(right):
                return str(left.value + right.value)
            if utils.is_zero(left):
                return str(self.visit(right))
            if utils.is_zero(right):
                return str(self.visit(left))
            return self.binOpHelper(node, '+', 1)

        if utils.is_substr(node):
            if utils.is_number(left) and utils.is_number(right):
                return str(left.value - right.value)
            if utils.is_zero(left):
                return r'-(%s)' % self.visit(right)
            if utils.is_zero(right):
                return str(self.visit(left))
            return self.binOpHelper(node, '-', 1)

        elif utils.is_prod(node):
            if utils.is_number(left) and utils.is_number(right):
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
            if utils.is_number(left) and utils.is_number(right):
                return str(left.value ** right.value)
            if (utils.is_one(left) or utils.is_zero(right)):
                return '1'
            if utils.is_zero(left):
                return '0'
            if utils.is_one(right):
                return str(self.visit(left))
            return self.binOpHelper(node, '**', 3)

    def visit_UnaryOp(self, node):
        op = node.op.value
        if utils.is_prefix_sign(node):
            simplified_node = utils.simplifyPrefixSign(node)
            if utils.is_number(simplified_node):
                return str(simplified_node.value)
            simpl_node_op = simplified_node.op.value
            if simpl_node_op == '-':
                if utils.is_atomic(simplified_node):
                    return r'-%s' % self.visit(simplified_node)
                return r'-(%s)' % self.visit(simplified_node)
            else:
                return str(self.visit(simplified_node))

        if utils.is_func(node):
            # return function with argument enclosed in parentheses
            return r'%s(%s)' % (op, self.visit(node.expr))

    def visit_Num(self, node):
        return str(node.value)

    def visit_Var(self, node):
        return str(node.value)

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        return self.visit(tree)
