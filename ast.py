from lexeme import Lexeme
class AST():
    def __init__(self, lex):
        self.mark = lex.value
        self.type = lex.type
        self.branches = []
    def add_branch(self, branch):
        if(len(self.branches) ==0  and branch.type != 'func'):
            self.type = branch.type

        if(len(self.branches) == 1):
            #self.mark+= branch.mark
            if(branch.type == 'double'  or self.type =='double'):
                self.type = 'double'
        self.branches.append(branch)
        #    def set_mark(self, mark):
        #        self.mark = mark
    def __repr__(self):
        if(self.branches == []):
            return "<"+self.type+">"+self.mark+"</"+ self.type+">\n"
        else:
            str="<" + self.type + ' name=\''+self.mark+"\'>\n"
            for i in self.branches:
                str+= i.__repr__()
                #str.join(self.branches)
            str+="</"+ self.mark+ ">\n"
            return str
