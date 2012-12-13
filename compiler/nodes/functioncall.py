from compiler.nodes.function import builtin
from compiler.nodes.node import Node
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
        if self.name not in [x.name for x in builtin]:
            #code = str(startMark) + ': LOAD_GLOBAL ' + self.name + '\n'
            code = ''
            for p in self.params:
                (c, startMark) = p.generateCode(startMark)
                code+=c
            code+=str(startMark)+': CALL ' + self.name + '\n'
        else:
            code = ''
            for x in builtin:
                if x.name == self.name:
                    f = x
                    break
            for p in self.params:
                (c, startMark) = p.generateCode(startMark+1)
                code+=c
            code+=str(startMark)+': ' + f.code+ ' ' + str(len(self.params)) + '\n'
        return (code, startMark + 1)
    def toasm(self):
        pass