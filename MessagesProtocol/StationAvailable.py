import sys, platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from GlobalTypes.Types import SpotType
from GlobalTypes.Coord import Coord

class StationAvailable():
    def __init__(self, stationID: str, coordinates: Coord, airline: str, spotType: SpotType) -> None:
        self.stationID: str = stationID
        self.coord: Coord = coordinates
        self.airline: str = airline
        self.spotType: SpotType = spotType 