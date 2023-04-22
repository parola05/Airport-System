import random

class Coord():
    def __init__(self,x=None,y=None) -> None:
        if x != None:self.x = x
        else: self.x = random.random()
        if y != None:self.y = y
        else: self.y = random.random()