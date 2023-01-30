'''
Parser for mathematical functions.
Main program is Parser.parse.
'''

from derivative_calculator.tokenizer import (
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


class UnaryOp:
    '''AST node representing a unary operation'''
    def __init__(self, op, expr):
        self.token = self.op = op
        self.value = self.token.value
        self.expr = expr


class BinOp:
    '''AST node representing a binary operation'''
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num:
    '''AST node representing a number'''
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Var:
    '''AST node representing a variable'''
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser:
    '''
    Parser for mathematical functions.
    Expression grammars are ordered by priority level:
    add_substr_expr: mul_div_expr ((PLUS | MINUS) mul_div_expr)*
    mul_div_expr: pow_expr ((MUL | DIV) pow_expr)*
    pow_expr: factor (POW factor)*
    factor : (PLUS | MINUS | FUNC) factor | INTEGER | LPAREN add_substr_expr RPAREN
    '''
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.current_token = self.tokenizer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.tokenizer.get_next_token()
        else:
            self.error()

    def factor(self):
        """
        factor : (PLUS | MINUS | FUNC) factor | INTEGER | LPAREN add_substr_expr RPAREN
        """
        token = self.current_token

        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)

        elif token.type == VAR:
            self.eat(VAR)
            return Var(token)

        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node

        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node

        elif token.type == FUNC:
            self.eat(FUNC)
            node = UnaryOp(token, self.factor())
            return node

        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.add_substr_expr()
            self.eat(RPAREN)
            return node

    def pow_expr(self):
        '''pow_expr: factor (POW factor)*'''
        node = self.factor()

        while self.current_token.type == POW:
            token = self.current_token
            self.eat(POW)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def mul_div_expr(self):
        '''
        mul_div_expr: pow_expr ((MUL | DIV) pow_expr)*
        '''
        node = self.pow_expr()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.pow_expr())

        return node

    def add_substr_expr(self):
        '''
        add_substr_expr: mul_div_expr ((PLUS | MINUS) mul_div_expr)*
        '''
        node = self.mul_div_expr()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.mul_div_expr())

        return node

    def parse(self):
        return self.add_substr_expr()
