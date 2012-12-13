from compiler.nodes.node import Node
class Block(Node):
    def __init__(self, env):
        super().__init__('block', 'block')
        self.env = env
    def generateCode(self, startMark):
        code = ''
        for b in self.branches:
            (c,  startMark)=b.generateCode(startMark)
            code += c
        return (code, startMark)
    def toasm(self):
        pass