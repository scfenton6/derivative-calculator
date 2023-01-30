'''
Parser for mathematical functions.
Main program is Parser.parse.
'''

import typing
from derivative_calculator.tokenizer import (
    Token,
    Tokenizer,
    INTEGER,
    VAR,
    PLUS,
    MINUS,
    MUL,
    DIV,
    POW,
    FUNC,
    LPAREN,
    RPAREN,
)

Node = typing.Union['UnaryOp', 'BinOp', 'Num', 'Var']


class UnaryOp:
    '''AST node representing a unary operation'''
    def __init__(self, op: Token, expr: Node) -> None:
        self.token = self.op = op
        self.value = self.token.value
        self.expr = expr


class BinOp:
    '''AST node representing a binary operation'''
    def __init__(self, left: Node, op: Token, right: Node) -> None:
        self.left = left
        self.token = self.op = op
        self.right = right


class Num:
    '''AST node representing a number'''
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value: int = token.value


class Var:
    '''AST node representing a variable'''
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value: str = token.value


class Parser:
    '''
    Parser for mathematical functions.
    Expression grammars are ordered by priority level:
    add_substr_expr: mul_div_expr ((PLUS | MINUS) mul_div_expr)*
    mul_div_expr: pow_expr ((MUL | DIV) pow_expr)*
    pow_expr: factor (POW factor)*
    factor : (PLUS | MINUS | FUNC) factor | INTEGER | LPAREN add_substr_expr RPAREN
    '''
    def __init__(self, tokenizer: Tokenizer) -> None:
        self.tokenizer = tokenizer
        self.current_token = self.tokenizer.get_next_token()

    def error(self) -> None:
        raise Exception('Invalid syntax')

    def eat(self, token_type: str) -> None:
        if self.current_token.type == token_type:
            self.current_token = self.tokenizer.get_next_token()
        else:
            self.error()

    def factor(self) -> Node:  # type: ignore[return]
        """
        factor : (PLUS | MINUS | FUNC) factor | INTEGER | LPAREN add_substr_expr RPAREN
        """
        token: Token = self.current_token

        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)

        elif token.type == VAR:
            self.eat(VAR)
            return Var(token)

        if token.type == PLUS:
            self.eat(PLUS)
            plus_node = UnaryOp(token, self.factor())
            return plus_node

        elif token.type == MINUS:
            self.eat(MINUS)
            minus_node = UnaryOp(token, self.factor())
            return minus_node

        elif token.type == FUNC:
            self.eat(FUNC)
            func_node = UnaryOp(token, self.factor())
            return func_node

        elif token.type == LPAREN:
            self.eat(LPAREN)
            paren_node: Node = self.add_substr_expr()
            self.eat(RPAREN)
            return paren_node

    def pow_expr(self) -> Node:
        '''pow_expr: factor (POW factor)*'''
        fact_node: Node = self.factor()

        while self.current_token.type == POW:
            token = self.current_token
            self.eat(POW)
            fact_node = BinOp(left=fact_node, op=token, right=self.factor())

        return fact_node

    def mul_div_expr(self) -> Node:
        '''
        mul_div_expr: pow_expr ((MUL | DIV) pow_expr)*
        '''
        pow_node: Node = self.pow_expr()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            pow_node = BinOp(left=pow_node, op=token, right=self.pow_expr())

        return pow_node

    def add_substr_expr(self) -> Node:
        '''
        add_substr_expr: mul_div_expr ((PLUS | MINUS) mul_div_expr)*
        '''
        mul_node: Node = self.mul_div_expr()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            mul_node = BinOp(left=mul_node, op=token, right=self.mul_div_expr())

        return mul_node

    def parse(self) -> Node:
        return self.add_substr_expr()
