from node import Node
class Return(Node):
    def __init__(self):
        super().__init__('return', 'return')
    def __repr__(self):
        str = ''
        for b in self.branches:
            str += b.__repr__()
        str = '<return>' +self.name + '\'>\n' + str +'</return>\n'
        return str
    def generateCode(self):
        code = ''
        for f in self.branches:
            code+=f.generateCode()
        code = code + 'RETURN_VALUE\n'
        return code