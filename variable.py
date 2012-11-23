from node import Node

class Variable(Node):
    def __init__(self, name, type, local):
        """ if local == true. variable in local scope """
        super().__init__(name, type)
        self.scope = local
    def generateCode(self, startMark):
        if self.scope:
            return (str(startMark)+ ': LOAD_FAST ' + self.name + '\n', startMark+1)
        else:
            return (str(startMark) +': LOAD_GLOBAL ' + self.name +'\n', startMark+1)