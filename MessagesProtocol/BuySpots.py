import sys, platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from GlobalTypes.Types import SpotType

class BuySpots():
    def __init__(self, n_spots: int, price_per_spot: float, spotType: SpotType, airlineID) -> None:
        self.n_spots: int = n_spots
        self.price_per_spot: float = price_per_spot
        self.spotType: SpotType = spotType 
        self.airlineID: str = airlineID