import numpy as np

class Node(object):
    def __init__(self,name,pos,static):
        self.name = name
        self.pos = pos
        self.static = static
        self.bound = {}

    def bindTo(self,point,numPath):
        self.bound[point.name] = (point,numPath)
        point.bound[self.name] = (self,numPath)

    def selfSize(self):
        distances = [np.linalg.norm(self.pos-p[0].pos) for p in self.bound.values()]
        return sum(distances)/2
    
    def selfDelay(self):
        distances = [np.linalg.norm(self.pos-p[0].pos)*p[1] for p in self.bound.values()]
        return sum(distances)/2

    def force(self,t,mult,smoothRadius):
        total = np.zeros(3)
        for out in self.bound.values():
            f = out[0].pos - self.pos
            f_length = np.linalg.norm(f)
            if f_length < smoothRadius:
                f = (t*out[1]+(1-t)) * f / smoothRadius
            else:
                f = (t*out[1]+(1-t)) * f / f_length
            total += f
        total_length = np.linalg.norm(total)
        total = mult*total/total_length
        return total

    def moveBy(self,displacement):
        if not(self.static):
            self.pos += displacement