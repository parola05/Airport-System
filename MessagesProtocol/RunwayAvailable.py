import sys, platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from GlobalTypes.Types import SpotType
from GlobalTypes.Coord import Coord

class RunwayAvailable():
    def __init__(self, runwayID: str, coordinates: Coord) -> None:
        self.runwayID: str = runwayID
        self.coord: Coord = coordinates 