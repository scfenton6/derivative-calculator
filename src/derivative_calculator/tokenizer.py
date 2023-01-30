'''
Tokenizer implementation.
Tokenizer.token_iter is the main program.
'''

import typing


INTEGER, VAR, PLUS, MINUS, MUL, DIV, POW, FUNC, LPAREN, RPAREN, EOF = (
    'INTEGER', 'VAR', 'PLUS', 'MINUS', 'MUL', 'DIV', 'POW', 'FUNC', '(', ')', 'EOF'
)
valid_functions = (
        'exp', 'log', 'sin', 'cos', 'tan', 'cosec', 'sec', 'cot'
        )


class Token:
    def __init__(self, type: str, value: typing.Any) -> None:
        self.type = type
        self.value = value


class Tokenizer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.current_char: typing.Optional[str] = self.text[self.pos]

    def error(self) -> None:
        raise Exception('Invalid character')

    def advance(self) -> None:
        """Advance pos pointer and set current_char variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self) -> None:
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def handle_integer(self) -> int:
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def handle_alpha_seq(self) -> tuple[str, str]:  # type: ignore[return]
        """Determine whether or not our sequence of alpha
        characters is a variable or a valid function."""
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()

        if len(result) == 1:
            return VAR, result

        if result in valid_functions:
            return FUNC, result

        self.error()

    def handle_asterisk(self) -> tuple[str, str]:  # type: ignore[return]
        """Determine whether or not our asterisk is followed
        by another asterisk. In the former case it would
        represent the product operator, and in the latter it
        would represent the power operator"""
        result = ''
        while self.current_char is not None and self.current_char == '*':
            result += self.current_char
            self.advance()

        if len(result) == 1:
            return MUL, result

        if len(result) == 2:
            return POW, result

        self.error()

    def get_next_token(self) -> Token:
        """
        Tokenizer: breaks a sentence apart into tokens one token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.handle_integer())

            if self.current_char.isalpha():
                op, val = self.handle_alpha_seq()
                return Token(op, val)

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                op, val = self.handle_asterisk()
                return Token(op, val)

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)
