from compiler.nodes.node import Node
from compiler.nodes.variable import Variable

class Function(Node):
    def __init__(self, name, code, returnType, params):
        super().__init__(name, 'function')
        self.returnType = returnType
        self.params = params
        self.code = code
    def __repr__(self):
        p = ', '.join([x.__repr__() for x in self.params])
        return super.__repr__() + ' params: [' + p + '], return type: '  + self.returnType + ', code: '+ self.code.__repr()
    def generateCode(self, startMark):
        code = ''
        startMark = 0
        for p in reversed(self.params):
            code += str(startMark) + ': STORE_FAST ' +p.name + '\n'
            startMark+=1
        (codec, startMark) = self.code.generateCode(startMark)
        code+=codec
        c = 'function ' + self.name +' '+str(startMark - 1)+ '\n'
        return (c+ code, startMark)
    def toasm(self):
        pass
builtin = [Function('print', 'PRINT', 'int', [Variable('a', 'int', True)])]
