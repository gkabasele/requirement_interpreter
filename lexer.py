INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS  = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
EOF = 'EOF'

OR = 'OR'
AND = 'AND'
NOT = 'NOT'

LESS = 'LESS'
GREAT = 'GREAT'
EQUAL = 'EQUAL'
GREAT_EQ = 'GREAT_EQ'
LESS_EQ = 'LESS_EQ'
DIFF = 'DIFF'
BOOLEAN = 'BOOLEAN'
LPAREN = '('
RPAREN = ')'

class Token(object):

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token(%s, %s)' % (self.type, self.value)

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]


    def skip_whitespace(self):
         while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def boolean(self, char):
        result = ''
        i = 0
        if char == 'F':
            text = 'False'
            while self.current_char is not None and text[i] == self.current_char:
                result += self.current_char
                self.advance()
                i += 1
        elif char == 'T': 
            text = 'True'
            while self.current_char is not None and text[i] == self.current_char:
                result += self.current_char
                self.advance()
                i += 1
        else:
            self.error()
        
        if result in ["True", "False"]:
            return result == "True"
        else:
            self.error()


    def get_next_token(self):

        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == 'T' or self.current_char == 'F':
                return Token(BOOLEAN, self.boolean(self.current_char))

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '&':
                self.advance()
                return Token(AND, '&')
            
            if self.current_char == '|':
                self.advance()
                return Token(OR, '|')
            
            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(DIFF, '!=')
                else:
                    return Token(NOT, '!')

            if self.current_char == '=':
                self.advance()
                return Token(EQUAL, '=')


            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(LESS_EQ, '<=')
                else:
                    return Token(LESS, '<')
            
            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(GREAT_EQ, '>=')
                else:
                    return Token(GREAT, '>')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)


