from node import Node

class Constant(Node):
    def generateCode(self):
        return 'LOAD_CONST ' + self.name + '\n'

