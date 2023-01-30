import pytest
import typing
from derivative_calculator.tokenizer import Token, Tokenizer, VAR, INTEGER, PLUS, MUL, POW
from derivative_calculator.math_parser import Var, Num, BinOp, UnaryOp, Parser
from derivative_calculator.interpreter import Interpreter
from derivative_calculator.symb_diff_tool import deriv

Node = typing.Union[UnaryOp, BinOp, Num, Var]


def get_parsed_expr(expr: str) -> Node:
    '''
    Takes a string containing an expression
    and returns the AST tree corresponding to the
    parsed expression
    '''
    return Parser(Tokenizer(expr)).parse()


def interpret_ast(ast_expr: Node) -> str:
    '''
    Takes an AST tree and returns the string
    containing its interpreted expression
    '''
    return Interpreter().visit(ast_expr)


def get_derivative(expr: str, var: str) -> str:
    '''
    Takes an math function and a variable and returns a string
    containing the interpreted expression of its derivative
    '''
    deriv_ast: Node = deriv(get_parsed_expr(expr), Var(Token(VAR, var)))
    return interpret_ast(deriv_ast)


def compare_ast(node_1: Node, node_2: Node) -> bool:  # type: ignore[return]
    '''
    Function that compares two abstract syntax trees
    node for node, returning True if they are equal
    and False if not
    '''
    if not (node_1 or node_2):
        return True

    if isinstance(node_1, (Num, Var)) and isinstance(node_2, (Num, Var)):
        if type(node_1) is type(node_2):
            if node_1.value == node_2.value:
                return True
            return False
        return False

    if (node_1 and not node_2) or (not node_1 and node_2):
        return False

    if isinstance(node_1, BinOp) and isinstance(node_2, BinOp):
        if node_1.op.type == node_2.op.type:
            return (compare_ast(node_1.left, node_2.left) and
                    compare_ast(node_1.right, node_2.right))
        return False

    if isinstance(node_1, UnaryOp) and isinstance(node_2, UnaryOp):
        if node_1.op.type == node_2.op.type:
            return compare_ast(node_1.expr, node_2.expr)
        return False


pow_node = BinOp(
    left=Var(Token(VAR, 'x')),
    op=Token(POW, '**'),
    right=Num(Token(INTEGER, 2))
    )

mul_node = BinOp(
    left=Num(Token(INTEGER, 3)),
    op=Token(MUL, '*'),
    right=pow_node
    )

add_node = BinOp(
    left=mul_node,
    op=Token(PLUS, '+'),
    right=Num(Token(INTEGER, 5))
    )


def test_parser() -> None:
    '''
    We compare our manually built AST corresponding to the
    function 3*x**2+5 with the result of calling our parser with
    3*x**2+5 as argument
    '''
    assert compare_ast(get_parsed_expr('3*x**2+5'), add_node)


def test_interpreter() -> None:
    '''
    Here we pass our manually built AST corresponding to the
    function 3*x**2+5 to the interpreter and check if the result
    is a string containing the function 3*x**2+5
    '''
    assert interpret_ast(add_node) == '3*x**2+5'


@pytest.mark.parametrize("test_input,expected", [
    (get_derivative('x', 'x'), '1'),
    (get_derivative('x', 'y'), '0'),
    (get_derivative('x**5', 'x'), '5*x**4'),
    (get_derivative('3*2*y', 'y'), '6'),
    (get_derivative('x*y', 'y'), 'x'),
    (get_derivative('sin(x)', 'x'), 'cos(x)'),
    (get_derivative('exp(x)', 'x'), 'exp(x)'),
    (get_derivative('log(x**2)', 'x'), '1/(x**2)*2*x'),
    (get_derivative('(1+x)*3**x', 'x'), '(1+x)*3**x*log(3)+3**x')
    ])
def test_derivatives(test_input: str, expected: str) -> None:
    '''
    We test our whole program at once, calling the derivative
    function with the parsed AST tree for each pair math function/
    variable and comparing the interpreted result with the expected
    result
    '''
    assert test_input == expected
