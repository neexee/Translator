import string
from  math import pow
import tree
from lexeme import  Lexeme
from enviroment import Enviroment

from tree import Tree
class ParserError(Exception):
    def __init__(self, symbol, lineNum, symbolNum, message):
        self.value = '['+repr(lineNum)+':'+repr(symbolNum)+']'+' Parse error on symbol "'+symbol.value+'" ('+symbol.type+')'+ ' : '+ str(message)
    def __str__(self):
        return repr(self.value)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.symbol = lexer.getToken()
        self.symbolNum=1
        self.lineNum =1
        self.environment = Enviroment(None)
        self.eof = Lexeme('', 'EOF')
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
            self.ignorenewline()
            if(self.symbol.type in self.lexer.types):
                self.declaration()
            if(self.symbol.value == 'def'):
                self.next()
                self.func()
            if(self.symbol.value == '{'):
                self.next()
                self.block()
                self.next('}')
            if(self.symbol.value =='}' or self.symbol == self.eof):
                return # WAT?
            else:
                self.instruction()
    def get_type_in_env(self, symbol):
        env = self.environment
        while(env != None):
            if(len(env.dict) != 0):
                return env.dict[symbol.type]
            env = env.top
        return None

    def instruction(self):
        #funcall or assignment
        if(self.exists_in_env(self.symbol)):
                type = self.get_type_in_env(self.symbol)
                symbol = self.symbol
                symbol.type = type
                if(symbol.type == 'func'):
                     self.expression()
                     return
                self.next('=')
                expr = self.expression()
                if(symbol.type == expr.type):
                    pass
                else:
                    self.error()
        else:
            self.error('undefined')
    def program(self):
        self.block()
    def declaration(self):
        # int i =0, k;
        # int s = f()
        if(self.symbol.type in self.lexer.types):
            type = self.symbol.type
            self.next()
            while(self.symbol != Lexeme(';', 'punct')):
                if(self.symbol.type == 'id' and self.symbol.value not in self.environment):
                    symbol = self.symbol
                    symbol.type = type
                    self.environment.dict[symbol] = None
                    self.next()
                    if(self.symbol == Lexeme(',', 'punct')):
                        self.next()
                        continue
                    if(self.symbol == Lexeme('=', 'operator')):
                        expr = self.expression()
                        #Check type expression and symbol.
                        if(expr.type == symbol.type):
                             self.environment.dict[symbol] = expr
                        else:
                            self.error()
                        self.next()
                        if(self.symbol == Lexeme(',', 'punct')):
                            self.next()
                            continue
                else:
                    self.error(self.symbol + 'already declared or not id')
    def eq_expr(self):
        pass

    def func(self):
        if( self.exists_in_env(self.symbol)):
            self.error(self.symbol + 'already declared' )    #function already declared
        else:
            func = self.symbol
            #self.enviroment.dict[self.symbol] = ''
            self.next()
            self.next('(')
            params = self.func_params()
            self.next(')')
            self.environment.dict[func] = params
            for param in params:
                self.environment.dict[param] = None
            self.ignorenewline()
            self.next('{')
            body = self.block()
            self.next('}')
    def ignorenewline(self):
        while(self.symbol.type == 'newline'):
            self.next()
    def func_params(self):
        params = []
        while(self.symbol.value in self.lexer.types):
             type = self.symbol.value
             self.next()
             if(self.symbol.type == 'id' and self.symbol not in self.environment):
                symbol = self.symbol
                symbol.type = type
                params.append(symbol)
                self.next()
                if(self.symbol == Lexeme(',', 'punctuation')):
                    self.next()
                    continue
                if(self.symbol == Lexeme(')', 'punctuation')):
                    break
                else:
                    self.error()
                    #self.next()
        return params
    def func_expr(self):
        pass

    def exists_in_env(self, symbol):
        env = self.environment

        while(env != None):
            if(len(env.dict) != 0):
                if(symbol in env):
                   return True
            env = env.top
        return False
    def term(self):
        """ term ::= [atom/*factor]
        """

        lbranch = self.atom()
        tt = Tree(Lexeme('', ''))
        tt.add_branch(lbranch)
        flag = True
        while (self.symbol.value in ['/', '*']):
            flag = False
            symbol = self.symbol
            if(self.symbol.value == '/'):
                rbranch = self.div()
            if(self.symbol.value == '*'):
                symbol = '*'
                rbranch = self.mul()
            tt.add_branch(Tree(symbol))
            tt.add_branch(rbranch)
        if(flag):
            tt = lbranch
        return  tt
    def expression(self):
        """ expression ::= [term+-term]
        """
        t = Tree(Lexeme('', ''))
        sign = 1
        if(self.symbol.value == '+'):
            t.add_branch(Tree(self.symbol))
            self.next('+')
        if(self.symbol.value == '-'):
            t.add_branch(Tree(self.symbol))
            self.next('-')
            sign = -1
        lbranch = self.term()
        t.add_branch(lbranch)
        flag = True
        while (self.symbol.value in ['+', '-']):
            flag = False
            symbol = self.symbol
            if(self.symbol.value =='+'):
                rbranch = self.add()
            if(self.symbol.value =='-'):
                rbranch = self.sub()
            t.add_branch(Tree(symbol))
            t.add_branch(rbranch)
        if(flag):
            t = lbranch
        return  t
    def atom(self):
        """atom ::= factor^factor
        """
        t = Tree(Lexeme('', ''))
        lbranch = self.factor()
        t.add_branch(lbranch)
        flag = True
        while (self.symbol.value == '^'):
            flag = False
            t.add_branch(Tree(self.symbol))
            self.next('^')
#            (cc, rbranch) = self.expression()
            rbranch = self.factor()
            t.add_branch(rbranch)
        if(flag):
            t = lbranch
        return  t
    def function_call(self):
        pass
    def factor(self):
        """ factor = (expression) | number
        """
        t = Tree(Lexeme('', ''))
        if(self.symbol.value == '('):
            t.add_branch(Tree(self.symbol))
            self.next('(')
            branch = self.expression()
            t.add_branch(branch)
            symbol = self.symbol
            self.next(')')
            t.add_branch(Tree(symbol))
            return  t
        else:
            symbol = self.symbol
            c = self.symbol.value
            self.next()
            if(symbol.type == self.lexer.types):
                try:
                    t = Tree(symbol)
                except ValueError as e:
                    raise ParserError(self.symbol, self.lineNum, self.symbolNum)
            if(symbol.type == 'id'):
               if(self.exists_in_env(symbol)):
                   # Att! If funcname == id name, it will bad
                   type = self.get_type_in_env()
                   if(type == 'func'):
                       t = self.function_call()
                   else:
                       symbol.type = type
                       t = Tree(symbol)
               else:
                   self.error('undefined')
            return  t
    def next(self, *args, **kwargs):
        if(len(args) !=0):
            if(args[0] != self.symbol.value):
                raise ParserError(self.symbol, self.lineNum, self.symbolNum , '')
        try:
            self.symbol = self.lexer.getToken()
        except EOFError as e:
            raise ParserError(self.symbol, self.lineNum, self.symbolNum)
    def error(self, message = None):
        raise ParserError(self.symbol, self.lineNum, self.symbolNum, message)

