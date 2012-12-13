from compiler.nodes.node import  Node
class IfElse(Node):
    def __init__(self, env):
        super().__init__('if', 'if')
        self.env = env

    def generateCode(self, startMark):
        code = ''
        condition = self.branches[0]
        trueSection = self.branches[1]
        falseSection = self.branches[2]
        (code, startMark) = condition.generateCode(startMark)
        conditionMark = startMark
        (truecode, startMark) = trueSection.generateCode(startMark)
        endOfTrue= startMark
        (falsecode, startMark) = falseSection.generateCode(startMark)
        endOfFalse = startMark
        if endOfFalse == endOfTrue:
            code +=  str(conditionMark)+ ': JUMP_IF_FALSE ' + str(endOfTrue) + '\n' + truecode
        else:
            code += str(conditionMark)+ ': JUMP_IF_FALSE ' + str(endOfTrue +1) + '\n' \
                    + truecode + str(endOfTrue) +': JUMP ' + str(endOfFalse) + '\n' + falsecode
        return (code, startMark)