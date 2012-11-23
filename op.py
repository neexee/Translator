from node import Node
class Operator(Node):
    def __init__(self, name):
        super().__init__(name, 'operator')
    def __repr__(self):
        str = ''
        for b in self.branches:
            str += b.__repr__()
        str = '<operator name=\'' +self.name + '\'>\n' + str +'</operator>\n'
        return str
    def generateCode(self, startMark):
        if self.name == '=':

            (right, startMark) = self.branches[1].generateCode(startMark)
            left = self.branches[0]
            if left.scope:
                c = str(startMark)+': STORE_FAST '
            else:
                c = str(startMark)+': STORE_GLOBAL '
            startMark+=1
            code = right + c + left.name+ '\n'
            return  (code, startMark)

        (left, startMark) = self.branches[0].generateCode(startMark)
        (right, startMark) = self.branches[1].generateCode(startMark)
        strm = str(startMark)
        funcName = {
                       '+' : lambda : 'BINARY_ADD\n',
                       '-' : lambda : 'BINARY_SUB\n',
                       '/' : lambda : 'BINARY_DIV\n',
                       '*' : lambda : 'BINARY_MUL\n',
                       '==': lambda : 'COMPARE_EQ\n',
                       '+=': lambda : 'UNARY_ADD\n',
                       '<' : lambda : 'COMPARE_LEFT\n',
                       '>' : lambda : 'COMPARE_RIGHT\n'
                   }[self.name]()
        funcName = strm + ': '+ funcName
        code = left  + right + funcName
        return (code, startMark+1)
