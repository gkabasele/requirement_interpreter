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
    def __init__(self, parser, variables, num_weight=1, bool_weight=5):
        self.parser = parser
        self.vars = variables
        self.distances = []
        self.num_weight = num_weight
        self.bool_weight = bool_weight

    def visit_BinOp(self, node):
        if node.op.type in (PLUS, MINUS, DIV,AND, OR):
            left = self.visit(node.left)
            right = self.visit(node.right)

            if node.op.type == PLUS:
                return left + right
            elif node.op.type == MINUS:
                return left - right
            elif node.op.type == MUL:
                return left * right
            elif node.op.type == DIV:
                return left / right
            elif node.op.type == AND:
                return left and right
            elif node.op.type == OR:
                return left or right

        elif node.op.type in (LESS, LESS_EQ, GREAT_EQ, GREAT, DIFF, EQUAL):
            left = self.visit(node.left)
            right = self.visit(node.right)
            self.distance_comparison(node.left, node.right, left, right)
            if node.op.type == LESS:
                return left < right
            elif node.op.type == LESS_EQ:
                return left <= right
            elif node.op.type == GREAT_EQ:
                return left >= right
            elif node.op.type == GREAT:
                return left > right
            elif node.op.type == DIFF:
                return left != right
            elif node.op.type == EQUAL:
                return left == right
            
    def visit_Num(self, node):
        return node.value

    def visit_Bool(self, node):
        return node.value

    def visit_Var(self, node):
        return self.vars[node.value].value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == NOT:
            return not self.visit(node.expr)

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

    def distance_comparison(self, node_left, node_right, val_left, val_right):
        if type(node_left) is Var or type(node_right) is Var:
            if type(node_left) is Var:
                weight = self.get_weight(node_left)
            elif type(node_right) is Var:
                weight = self.get_weight(node_right)
            self.distances.append(weight * abs( val_left - val_right))

    def compute_distance(self, num_var, bool_var):
        divider = self.num_weight*num_var + self.bool_weight*bool_var
        s = sum(self.distances)
        d =  float(sum(self.distances))/(self.num_weight*num_var + self.bool_weight*bool_var)
        self.distances =  []
        return d

    def get_weight(self, node):
        if self.vars[node.value].is_bool_var():
            w = self.bool_weight
        else:
            w = self.num_weight
        return w



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
