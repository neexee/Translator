from symtable import Symbol
from compiler.nodes._while import While
from compiler.nodes.block import Block
from compiler.nodes.const import Constant
from compiler.nodes.function import Function
from compiler.nodes.functioncall import FunctionCall
from compiler.nodes.node import Node
from compiler.nodes.op import Operator
from compiler.nodes._return import Return
from compiler.logic.lexeme import  Lexeme
from compiler.nodes.ifelse import IfElse
from compiler.logic.environment import Environment
from compiler.nodes.variable import Variable
from compiler.nodes.function import builtin
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
        self.currentFunction = None
        self.varnum = 0
    def get_env_value(self, symbol):
        env = self.environment
        while env != None:
            if symbol.value in env.dict:
                s = env.dict[symbol.value]
                return  s
            env = env.top
        return None
    def get_type_in_env(self, symbol):
        env = self.environment
        while env != None:
            if symbol.value in env.dict:
                s = env.dict[symbol.value]
                if s.type == 'function':
                    return 'function'
                else:
                    return s.type
            env = env.top
        return None

    def exists_in_env(self, symbol):
        env = self.environment
        local = True
        while env != None:
            if symbol.value in env.dict:
                if env != self.environment:
                    local = False
                return  (local, True)
            env = env.top
        return (False, False)

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
        t = Block(self.environment)
        while self.symbol != self.eof:
            t.add_branch(self.block())
        return t

    def block(self):
        t = Block(self.environment)
        #instructions = False
        while True:
            self.ignorenewline()
            if self.symbol.value in self.lexer.types:
                instructs = self.declaration()
                for i in instructs:
                    t.add_branch(i)
                self.next(';')
                self.ignorenewline()
        #        instructions = True
                continue
            if self.symbol.value == 'def':
         #       if instructions:
         #           break
                self.next()
                t = self.func()
                self.ignorenewline()
                break
            if self.symbol.value == '{':
                self.next()
                self.environment = Environment(self.environment)
                self.block()
                if self.environment.top != None:
                   self.environment = self.environment.top

                self.next('}')
                continue
            if self.symbol.value =='}' or self.symbol == self.eof:
                break
            if(self.symbol.value == 'if'):
         #       instructions = True
               t.add_branch(self.ifstatement())
            if(self.symbol.value == 'while'):
         #       instructions = True
                t.add_branch(self.whilestatiment())
            else:
          #      instructions = True
                t.add_branch(self.instruction())

        return t
    def whilestatiment(self):
        t = While(self.environment)
        self.next()
        self.next('(')
        t.add_branch(self.instruction(False))
        self.next(')')
        self.ignorenewline()
        self.next('{')
        t.add_branch(self.block())
        self.next('}')
        return t
    def ifstatement(self):
        t = IfElse(self.environment)
        self.next()
        self.next('(')
        t.add_branch(self.instruction(False))
        self.next(')')
        self.ignorenewline()
        self.next('{')
        t.add_branch(self.block())
        self.next('}')
        self.ignorenewline()
        if self.symbol.value =='else':
            self.ignorenewline()
            self.next()
            self.ignorenewline()
            self.next('{')

            savedvar = self.varnum
            self.varnum = 0

            t.add_branch(self.block())

            self.varnum = savedvar

            self.ignorenewline()
            self.next('}')
            self.ignorenewline()
        else:
            t.add_branch(Node('', ''))
        return t
    def instruction(self, nl = True):
        #funcall or assignment
        if self.symbol.value == 'return':
            if(self.environment.top == None):
                raise ParserError('return in global scope')
            t = Return()
            self.next()
            expr = self.expression()
            type = self.currentFunction.returnType
            etype = expr.type
            if(type == etype):
                t.add_branch(expr)
                self.next(';')
            else:
                self.error('incompatible types when returning type "' + etype +'" but "' + type + '" was expected')
            return  t
        else:
                if self.symbol.value in [x.name for x in builtin]:
                    ex = True
                    local = True
                else:
                    (local, ex) = self.exists_in_env(self.symbol)
                if ex:

                    type = self.get_type_in_env(self.symbol)
                    symbol = self.symbol
                    symbol.type = type
                    if symbol.type == 'func':
                        t = self.factor()
                        self.next(';')
                        return t
                    #t = Operator('=')
                    self.next()
                    if self.symbol.value in self.lexer.operations:
                        t = Operator(self.symbol.value)
                        self.next()
                    expr = self.expression()
                    etype = expr.type

                    #Check type expression and symbol.
                    if expr.type == 'funcall':
                        if expr.name in  [ x.name for x in builtin]:
                            for x in builtin:
                                if x.name == expr.name:
                                    function = x
                                    break
                        else:
                            function = self.get_env_value(Lexeme(expr.name, expr.type))
                        etype = function.returnType
                    if symbol.type == etype:
                        t.add_branch(Variable(symbol.value, symbol.type, local))
                        t.add_branch(expr)
                        if(nl):
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
        code = []
        if self.symbol.value in self.lexer.types:
            type = self.symbol.value
            self.next()
            while self.symbol != Lexeme(';', 'punctuation'):
                if self.symbol.type == 'id' and self.symbol not in self.environment:
                    symbol = self.symbol
                    symbol.type = type
                    self.environment.dict[symbol.value] = (type, None)
                    self.next()
                    if self.symbol == Lexeme(',', 'punctuation'):
                        self.next()
                        #variables.append(symbol)
                        continue
                    if self.symbol.value == '=':
                        self.next()
                        expr = self.expression()
                        etype = expr.type
                        #Check type expression and symbol.
                        t = Operator('=')

                        t.add_branch(Variable(symbol.value, symbol.type, True))
                        self.varnum+=1

                        if expr.type == 'funcall':
                            function = self.get_env_value(Lexeme(expr.name, expr.type))
                            etype = function.returnType
                        if etype == symbol.type:
                             self.environment.dict[symbol.value] = expr
                             t.add_branch(expr)
                             code.append(t)
                        else:
                            self.error()
                       # self.next()
                        if self.symbol == Lexeme(',', 'punctuation'):
                            self.next()
                            continue
                else:
                    self.error(self.symbol.value + ' already declared or not id')
        return code
    def eq_expr(self):
        pass

    def func(self):
        if self.symbol.value in self.lexer.types :
            returnType = self.symbol.value
        else:
            self.error('unknown return type')
        self.next()
        if self.exists_in_env(self.symbol)[1]:
            self.error( str(self.symbol) + 'already declared' )    #function already declared
        else:
            func = self.symbol
            func.type = 'func'
            self.next()
            self.next('(')
            params = self.func_params()
            self.next(')')
            self.ignorenewline()
            self.next('{')
            self.environment = Environment(self.environment)
            for param in params:
                self.environment.dict[param.name] = param
            f = Function(name=func.value, code=None,returnType=returnType, params=params)

            self.environment.top.dict[func.value] = f
            self.currentFunction = f
            body = self.block()
            f.code = body
            self.environment = self.environment.top

            self.ignorenewline()
            self.next('}')
            return f
    def ignorenewline(self):
        while self.symbol.type == 'newline':
            self.next()

    def func_params(self):
        params = []
        while self.symbol.value in self.lexer.types:
             type = self.symbol.value
             self.next()
             if self.symbol.type == 'id' and self.symbol not in self.environment:
                (local, ex) = self.exists_in_env(self.symbol)
                symbol = self.symbol
                symbol.type = type
                params.append(Variable(symbol.value, symbol.type, local))
                self.next()
                if self.symbol == Lexeme(',', 'punctuation'):
                    self.next()
                    continue
                if self.symbol == Lexeme(')', 'punctuation'):
                    break
                else:
                    self.error(') not found in function declaration')
             else:
                 self.error(self.symbol.value + ' already declared or not id')
        return params

    def func_expr(self):
        pass

    def term(self):
        """ term ::= [atom/*factor]
        """
        lbranch = self.atom()
        t = Operator('')
        t.add_branch(lbranch)
        # flag == True ==> We don't wrap tree as term. Keep it atom.
        flag = True
        # onetime == True ==> Every iteration in while() we build new tree, where old tree = left branch of it.
        onetime = False
        while self.symbol.value in ['/', '*']:
            flag = False
            tt = t
            if onetime:
                tt = Operator('')
                tt.add_branch(t)
            tt.mark = self.symbol.value
            if self.symbol.value == '/':
                rbranch = self.div()
                tt.name = '/'
            if self.symbol.value == '*':
                rbranch = self.mul()
                tt.name = '*'
            tt.add_branch(rbranch)
            onetime = True
            t = tt
        if(flag):
            t = lbranch
        return  t
    def expression(self):
        """ expression ::= [term+-term]
        """
        t = Operator( '')
        sign = 1
        # I have no good idea for unary [+/-]
        if self.symbol.value == '+' :
            # ignore this operator
            #t.add_branch(Tree(self.symbol))
            self.next()
        if self.symbol.value == '-':
            t.add_branch(Node(self.symbol.value, self.symbol.type))
            self.next()
            sign = -1
        lbranch = self.term()
        t.add_branch(lbranch)
        flag = True
        onetime = False
        while self.symbol.value in ['+', '-']:
            flag = False
            if(onetime):
                tt = Operator('')
                tt.add_branch(t)
            else:
                tt = Operator('')
                tt.add_branch(lbranch)
            symbol = self.symbol
            if self.symbol.value =='+':
                rbranch = self.add()
                tt.name = '+'
            if self.symbol.value =='-':
                rbranch = self.sub()
                tt.name = '-'
            tt.mark = symbol.value
            tt.add_branch(rbranch)
            t = tt
            onetime = True
        if flag:
            t = lbranch
        return  t
    def atom(self):
        """atom ::= factor^factor
        """
        t = Operator('')
        lbranch = self.factor()
        t.add_branch(lbranch)
        flag = True
        onetime = False
        while self.symbol.value == '^':
            flag = False
            tt = t
            if(onetime):
                tt = Node()
                tt.add_branch(t)
            self.next()
            rbranch = self.factor()
            tt.add_branch(rbranch)
            t = tt
            onetime = True
        if flag:
            t = lbranch
        return  t
    def function_call(self):
        if self.symbol.value in [x.name for x in builtin]:
           for x in builtin:
               if x.name == self.symbol.value:
                   function = x
                   break
        else:
            function = self.get_env_value(self.symbol)
        params = function.params
        self.next()
        self.next('(')
        p = []
        for paramnum in range(0, len(params)):
            param = params[paramnum]
            type = param.type
            expr = self.expression()
            type_passed = expr.type
            if(expr.type == 'funcall'):
                type_passed = self.get_env_value(Lexeme(expr.name,'')).returnType
            if type == type_passed:
                self.symbol.type = type_passed
                p.append(expr)
                self.next()
                if self.symbol == Lexeme(',', 'punctuation'):
                    self.next()
                    continue
            else:
                    self.error('parameter type mismatch, defined ' + type + ', passed '+ type_passed)
            #else:
            #    self.error('undefined')
        #self.next(')')
        t = FunctionCall(function.name, p)
        return t
    def factor(self):
        """ factor = (expression) | number
        """
        t = Operator('')
        if self.symbol.value == '(':
            self.next('(')
            branch = self.expression()
            t.add_branch(branch)
            self.next(')')
        else:
            symbol = self.symbol
            c = self.symbol.value
            if symbol.type in self.lexer.types:
                try:
                    t = Constant(symbol.value, symbol.type)
                    self.next()
                except ValueError as e:
                    raise ParserError(self.symbol, self.lineNum, self.symbolNum)
                return t
            if symbol.type == 'id':
               (local, exist) = self.exists_in_env(symbol)
               if symbol.value in [x.name for x in builtin]:
                   type = 'function'
                   symbol.type = 'function'
               else:
                    if exist:
                        type = self.get_type_in_env(symbol)
                        symbol.type = type
                    else:
                        self.error('unknown symbol')
                   # Att! If funcname == id name, it will bad
            else:
                self.error('unknown symbol type')
            if symbol.type == 'function':
                    t = self.function_call()
            else:
                    symbol.type = type
                    t = Variable(symbol.value, symbol.type, local)
                    self.next()
        return  t
    def next(self, *args, **kwargs):
        if len(args) !=0:
            if args[0] != self.symbol.value:
                raise ParserError(self.symbol, self.lexer.linenum, self.lexer.symbolnum , '')
        try:
            self.symbol = self.lexer.getToken()
        except EOFError as e:
            raise ParserError(self.symbol, self.lexer.linenum, self.lexer.symbolnum)
    def error(self, message = None):
        raise ParserError(self.symbol, self.lexer.linenum, self.lexer.symbolnum, message)
