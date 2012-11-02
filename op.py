from node import Node
class Operator(Node):
    def __init__(self, name):
        super().__init__(name, 'operator')
    def __repr__(self):
        str = ''
        for b in self.branches:
            str += b.__repr__()
        str = '<operator name=\'' +self.name + '\'>\n' + str +'</operator>\n'
        return str
    def generateCode(self):
        if self.name == '=':
            left = self.branches[0]
            c = ''
            if left.scope:
                 c = 'STORE_FAST '
            else:
                c = 'STORE_GLOBAL '
            right = self.branches[1].generateCode()
            code = right + c + left.name+ '\n'
            return  code
        funcName = {
            '+' : lambda : 'BINARY_ADD\n',
            '-' : lambda : 'BINARY_SUB\n',
            '/' : lambda : 'BINARY_DIV\n',
            '*' : lambda : 'BINARY_MUL\n'
        }[self.name]()
        left = self.branches[0].generateCode()
        right = self.branches[1].generateCode()
        code = left  + right + funcName
        return code
