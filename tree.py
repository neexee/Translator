from lexeme import Lexeme
class Tree():
    def __init__(self, lex = Lexeme('', '')):
        self.mark = lex
        self.type = lex.type
        self.branches = []
    def add_branch(self, branch):
        self.branches.append(branch)
        self.mark.value+= branch.mark.value
        if(branch.type == 'double'  or self.type =='double'):
            self.type = 'double'
#    def set_mark(self, mark):
#        self.mark = mark
    def __repr__(self):
        if(self.branches == []):
            return "<T type='"+self.mark.type+"'>"+self.mark.value+"</T>\n"
        else:
            str="<N mark='"+ self.mark.value+" type='"+ self.type+"'>\n"
            for i in self.branches:
                str+= i.__repr__()
            #str.join(self.branches)
            str+="</N>\n"
            return str
