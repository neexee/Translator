import string
from  math import pow
import tree
from token import  Token
from enviroment import Enviroment

from tree import Tree
class ParserError(Exception):
    def __init__(self, symbol, lineNum, symbolNum):
        self.value = '['+repr(lineNum)+':'+repr(symbolNum)+']'+' Parse error on symbol "'+symbol.value+'" ('+symbol.type+')'
    def __str__(self):
        return repr(self.value)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.symbol = lexer.getToken()
        self.symbolNum=1
        self.lineNum =1
        self.environment = Enviroment(None)
        self.eof = Token('', 'EOF')
    def add(self):
        self.next('+')
        return self.term()
    def sub(self):
        self.next('-')
        return self.term()
    def div(self):
        self.next('/')
        return self.factor()

    def mul(self):
        self.next('*')
        return self.factor()
    def block(self):
        self.environment = Enviroment(self.environment)
        while(True):
            if(self.symbol.type in self.lexer.types):
                self.declaration()
            if(self.symbol.value == 'def'):
                self.func()
            if(self.symbol.value == '{'):
                self.next()
                self.block()
                self.next('}')
            if(self.symbol.value =='}' or self.symbol == self.eof):
                return # WAT?
            else:
                self.instruction()

    def instruction(self):
        #funcall or assignment
        if(self.symbol in self.environment.dict):
            if(self.symbol.type in self.lexer.types):
                symbol = self.symbol
                self.next('=')
                expr = self.expression()
                if(symbol.type == expr.type):
                    pass
                else:
                    self.error()
            if(self.symbol.type == 'func'):
                self.expression()
            else:
                self.error()
        else:
            self.error()
    def program(self):
        self.block()
    def declaration(self):
        # int i =0, k;
        # int s = f()
        if(self.symbol.type in self.lexer.types):
            type = self.symbol.type
            self.next()
            while(self.symbol != Token(';', 'punct')):
                if(self.symbol.type == 'id' and self.symbol.value not in self.environment):
                    symbol = self.symbol
                    symbol.type = type
                    self.environment.dict[symbol] = None
                    self.next()
                    if(self.symbol == Token(',', 'punct')):
                        self.next()
                        continue
                    if(self.symbol == Token('=', 'operator')):
                        expr = self.expression()
                        #Check type expression and symbol.
                        if(expr.type == symbol.type):
                             self.environment.dict[symbol] = expr
                        else:
                            self.error()
                        self.next()
                        if(self.symbol == Token(',', 'punct')):
                            self.next()
                            continue
                else:
                    self.error()
    def eq_expr(self):
        pass

    def func(self):
        if( self.exists_in_env(self.symbol)):
            self.error()    #function already declared
        else:
            func = self.symbol
            #self.enviroment.dict[self.symbol] = ''
            self.next('(')
            params = self.func_params()
            self.next(')')
            self.environment.dict[func] = params
            self.next('{')
            body = self.block()
            self.next('}')

    def func_params(self):
        pass
    def func_expr(self):
        pass

    def exists_in_env(self, symbol):
        if(symbol in self.environment.dict):
            return True
        return False
    def term(self):
        """ term ::= [atom/*factor]
        """

        (c, lbranch) = self.atom()
        tt = Tree(Token('', ''))
        tt.add_branch(lbranch)
        flag = True
        while (self.symbol.value in ['/', '*']):
            flag = False
            symbol = self.symbol
            if(self.symbol.value == '/'):
                (c0, rbranch) = self.div()
                c /= c0
            if(self.symbol.value == '*'):
                symbol = '*'
                (c0, rbranch) = self.mul()
                c *= c0
            tt.add_branch(Tree(symbol))
            tt.add_branch(rbranch)
        if(flag):
            tt = lbranch
        return c, tt
    def expression(self):
        """ expression ::= [term+-term]
        """
        t = Tree(Token('', ''))
        sign = 1
        if(self.symbol.value == '+'):
            t.add_branch(Tree(self.symbol))
            self.next('+')
        if(self.symbol.value == '-'):
            t.add_branch(Tree(self.symbol))
            self.next('-')
            sign = -1
        (c, lbranch) = self.term()
        c*= sign
        t.add_branch(lbranch)
        flag = True
        while (self.symbol.value in ['+', '-']):
            flag = False
            symbol = self.symbol
            if(self.symbol.value =='+'):
                (cc, rbranch) = self.add()
                c+=cc
            if(self.symbol.value =='-'):
                (cc, rbranch) = self.sub()
                c-=cc
            t.add_branch(Tree(symbol))
            t.add_branch(rbranch)
        if(flag):
            t = lbranch
        return c, t
    def atom(self):
        """atom ::= factor^factor
        """
        t = Tree(Token('', ''))
        (c, lbranch) = self.factor()
        t.add_branch(lbranch)
        flag = True
        while (self.symbol.value == '^'):
            flag = False
            t.add_branch(Tree(self.symbol))
            self.next('^')
#            (cc, rbranch) = self.expression()
            (cc, rbranch) = self.factor()


            c = pow(c, cc)
            t.add_branch(rbranch)
        if(flag):
            t = lbranch
        return c, t
    def factor(self):
        """ factor = (expression) | number
        """
        t = Tree(Token('', ''))
        if(self.symbol.value == '('):
            t.add_branch(Tree(self.symbol))
            self.next('(')
            (result, branch) = self.expression()
            t.add_branch(branch)
            symbol = self.symbol
            self.next(')')
            t.add_branch(Tree(symbol))
            return result, t
        else:
            symbol = self.symbol
            c = self.symbol.value
            self.next(self.symbol.value)

            try:
                value = int(c)
                t = Tree(symbol)
            except ValueError as e:
                raise ParserError(self.symbol, self.lineNum, self.symbolNum)
            return value , t
    def next(self):
         try:
            self.symbol = self.lexer.getToken()
         except EOFError as e:
                raise ParserError(self.symbol, self.lineNum, self.symbolNum)
    def next(self, value):
        if(self.symbol.value == value):
            try:
                self.symbol = self.lexer.getToken()
            except EOFError as e:
                raise ParserError(self.symbol, self.lineNum, self.symbolNum)
            self.symbolNum+=1
        else:
            raise ParserError(self.symbol, self.lineNum, self.symbolNum)
    def error(self):
        raise ParserError(self.symbol, self.lineNum, self.symbolNum)

