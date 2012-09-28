class Tree():
    def __init__(self, mark = ''):
        self.mark = mark
        self.branches = []
    def add_branch(self, branch):
        self.branches.append(branch)
        self.mark+= branch.mark
    def set_mark(self, mark):
        self.mark = mark
    def __repr__(self):
        if(self.branches == []):
            return "<T>"+self.mark+"</T>\n"
        else:
            str="<N><mark>"+ self.mark+"</mark>\n"
            for i in self.branches:
                str+= i.__repr__()
            #str.join(self.branches)
            str+="</N>\n"
            return str
