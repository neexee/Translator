import string
from  math import pow
import tree

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

    def term(self):
        """ term ::= [atom/*factor]
        """
        t = Tree()
        (c, lbranch) = self.atom()
        t.add_branch(lbranch)
        flag = True
        while (self.symbol.value in ['/', '*']):
            flag = False
            if(self.symbol.value == '/'):
                symbol = '/'
                (c0, rbranch) = self.div()
                c /= c0
            if(self.symbol.value == '*'):
                symbol = '*'
                (c0, rbranch) = self.mul()
                c *= c0
            t.add_branch(Tree(symbol))
            t.add_branch(rbranch)
        if(flag):
            t = lbranch
        return c, t
    def expression(self):
        """ expression ::= [term+-term]
        """
        t = Tree()
        sign = 1
        if(self.symbol.value == '+'):
            t.add_branch(Tree('+'))
            #symbol = '+'
            self.next('+')
        if(self.symbol.value == '-'):
            t.add_branch(Tree('-'))
            #symbol = '-'
            self.next('-')
            sign = -1
        (c, lbranch) = self.term()
        c*= sign
        t.add_branch(lbranch)
        flag = True
        while (self.symbol.value in ['+', '-']):
            flag = False
            if(self.symbol.value =='+'):
                s = '+'
                (cc, rbranch) = self.add()
                c+=cc
            if(self.symbol.value =='-'):
                s = '-'
                (cc, rbranch) = self.sub()
                c-=cc
            t.add_branch(Tree(s))
            t.add_branch(rbranch)
        if(flag):
            t = lbranch
        return c, t
    def atom(self):
        """atom ::= factor^expression
        """
        t = Tree()
        (c, lbranch) = self.factor()
        t.add_branch(lbranch)
        flag = True
        while (self.symbol.value == '^'):
            flag = False
            t.add_branch(Tree('^'))
            self.next('^')
            (cc, rbranch) = self.expression()

            c = pow(c, cc)
            t.add_branch(rbranch)
        if(flag):
            t = lbranch
        return c, t
    def factor(self):
        """ factor = (expression) | number
        """
        t = Tree()
        if(self.symbol.value == '('):
            t.add_branch(Tree('('))
            self.next('(')
            (result, branch) = self.expression()
            t.add_branch(branch)
            self.next(')')
            t.add_branch(Tree(')'))
            return result, t
        else:
            c = self.symbol.value
            self.next(self.symbol.value)

            try:
                value = int(c)
                t = Tree(c)
            except ValueError as e:
                raise ParserError(self.symbol, self.lineNum, self.symbolNum)
            return value , t

    def next(self, value):
        if(self.symbol.value == value):
            self.symbol = self.lexer.getToken()
            self.symbolNum+=1
        else:
            raise ParserError(self.symbol, self.lineNum, self.symbolNum)


