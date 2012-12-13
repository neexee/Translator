class GeneratorError(Exception):
    def __init__(self, message):
        self.value = message
    def __str__(self):
        return repr(self.value)

class Generator():
    def __init__(self, tree):
        self.startBlock = tree
    def generateCode(self):
        main = self.findMain()
        (code, len) = self.startBlock.generateCode(0)
        return code
    def findMain(self):
        if 'main' in  self.startBlock.env.dict:
            return self.startBlock.env.dict['main']
        else:
            raise GeneratorError('Symbol \'main\' not found')
