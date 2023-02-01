'''
Collection of utils used in the symbolic
differentiation tool and in the interpreter.
'''

import typing
from derivative_calculator.math_parser import Num, Var, UnaryOp, BinOp
from derivative_calculator.tokenizer import Token, INTEGER, PLUS, MINUS, MUL, DIV, POW, FUNC

Node = typing.Union[UnaryOp, BinOp, Num, Var]


def binOp_type(node: Node, OP: str) -> bool:
    return isinstance(node, BinOp) and node.op.type == OP


def is_number(node: Node) -> bool:
    return isinstance(node, Num)


def is_zero(node: Node) -> bool:
    return isinstance(node, Num) and node.value == 0


def is_one(node: Node) -> bool:
    return isinstance(node, Num) and node.value == 1


def is_var(node: Node) -> bool:
    return isinstance(node, Var)


def same_var(x: Node, y: Node) -> bool:
    return (isinstance(x, Var)
            and isinstance(y, Var)) and x.value == y.value


def is_prefix_sign(node: Node) -> bool:
    return isinstance(node, UnaryOp) and node.op.type in (PLUS, MINUS)


def is_func(node: Node) -> bool:
    return isinstance(node, UnaryOp) and node.op.type == FUNC


def is_sum(node: Node) -> bool:
    return isinstance(node, BinOp) and node.op.type == PLUS


def is_substr(node: Node) -> bool:
    return isinstance(node, BinOp) and node.op.type == MINUS


def is_prod(node: Node) -> bool:
    return isinstance(node, BinOp) and node.op.type == MUL


def is_div(node: Node) -> bool:
    return isinstance(node, BinOp) and node.op.type == DIV


def is_pow(node: Node) -> bool:
    return isinstance(node, BinOp) and node.op.type == POW


def is_rational_number(node: BinOp) -> bool:
    return is_div(node) and (is_number(node.left) and is_number(node.right))


def simplifyPrefixSign(node: UnaryOp) -> typing.Union[Num, UnaryOp]:
    plus_token = Token(PLUS, '+')
    minus_token = Token(MINUS, '-')
    prefixes: tuple[str, str] = (plus_token.value, minus_token.value)
    minus_counter = 0
    while is_prefix_sign(node):
        if node.op.type == MINUS:
            minus_counter += 1
        node = node.expr
    # at this point we know that node cannot be prefix sign expression
    sign = prefixes[minus_counter % 2]
    if isinstance(node, Num):
        prefix_sign = -1 if sign == '-' else 1
        token_value: int = prefix_sign * node.value
        return Num(Token(INTEGER, token_value))
    else:
        curr_token: Token = minus_token if sign == '-' else plus_token
        return UnaryOp(curr_token, node)


def make_sum(x: Node, y: Node) -> Node:
    if isinstance(x, UnaryOp) and x.op.type in (PLUS, MINUS):
        x = simplifyPrefixSign(x)

    if isinstance(y, UnaryOp) and y.op.type in (PLUS, MINUS):
        y = simplifyPrefixSign(y)

    if isinstance(x, Num) and isinstance(y, Num):
        return Num(Token(INTEGER, x.value + y.value))

    if isinstance(x, Num) and x.value == 0:
        return y

    if isinstance(y, Num) and y.value == 0:
        return x
    return BinOp(x, Token(PLUS, '+'), y)


def make_substr(x: Node, y: Node) -> Node:
    if isinstance(x, UnaryOp) and x.op.type in (PLUS, MINUS):
        x = simplifyPrefixSign(x)

    if isinstance(y, UnaryOp) and y.op.type in (PLUS, MINUS):
        y = simplifyPrefixSign(y)

    if isinstance(x, Num) and isinstance(y, Num):
        return Num(Token(INTEGER, x.value - y.value))

    if isinstance(x, Num) and x.value == 0:
        return UnaryOp(op=Token(MINUS, '-'), expr=y)

    if isinstance(y, Num) and y.value == 0:
        return x

    return BinOp(x, Token(MINUS, '-'), y)


def make_prod(x: Node, y: Node) -> Node:
    if isinstance(x, UnaryOp) and x.op.type in (PLUS, MINUS):
        x = simplifyPrefixSign(x)

    if isinstance(y, UnaryOp) and y.op.type in (PLUS, MINUS):
        y = simplifyPrefixSign(y)

    if isinstance(x, Num) and isinstance(y, Num):
        return Num(Token(INTEGER, x.value * y.value))

    if (isinstance(x, Num) and x.value == 0 or
            isinstance(y, Num) and y.value == 0):
        return Num(Token(INTEGER, 0))

    if isinstance(x, Num) and x.value == 1:
        return y

    if isinstance(y, Num) and y.value == 0:
        return x

    return BinOp(x, Token(MUL, '*'), y)


def make_div(x: Node, y: Node) -> Node:
    if isinstance(x, UnaryOp) and x.op.type in (PLUS, MINUS):
        x = simplifyPrefixSign(x)

    if isinstance(y, UnaryOp) and y.op.type in (PLUS, MINUS):
        y = simplifyPrefixSign(y)

    if isinstance(y, Num) and y.value == 0:
        raise Exception('Error: division by zero')

    if isinstance(x, Num) and x.value == 0:
        return Num(Token(INTEGER, 0))

    if isinstance(y, Num) and y.value == 1:
        return x

    return BinOp(x, Token(DIV, '/'), y)


def make_power(x: Node, y: Node) -> Node:
    if isinstance(x, UnaryOp) and x.op.type in (PLUS, MINUS):
        x = simplifyPrefixSign(x)

    if isinstance(y, UnaryOp) and y.op.type in (PLUS, MINUS):
        y = simplifyPrefixSign(y)

    if isinstance(x, Num) and isinstance(y, Num):
        return Num(Token(INTEGER, x.value ** y.value))

    if (isinstance(x, Num) and x.value == 1 or
            isinstance(y, Num) and y.value == 0):
        return Num(Token(INTEGER, 1))

    if isinstance(x, Num) and x.value == 0:
        return Num(Token(INTEGER, 0))

    if isinstance(y, Num) and y.value == 1:
        return x

    return BinOp(x, Token(POW, '**'), y)


def make_func(func: str, arg: Node) -> UnaryOp:
    return UnaryOp(Token(FUNC, func), arg)
