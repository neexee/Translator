from node import Node

class Variable(Node):
    def __init__(self, name, type, local):
        """ if local == true. variable in local scope """
        super().__init__(name, type)
        self.scope = local
    def generateCode(self):
        if self.scope:
            return 'LOAD_FAST ' + self.name + '\n'
        else:
            return 'LOAD_GLOBAL ' + self.name +'\n'