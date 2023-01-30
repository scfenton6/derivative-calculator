'''
Collection of utils used in the symbolic
differentiation tool and in the interpreter.
'''

from derivative_calculator.math_parser import Num, Var, UnaryOp, BinOp
from derivative_calculator.tokenizer import Token, INTEGER, PLUS, MINUS, MUL, DIV, POW, FUNC


def binOp_type(node, OP):
    return isinstance(node, BinOp) and node.op.type == OP


def is_number(node):
    return isinstance(node, Num)


def is_zero(node):
    return is_number(node) and node.value == 0


def is_one(node):
    return is_number(node) and node.value == 1


def is_var(node):
    return isinstance(node, Var)


def is_atomic(node):
    return is_number(node) or is_var(node) or is_func(node)


def same_op(x, y):
    return x.op.type == y.op.type


def same_atom(x, y):
    return x.value == y.value


def same_num(x, y):
    return x.value == y.value


def same_var(x, y):
    return x.value == y.value


def is_prefix_sign(node):
    return isinstance(node, UnaryOp) and node.op.type in (PLUS, MINUS)


def is_func(node):
    return isinstance(node, UnaryOp) and node.op.type == FUNC


def is_sum(node):
    return isinstance(node, BinOp) and node.op.type == PLUS


def is_substr(node):
    return isinstance(node, BinOp) and node.op.type == MINUS


def is_prod(node):
    return isinstance(node, BinOp) and node.op.type == MUL


def is_div(node):
    return isinstance(node, BinOp) and node.op.type == DIV


def is_pow(node):
    return isinstance(node, BinOp) and node.op.type == POW


def simplifyPrefixSign(node):
    op = node.op.type
    minus_counter = 1 if op == MINUS else 0
    node_child = node.expr
    while isinstance(node_child, UnaryOp):
        if node_child.op.type == MINUS:
            minus_counter += 1
        node_child = node_child.expr
    # at this point we know that node_child cannot be of the type UnaryOp
    sign = '-' if minus_counter % 2 == 1 else '+'
    # we return either a number or a prefix sign expression whose
    # argument is not a prefix sign expression
    if is_number(node_child):
        if sign == '-':
            return Num(Token(INTEGER, -1*node_child.value))
        return Num(Token(INTEGER, node_child.value))
    if sign == '-':
        return UnaryOp(Token(MINUS, '-'), node_child)
    return UnaryOp(Token(PLUS, '+'), node_child)


def make_sum(x, y):
    if is_prefix_sign(x):
        x = simplifyPrefixSign(x)

    if is_prefix_sign(y):
        y = simplifyPrefixSign(y)

    if is_number(x) and is_number(y):
        return Num(Token(INTEGER, x.value + y.value))

    if is_zero(x):
        return y

    if is_zero(y):
        return x
    return BinOp(x, Token(PLUS, '+'), y)


def make_substr(x, y):
    if is_prefix_sign(x):
        x = simplifyPrefixSign(x)

    if is_prefix_sign(y):
        y = simplifyPrefixSign(y)

    if is_number(x) and is_number(y):
        return Num(Token(INTEGER, x.value - y.value))

    if is_zero(x):
        return UnaryOp(op=Token(MINUS, '-'), expr=y)

    if is_zero(y):
        return x

    return BinOp(x, Token(MINUS, '-'), y)


def make_prod(x, y):
    if is_prefix_sign(x):
        x = simplifyPrefixSign(x)

    if is_prefix_sign(y):
        y = simplifyPrefixSign(y)

    if is_number(x) and is_number(y):
        return Num(Token(INTEGER, x.value * y.value))

    if is_zero(x) or is_zero(y):
        return Num(Token(INTEGER, 0))

    if is_one(x):
        return y

    if is_one(y):
        return x

    return BinOp(x, Token(MUL, '*'), y)


def make_div(x, y):
    if is_prefix_sign(x):
        x = simplifyPrefixSign(x)

    if is_prefix_sign(y):
        y = simplifyPrefixSign(y)

    if (is_number(y) and y.value == 0):
        raise Exception('Error: division by zero')

    if (is_number(x) and x.value == 0):
        return Num(Token(INTEGER, 0))

    if (is_number(y) and y.value == 1):
        return x

    return BinOp(x, Token(DIV, '/'), y)


def make_power(x, y):
    if is_prefix_sign(x):
        x = simplifyPrefixSign(x)

    if is_prefix_sign(y):
        y = simplifyPrefixSign(y)

    if is_number(x) and is_number(y):
        return Num(Token(INTEGER, x.value ** y.value))

    if is_one(x) or is_zero(y):
        return Num(Token(INTEGER, 1))

    if is_zero(x):
        return Num(Token(INTEGER, 0))

    if is_one(y):
        return x

    return BinOp(x, Token(POW, '**'), y)


def make_func(func, arg):
    return UnaryOp(Token(FUNC, func), arg)
