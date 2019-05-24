from parser import *
from lexer import *
from interpreter import Interpreter

class ProcessVariable():
    def __init__(self, kind, value, gap=1):

        self.kind = kind
        self.value = value
        self.gap = gap

    def is_bool_var(self):
        return self.kind is bool

def main():

    variables = {
                    "test": ProcessVariable( bool, 1),
                    "ab": ProcessVariable( int, 30, 60),
                    "cd": ProcessVariable( int, 15, 20),
                    "ef": ProcessVariable( int, 50, 20), 
                    "t3" : ProcessVariable( int,0, 14),
                    "v1" : ProcessVariable( bool, 0),
                    "v2" : ProcessVariable( bool, 0),
                    "v3" : ProcessVariable( bool, 0)
                }

    while True:
        try:
            text = input('simple>')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser, variables)
        result = interpreter.interpret()
        print(interpreter.mapping_id_var)
        print(interpreter.distances)
        print(interpreter.compute_distance(4,4, False))
        print(result)

if __name__ == '__main__':
    main()
