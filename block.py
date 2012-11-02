from node import Node
class Block(Node):
    def __init__(self, env):
        super().__init__('', 'block')
        self.env = env
    def generateCode(self):
        code = ''
        for b in self.branches:
            code+=b.generateCode()
        return code