import sys
sys.path.append("..\\..")
from GlobalTypes import SpotType

class BuySpots():
    def __init__(self,n_spots:int,price_per_spot:float,spotType:SpotType) -> None:
        self.n_spots:int = n_spots
        self.price_per_spot:float = price_per_spot
        self.spotType:SpotType = spotType 