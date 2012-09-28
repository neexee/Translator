import string
from lexeme import Lexeme
class LexerError(Exception):
    def __init__(self, value):
        self.value = 'Lexer error on symbol '+ value
    def __str__(self):
        return repr(self.value)
class Lexer:
    def __init__(self, reader):
        self.reader = reader
        self.operations = ['*', '/', '-', '+', '^']
        self.punct = ['(', ')']
    def getToken(self):
        c = ' '
        while c  in string.whitespace:
            try:
                c = self.reader.nextChar()
            except EOFError as e:
                print(e)
                self.reader.close()
                return Lexeme('', 'Expected EOF')
        buffer = ''

        if(c in self.punct):
           return Lexeme(c, 'punctuation')
        if(c in self.operations):
           return Lexeme(c, 'operation')
        if(c == '\n'):
           return Lexeme(c, "EOL")

        while (c in string.digits):
              buffer+=c
              c= self.reader.nextChar()
        self.reader.putBack(c)
        if(buffer != ''):
           return Lexeme(buffer, 'digit')

        raise LexerError(c)

