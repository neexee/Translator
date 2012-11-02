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
    def generateCode(self):
        code = 'LOAD_GLOBAL ' + self.name + '\n'
        for p in self.params:
            c = p.generateCode()
            code+=c
        code+='CALL_FUNCTION ' + str(len(self.params)) + '\n'
        return code