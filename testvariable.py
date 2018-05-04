from parser import *
from lexer import *
from interpreter import Interpreter

class ProcessVariable():
    def __init__(self, kind, value):

        self.kind = kind
        self.value = value

    def is_bool_var(self):
        return self.kind is bool

def main():

    variables = {"test": ProcessVariable( bool, 1), "ab": ProcessVariable( int, 40)}

    while True:
        try:
            text = raw_input('simple>')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser, variables)
        result = interpreter.interpret()
        print interpreter.distances
        print interpreter.compute_distance(1,1)
        print(result)

if __name__ == '__main__':
    main()
