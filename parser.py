import string
from  math import pow
from ast import AST
from function import Function
import tree
from lexeme import  Lexeme
from environment import Environment

from tree import Tree
class ParserError(Exception):
    def __init__(self, symbol, lineNum, symbolNum, message):
        self.value = '['+repr(lineNum)+':'+repr(symbolNum)+']'+\
                     ' Parse error on symbol "'+symbol.value+'" ('+symbol.type+')'+\
                     ' : '+ str(message)
    def __str__(self):
        return repr(self.value)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.symbol = lexer.getToken()
        self.symbolNum=1
        self.lineNum =1
        self.environment = Environment(None)
        self.eof = Lexeme('', 'EOF')
        self.functions = []
    def get_env_value(self, symbol):
        env = self.environment
        while(env != None):
            if(symbol.value in env.dict):
                s = env.dict[symbol.value]
                if(s == None):
                    continue
                    #s[1] = value
                return s[1]
            env = env.top
        return None
    def get_type_in_env(self, symbol):
        env = self.environment
        while(env != None):
            if(symbol.value in env.dict):
                s = env.dict[symbol.value]
                if(s != None):
                    return s[0]
            env = env.top
        return None

    def exists_in_env(self, symbol):
        env = self.environment

        while(env != None):
            if(symbol.value in env.dict):
                if(symbol in env):
                    return True
            env = env.top
        return False

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
    def program(self):
        t = AST(Lexeme('program', 'program'))
        while(self.symbol != self.eof):
            t.add_branch(self.block())
        return t

    def block(self):
        self.environment = Environment(self.environment)
        t = AST(Lexeme('block', 'block'))
        while(True):
            self.ignorenewline()
            if(self.symbol.value in self.lexer.types):
                self.declaration()
                self.next(';')
                self.ignorenewline()
                continue
            if(self.symbol.value == 'def'):
                self.next()
                t.add_branch(self.func())
                self.ignorenewline()
                continue
            if(self.symbol.value == '{'):
                self.next()
                self.block()
                self.next('}')
                continue
            if(self.symbol.value =='}' or self.symbol == self.eof):
                return t
            #if(self.symbol.type == 'newline'):
            #    self.error('expected EOF, not found \'}\'')
            else:
                t.add_branch(self.instruction())

    def instruction(self):
        #funcall or assignment
        if(self.exists_in_env(self.symbol)):
                type = self.get_type_in_env(self.symbol)
                symbol = self.symbol
                symbol.type = type
                if(symbol.type == 'func'):
                     #t = AST(symbol)
                     t = self.factor()
                     self.next(';')
                     return t
                t = AST(Lexeme('=', 'operator'))
                self.next()
                self.next('=')
                expr = self.expression()
                etype = expr.type
                #Check type expression and symbol.
                if(expr.type == 'func'):
                    function = self.get_env_value(Lexeme(expr.mark, expr.type))
                    etype = function.returnType
                if(symbol.type == etype):
                    t.add_branch(AST(symbol))
                    t.add_branch(expr)
                    self.next(';')
                    self.next()
                    return t
                else:
                    self.error('unexpected assignment ' + expr.type + ' to ' + symbol.type)
        else:
            self.error('undefined or rvalue')
    # I have no idea what I'm doing
    def declaration(self):
        # int i =0, k;
        # int s = f()
        #variables = []
        if(self.symbol.value in self.lexer.types):
            type = self.symbol.value
            self.next()
            while(self.symbol != Lexeme(';', 'punctuation')):
                if(self.symbol.type == 'id' and self.symbol not in self.environment):
                    symbol = self.symbol
                    symbol.type = type
                    self.environment.dict[symbol.value] = (type, None)
                    self.next()
                    if(self.symbol == Lexeme(',', 'punctuation')):
                        self.next()
                        #variables.append(symbol)
                        continue
                    if(self.symbol == Lexeme('=', 'operator')):
                        self.next()
                        expr = self.expression()
                        etype = expr.type
                        #Check type expression and symbol.
                        if(expr.type == 'func'):
                            function = self.get_env_value(Lexeme(expr.value, expr.type))
                            etype = function.returnType
                        if(etype == symbol.type):
                             self.environment.dict[symbol.value] = (symbol.type, expr)
                        else:
                            self.error()
                       # self.next()
                        if(self.symbol == Lexeme(',', 'punctuation')):
                            self.next()
                            continue
                else:
                    self.error(self.symbol.value + ' already declared or not id')
    def eq_expr(self):
        pass

    def func(self):
        if(self.symbol.value in self.lexer.types):
            returnType = self.symbol.value
        else:
            self.error('unknown return type')
        self.next()
        if( self.exists_in_env(self.symbol)):
            self.error(self.symbol + 'already declared' )    #function already declared
        else:
            func = self.symbol
            func.type = 'func'
            #self.enviroment.dict[self.symbol] = ''
            self.next()
            self.next('(')
            params = self.func_params()
            self.next(')')
            self.environment.dict[func.value] = (func.type, Function(returnType, params))
            for param in params:
                self.environment.dict[param.value] = (param.type, None)
            self.ignorenewline()
            self.next('{')
            body = self.block()
            # temp
            body.type = 'func'
            body.mark = func.value
            self.ignorenewline()
            self.next('}')
            return body
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
                    self.error(') not found in function declaration')
             else:
                 self.error(self.symbol.value + ' already declared or not id')
                    #self.next()
        return params

    def func_expr(self):
        pass

    def term(self):
        """ term ::= [atom/*factor]
        """
        lbranch = self.atom()
        t = AST(Lexeme('', ''))
        t.add_branch(lbranch)
        # flag == True ==> We don't wrap tree as term. Keep it atom.
        flag = True
        # onetime == True ==> Every iteration in while() we build new tree, where old tree = left branch of it.
        onetime = False
        while (self.symbol.value in ['/', '*']):
            flag = False
            tt = t
            if(onetime):
                tt = AST(Lexeme('', ''))
                tt.add_branch(t)
            tt.mark = self.symbol.value
            if(self.symbol.value == '/'):
                rbranch = self.div()
            if(self.symbol.value == '*'):
                rbranch = self.mul()
            tt.add_branch(rbranch)
            onetime = True
            t = tt
        if(flag):
            t = lbranch
        return  t
    def expression(self):
        """ expression ::= [term+-term]
        """
        t = AST(Lexeme('', ''))
        sign = 1
        # I have no good idea for unary [+/-]
        if(self.symbol.value == '+'):
            # ignore this operator
            #t.add_branch(Tree(self.symbol))
            self.next()
        if(self.symbol.value == '-'):
            t.add_branch(AST(self.symbol))
            self.next()
            sign = -1
        lbranch = self.term()
        t.add_branch(lbranch)
        flag = True
        onetime = False
        while (self.symbol.value in ['+', '-']):
            flag = False
            tt = t
            if(onetime):
                tt = AST(Lexeme('', ''))
                tt.add_branch(t)
            symbol = self.symbol
            if(self.symbol.value =='+'):
                rbranch = self.add()
            if(self.symbol.value =='-'):
                rbranch = self.sub()
            tt.mark = symbol.value
            tt.add_branch(rbranch)
            t = tt
            onetime = True
        if(flag):
            t = lbranch
        return  t
    def atom(self):
        """atom ::= factor^factor
        """
        t = AST(Lexeme('', ''))
        lbranch = self.factor()
        t.add_branch(lbranch)
        flag = True
        onetime = False
        while (self.symbol.value == '^'):
            flag = False
            tt = t
            if(onetime):
                tt = AST(Lexeme('', ''))
                tt.add_branch(t)
            #tt.add_branch(Tree(self.symbol))
            self.next()
