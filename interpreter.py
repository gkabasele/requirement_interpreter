from parser import *
from lexer import *

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_'+ type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self, parser, variables):
        self.parser = parser
        self.vars = variables

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == LESS:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.type == LESS_EQ:
            return self.visit(node.left) <= self.visit(node.right)
        elif node.op.type == GREAT_EQ:
            return self.visit(node.left) >= self.visit(node.right)
        elif node.op.type == GREAT:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.type == DIFF:
            return self.visit(node.left) != self.visit(node.right)
        elif node.op.type == EQUAL:
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.type == AND:
            return self.visit(node.left) and self.visit(node.right)
        elif node.op.type == OR:
            return self.visit(node.left) or self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_Bool(self, node):
        return node.value

    def visit_Var(self, node):
        return self.vars[node.value]

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == NOT:
            return not self.visit(node.expr)

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

def main():
    variables = {"test1": 1, "bac": 3}
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
        print(result)
           

if __name__ == '__main__':
    main()
