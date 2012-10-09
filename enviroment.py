class Enviroment():
    def __init__(self, top):
        self.dict = {}
        self.top = top
    def __contains__(self, item):
        s = [x.value for x in self.dict.keys()]
        if(item.value in s):
            return True
        return False