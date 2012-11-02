from node import Node
class Function(Node):
    def __init__(self, name, code, returnType, params):
        super().__init__(name, 'function')
        self.returnType = returnType
        self.params = params
        self.code = code
    def __repr__(self):
        p = ', '.join([x.__repr__() for x in self.params])
        return super.__repr__() + ' params: [' + p + '], return type: '  + self.returnType + ', code: '+ self.code.__repr()
    def generateCode(self):
        c = '#Disassembly function ' + self.name + '\n'
        c += self.code.generateCode()
        return c
