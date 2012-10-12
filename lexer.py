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
        self.types = ['int', 'double']
        self.keywords = ['return', 'def']
        self.operations = ['*', '/', '-', '+', '^', '=']
        self.punct = ['(', ')', '{', '}', ';', ',']
        self.parse_func = False
        self.symbolnum = 1
        self.linenum = 1
    def getToken(self):
        c = ' '

        while c  in string.whitespace:
            try:
                c = self.reader.nextChar()
                self.symbolnum +=1
            except EOFError as e:
                #print(e)
                self.reader.close()
                return Lexeme('', 'EOF')
            if(c =='\n'):
                self.symbolnum = 1
                self.linenum +=1
                return Lexeme('', 'newline')
            if(c == None):
                self.reader.close()
                return Lexeme('', 'EOF')

        buffer = ''

        if(c in self.punct):
           return Lexeme(c, 'punctuation')
        if(c in self.operations):
           return Lexeme(c, 'operator')
        if(c == '\n'):
           return Lexeme(c, "EOL")

        if(c in string.digits):
            while (c in string.digits):
                  buffer+=c
                  c= self.reader.nextChar()
            self.reader.putBack(c)
            return Lexeme(buffer, 'int')

        while(c in string.ascii_lowercase):
            buffer+=c
            c = self.reader.nextChar()
        self.reader.putBack(c)

        if(buffer  == 'def'):
            self.parse_func = True
            return Lexeme(buffer, 'def')
        else:
            if(self.parse_func):
                self.parse_func = False
                return Lexeme(buffer, 'func')
            else:
                return Lexeme(buffer, 'id')

