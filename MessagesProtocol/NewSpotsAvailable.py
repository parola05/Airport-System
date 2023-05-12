from GlobalTypes.Types import SpotType

class NewSpotsAvailable():
    def __init__(self, airline:str, spotType:SpotType, nSpots:int) -> None:
        self.airline = airline
        self.spotType:SpotType = spotType
        self.nSpots = nSpots