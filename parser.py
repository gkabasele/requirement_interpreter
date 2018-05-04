from lexer import *

class AST(object):
    pass

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Bool(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)

        elif token.type == VAR:
            self.eat(VAR)
            return Var(token)

        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node

    def term(self):
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def numexpr(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def compexpr(self):
        token = self.current_token

        if token.type == BOOLEAN:
            self.eat(BOOLEAN)
            return Bool(token)

        elif token.type == NOT:
            self.eat(NOT)
            node = UnaryOp(op=token, expr=self.compexpr)

        else:
            node = self.numexpr()

            while self.current_token.type in (LESS, LESS_EQ, GREAT_EQ, GREAT, EQUAL, DIFF):
                token = self.current_token
                if token.type == LESS:
                    self.eat(LESS)
                elif token.type == LESS_EQ:
                    self.eat(LESS_EQ)
                elif token.type == GREAT_EQ:
                    self.eat(GREAT_EQ)
                elif token.type == GREAT:
                    self.eat(GREAT)
                elif token.type == EQUAL:
                    self.eat(EQUAL)
                elif token.type == DIFF:
                    self.eat(DIFF)

                node = BinOp(left=node, op=token, right=self.numexpr())

        return node

    def conexpr(self):
        node = self.compexpr()
        while self.current_token.type == AND:
            token = self.current_token
            self.eat(AND)
            node = BinOp(left=node, op=token, right=self.compexpr())


        return node

    def boolexpr(self):
        node = self.conexpr()

        while self.current_token.type == OR:
            token = self.current_token
            self.eat(OR)
            node = BinOp(left=node, op=token, right=self.conexpr())

        return node

    def parse(self):
        return self.boolexpr()
            



