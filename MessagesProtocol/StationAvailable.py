import sys
sys.path.append("..\\..")
from GlobalTypes import SpotType

class StationAvailable():
    def __init__(self, airline: str, spotType: SpotType) -> None:
        self.airline: str = airline
        self.spotType: SpotType = spotType 