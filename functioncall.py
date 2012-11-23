from node import Node

class FunctionCall(Node):
    def __init__(self, name, params):
        super().__init__(name, 'funcall')
        self.params = params
    def __repr__(self):
        str = '<funcall name =\'' +self.name + '\'>\n'
        for x in  self.params:
            str += '<param>\n' + x.__repr__() + '</param>\n'
        return str + '</funcall>\n'
    def generateCode(self, startMark):
        code = str(startMark) + ': LOAD_GLOBAL ' + self.name + '\n'
        for p in self.params:
            (c, startMark) = p.generateCode(startMark+1)
            code+=c
        code+=str(startMark)+': CALL_FUNCTION ' + str(len(self.params)) + '\n'

        return (code, startMark + 1)