#            (cc, rbranch) = self.expression()
            rbranch = self.factor()
            tt.add_branch(rbranch)
            t = tt
            onetime = True
        if(flag):
            t = lbranch
        return  t
    def function_call(self):
        function = self.get_env_value(self.symbol)
        params = function.params
        t = AST(self.symbol)
        self.next()
        self.next('(')
        for paramnum in range(0, len(params)):
            param = params[paramnum]
            name = param.value
            type = param.type
            if(self.exists_in_env(self.symbol)):
                type_passed = self.get_type_in_env(self.symbol)
                if(type == type_passed):
                    self.symbol.type = type_passed
                    t.add_branch(AST(self.symbol))
                    self.next()
                    if(self.symbol == Lexeme(',', 'punctuation')):
                        self.next()
                        continue
                else:
                    self.error('parameter type mismatch, defined ' + type + ', passed '+ type_passed)
            else:
                self.error('undefined')
        self.next(')')
        return t
    def factor(self):
        """ factor = (expression) | number
        """
        t = AST(Lexeme('', ''))
        if(self.symbol.value == '('):
            #t.add_branch(Tree(self.symbol))
            self.next('(')
            branch = self.expression()
            t.add_branch(branch)

            #symbol = self.symbol
            self.next(')')
            #t.add_branch(Tree(symbol))
        else:
            symbol = self.symbol
            c = self.symbol.value

            if(symbol.type in self.lexer.types):
                try:
                    t = AST(symbol)
                    self.next()
                except ValueError as e:
                    raise ParserError(self.symbol, self.lineNum, self.symbolNum)
                return t
            if(symbol.type == 'id'):
               if(self.exists_in_env(symbol)):
                   type = self.get_type_in_env(symbol)
                   symbol.type = type
               else:
                   self.error('unknown symbol')
                   # Att! If funcname == id name, it will bad
            else:
                self.error('unknown symbol type')
            if(symbol.type == 'func'):
                    t = self.function_call()
            else:
                    symbol.type = type
                    t = AST(symbol)
                    self.next()

                    #self.error('unknown function')

        return  t
    def next(self, *args, **kwargs):
        if(len(args) !=0):
            if(args[0] != self.symbol.value):
                raise ParserError(self.symbol, self.lexer.linenum, self.lexer.symbolnum , '')
        try:
            self.symbol = self.lexer.getToken()
        except EOFError as e:
            raise ParserError(self.symbol, self.lexer.linenum, self.lexer.symbolnum)
    def error(self, message = None):
        raise ParserError(self.symbol, self.lexer.linenum, self.lexer.symbolnum, message)

