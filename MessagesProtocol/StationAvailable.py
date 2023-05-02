import sys
import platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from GlobalTypes.Types import SpotType

class StationAvailable():
    def __init__(self, airline: str, spotType: SpotType) -> None:
        self.airline: str = airline
        self.spotType: SpotType = spotType 