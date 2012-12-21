from compiler.nodes.node import Node

class While(Node):
    def __init__(self, env):
        super().__init__('while', 'while')
        self.env = env
    def generateCode(self, startMark):
        condition = self.branches[0]
        codeSection = self.branches[1]
        begin = startMark
        (code, startMark) = condition.generateCode(startMark)
        conditionMark = startMark
        (sectionCode, startMark) = codeSection.generateCode(startMark+1)
        codeBlockEnd = startMark
        code +=  str(conditionMark)+ ': JUMP_IF_FALSE ' + str(codeBlockEnd +1) + '\n' + sectionCode+ \
                 str(codeBlockEnd)+ ': JUMP ' + str(begin) +'\n'
        return (code, startMark+1)