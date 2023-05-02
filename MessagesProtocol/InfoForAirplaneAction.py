import sys
import platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from GlobalTypes.Types import RequestType
from GlobalTypes.Coord import Coord

class InfoForAirplaneAction():
    def __init__(self, requestType: RequestType, stationCoord: Coord, runwayCoord: Coord) -> None:
        self.requestType: RequestType = requestType
        self.stationCoord: Coord = stationCoord
        self.runwayCoord: Coord = runwayCoord 