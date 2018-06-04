from parser import *
from lexer import *

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_'+ type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class DistanceVal(object):

    def __init__(self, node_id, val):
        self.node_id = node_id
        self.val = val

    def __str__(self):
        return "({}, {})".format(self.node_id, self.val)

    def __repr__(self):
        return self.__str__()

class Interpreter(NodeVisitor):
    def __init__(self, parser, variables, num_weight=1, bool_weight=5):
        self.parser = parser
        # variable is a dict name -> process_variable
        self.vars = variables
        self.distances = []
        self.num_weight = num_weight
        self.bool_weight = bool_weight
        self.current_node_id = 0
        # node_id -> name_var
        self.mapping_id_var = {}

    def set_current_node_id(self, node):
        node.id = self.current_node_id
        self.current_node_id += 1

    def visit_BinOp(self, node):
        if node.op.type in (PLUS, MINUS, DIV,AND, OR):
            left = self.visit(node.left)
            right = self.visit(node.right)
            self.set_current_node_id(node)

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
            self.set_current_node_id(node)
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
        self.set_current_node_id(node)
        return node.value

    def visit_Bool(self, node):
        self.set_current_node_id(node)
        return node.value

    def visit_Var(self, node):
        self.mapping_id_var[str(self.current_node_id)] = node.value
        self.set_current_node_id(node)
        return self.vars[node.value].value

    def visit_UnaryOp(self, node):
        self.set_current_node_id(node)
        op = node.op.type
        if op == NOT:
            return not self.visit(node.expr)

    def interpret(self):
        if self.parser is not None:
            tree = self.parser.parse()
            return self.visit(tree)

    def distance_comparison(self, node_left, node_right, val_left, val_right):
        if type(node_left) is Var or type(node_right) is Var:
            if type(node_left) is Var:
                identifier = node_left.id
                weight = self.get_weight(node_left)
            elif type(node_right) is Var:
                identifier = node_right.id
                weight = self.get_weight(node_right)

            dist = weight * abs( val_left - val_right)
            self.distances.append(DistanceVal(str(identifier), dist))

    def compute_distance(self, num_var, bool_var, normal=True):
        if normal: 
            d =  float(sum([x.val for x in self.distances]))/(self.num_weight*num_var + self.bool_weight*bool_var)
        else:
            # We only take, for each variable, the minimum between all distances for a variable, A in [10,30]
            # A = 25, dist(A) = min(|10-25|, |30-25|) = 5
            # We have a dict giving the id of the variable in the tree, and for each distance we know which "instance" of the variable was used

            # name_var -> minimum_dist
            dist_vars_mapping = {}
            for dist in self.distances:
                varname = self.mapping_id_var[dist.node_id]
                if varname in dist_vars_mapping:
                    if self.vars[varname].is_bool_var():
                        dist_vars_mapping[varname].append(dist.val)
                    else:
                        dist_vars_mapping[varname] = [min(dist_vars_mapping[varname], dist.val)]
                else:
                    dist_vars_mapping[varname] = [dist.val]
            d = float(sum([val for sublist in dist_vars_mapping.itervalues() for val in sublist]))/(self.num_weight*num_var + self.bool_weight*bool_var)
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
