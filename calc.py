def Node(object):
    def __init__(self,name,pos,static):
        self.name = name
        self.pos = pos
        self.static = static
        self.bound = {}

    def bindTo(self,point,numPath):
        self.bound[point.name] = numPath
        point.bound[self.name] = numPath