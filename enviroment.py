class Enviroment():
    def __init(self, top):
        self.dict = {}
        self.top = top
    def __contains__(self, item):
        if(item in self.dict):
            return True
        return False