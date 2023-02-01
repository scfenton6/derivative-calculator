import os
from derivative_calculator.tokenizer import Token, Tokenizer, VAR
from derivative_calculator.math_parser import Var, Parser
from derivative_calculator.symb_diff_tool import deriv
from derivative_calculator.interpreter import Interpreter


def main():

    print()
    print('    -------------------------    ')
    print('    - Derivative calculator -    ')
    print('    -------------------------    ')
    print()
    print(' - Supported functions are: exp, log, sin, cos, tan, cosec, sec, cot.')
    print(' - Powers are represented by a double asterisk (**).')
    print(' - Valid variable inputs are single alphabet letters.')
    print()

    while True:
        try:
            expr = input('Enter mathematical function: ')
            if not isinstance(expr, str):
                raise ValueError
            break
        except ValueError:
            print("Invalid input: the mathematical expression must be in string format.")

    while True:
        try:
            var = input('Derivate respect to: ')
            if not (var.isalpha and len(var) == 1):
                raise ValueError
            break
        except ValueError:
            print("Invalid input: the variable must be a single alphabet letter.")

    expr_ast = Parser(Tokenizer(expr)).parse()  # AST representing function
    token_var = Var(Token(VAR, var))  # Token object containing variable

    deriv_ast = deriv(expr_ast, token_var)
    inter = Interpreter()
    deriv_output = inter.visit(deriv_ast)

    print('Derivative: ', deriv_output)

    restart = input("Would you like to restart this program? (y/n): ")
    if restart == "y":
        os.system('cls||clear')
        main()
    if restart == "n":
        print("Good bye.")


if __name__ == '__main__':
    main()
