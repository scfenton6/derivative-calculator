'''
Symbolic differentiation tool that takes an abstract syntax
tree containing a math function as input and applies the
derivative rules and the chain rule on it via depth first search
to return an abstract syntax tree containing the derivative of the
function.

Derivative rules: https://en.wikipedia.org/wiki/Differentiation_rules
Chain rule: https://en.wikipedia.org/wiki/Chain_rule
'''

import typing
from derivative_calculator.math_parser import Num, Var, UnaryOp, BinOp
from derivative_calculator.tokenizer import Token, INTEGER, MINUS
import derivative_calculator.utils as utils

Node = typing.Union[UnaryOp, BinOp, Num, Var]


def deriv(node: Node, var: Var) -> Node:
    if utils.is_number(node):
        return Num(Token(INTEGER, 0))

    if utils.is_var(node):
        if utils.same_var(node, var):
            return Num(Token(INTEGER, 1))
        return Num(Token(INTEGER, 0))

    if isinstance(node, UnaryOp):
        if utils.is_prefix_sign(node):
            simpl_node: UnaryOp | Num = utils.simplifyPrefixSign(node)
            if isinstance(simpl_node, Num):
                return Num(Token(INTEGER, 0))
            else:
                return UnaryOp(simpl_node.token, deriv(simpl_node.expr, var))

        if utils.is_func(node):
            if node.value == 'exp':
                return utils.make_prod(
                    node,
                    deriv(node.expr, var)
                )

            if node.value == 'log':
                return utils.make_prod(
                    utils.make_div(
                        Num(Token(INTEGER, 1)),
                        node.expr
                    ),
                    deriv(node.expr, var)
                )

            if node.value == 'sin':
                return utils.make_prod(
                    utils.make_func(
                        func='cos',
                        arg=node.expr
                    ),
                    deriv(node.expr, var)
                )

            if node.value == 'cos':
                return utils.make_prod(
                    UnaryOp(
                        Token(MINUS, '-'),
                        utils.make_func(
                            func='sin',
                            arg=node.expr
                            )
                        ),
                    deriv(node.expr, var)
                )

            if node.value == 'tan':
                return utils.make_prod(
                        utils.make_power(
                            utils.make_func(
                                func='sec',
                                arg=node.expr
                            ),
                            Num(Token(INTEGER, 2))
                        ),
                        deriv(node.expr, var)
                    )

            if node.value == 'cosec':
                return utils.make_prod(
                    utils.make_prod(
                        UnaryOp(
                            op=Token(MINUS, '-'),
                            expr=node
                        ),
                        utils.make_func(
                            func='cot',
                            arg=node.expr
                        )
                    ),
                    deriv(node.expr, var)
                )

            if node.value == 'sec':
                return utils.make_prod(
                    utils.make_prod(
                        node,
                        utils.make_func(
                            func='tan',
                            arg=node.expr
                        )
                    ),
                    deriv(node.expr, var)
                )

            if node.value == 'cot':
                return utils.make_prod(
                    UnaryOp(
                        op=Token(MINUS, '-'),
                        expr=utils.make_power(
                            utils.make_func(
                                func='cosec',
                                arg=node.expr
                                ),
                            Num(Token(INTEGER, 2))
                            )
                    ),
                    deriv(node.expr, var)
                )

    if isinstance(node, BinOp):
        if utils.is_sum(node):
            return utils.make_sum(
                deriv(node.left, var),
                deriv(node.right, var)
            )

        if utils.is_substr(node):
            return utils.make_substr(
                deriv(node.left, var),
                deriv(node.right, var)
            )

        if utils.is_prod(node):
            return utils.make_sum(
                utils.make_prod(
                    node.left,
                    deriv(node.right, var)
                ),
                utils.make_prod(
                    deriv(node.left, var),
                    node.right
                )
            )

        if utils.is_div(node):
            return utils.make_div(
                utils.make_substr(
                    utils.make_prod(
                        node.right,
                        deriv(node.left, var)
                    ),
                    utils.make_prod(
                        node.left,
                        deriv(node.right, var)
                    )
                ),
                utils.make_power(
                    node.right,
                    Num(Token(INTEGER, 2))
                )
            )

        if utils.is_pow(node):
            base: Node = node.left
            exponent: Node = node.right
    
            return utils.make_sum(
                utils.make_prod(
                        utils.make_prod(
                            exponent,
                            utils.make_power(
                                base,
                                utils.make_substr(
                                    exponent,
                                    Num(Token(INTEGER, 1))
                                )
                            )
                        ),
                        deriv(base, var)
                    ),
                utils.make_prod(
                        utils.make_prod(
                            node,
                            utils.make_func(
                                'log',
                                base
                                )
                        ),
                        deriv(exponent, var)
                    )
                )

    raise Exception('Could not find any tokens matching input')
