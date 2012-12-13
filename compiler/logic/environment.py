class Environment():
    def __init__(self, top):
        self.dict = {}
        self.top = top
    def __contains__(self, item):
        if(item.value in self.dict):
            return True
        return False