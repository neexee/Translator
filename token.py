class Token():
    def __init__(self, value, type):
       self.value = value
       self.type = type
    def __repr__(self):
        return 'Token('+self.value+', '+self.type+')'
    def __cmp__(self, other):
        if(self.value == other.value and self.type == other.type):
            return 0
        return 1
    def __eq__(self, other):
        return self.value == other.value and self.type == other.type
    def __ne__(self, other):
        return not (self.value == other.value and self.type == other.type )