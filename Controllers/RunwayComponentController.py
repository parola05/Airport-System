import sys, platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\..")
else:
    print("Unsupported operating system")

from Agents.Agents import Agents
from GlobalTypes.Coord import Coord

class RunwayComponentController():
    def __init__(self) -> None:
        '''
            Get Runway Manager from Agents Singleton
        '''
        self.runwayManager = Agents().runwayManager

    def getRunways(self):
        '''
            Get a list where each item have:
                - Runways ID
                - Runways Coordinates (Coord)
                - Runways Availability (bool)
        '''
        return [
            {
                "id": "TODO",
                "position": Coord(0,0),
                "available": "TODO",
            },
            {
                "id":"TODO",
                "position": Coord(0,0),
                "available": "TODO",
            },
            {
                "id":"TODO",
                "position": Coord(0,0),
                "available": "TODO",
            },
            {
                "id":"TODO",
                "position": Coord(0,0),
                "available": "TODO",
            },
            {
                "id":"TODO",
                "position": Coord(0,0),
                "available": "TODO",
            },
            {
                "id":"TODO",
                "position": Coord(0,0),
                "available": "TODO",
            },
             {
                "id":"TODO",
                "position": Coord(0,0),
                "available": "TODO",
            },
             {
                "id":"TODO",
                "position": Coord(0,0),
                "available": "TODO",
            },
        ]