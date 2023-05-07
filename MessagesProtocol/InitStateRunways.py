class InitStateRunways():
    def __init__(self) -> None:
        self.runways = []

class RunwayInfo():
    def __init__(self,id,coord,available) -> None:
        self.id = id 
        self.coord = coord
        self.available = available