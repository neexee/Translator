from node import Node

class Constant(Node):
    def generateCode(self, startMark):
        return (str(startMark) + ': LOAD_CONST ' + self.name + '\n', startMark+1)

