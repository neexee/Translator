import string
from token import Token
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
    def getToken(self):
        c = ' '

        while c  in string.whitespace:
            try:
                c = self.reader.nextChar()
            except EOFError as e:
                #print(e)
                self.reader.close()
                return Token('', 'EOF')
            if(c =='\n'):
                return Token('', 'newline')
            if(c == None):
                self.reader.close()
                return Token('', 'EOF')

        buffer = ''

        if(c in self.punct):
           return Token(c, 'punctuation')
        if(c in self.operations):
           return Token(c, 'operator')
        if(c == '\n'):
           return Token(c, "EOL")

        if(c in string.digits):
            while (c in string.digits):
                  buffer+=c
                  c= self.reader.nextChar()
            self.reader.putBack(c)
            return Token(buffer, 'int')

        while(c in string.ascii_lowercase):
            buffer+=c
            c = self.reader.nextChar()
        self.reader.putBack(c)

        if(buffer  == 'def'):
            self.parse_func = True
            return Token(buffer, 'def')
        else:
            if(self.parse_func):
                return Token(buffer, 'func')
            else:
                return Token(buffer, 'id')

