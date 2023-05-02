import sys, platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\..")
else:
    print("Unsupported operating system")
    
from Agents.Agents import Agents

class StationComponentController():
    def __init__(self) -> None:
        '''
            Get Station Manager from Agents Singleton
        '''
        self.stationManager = Agents().stationManager

    def getStations(self):
        '''
            Get a list where each item have:
                - Station ID
                - Station commercial spots capacity
                - Station merchandise spots capacity
        '''
        
        return [
            {
                "id":"TODO",
                "commercialSpots":"TODO",
                "merchandiseSpots":"TODO"
            },
            {
                "id":"TODO",
                "commercialSpots":"TODO",
                "merchandiseSpots":"TODO",
            },
            {
                "id":"TODO",
                "commercialSpots":"TODO",
                "merchandiseSpots":"TODO"
            },
            {
                "id":"TODO",
                "commercialSpots":"TODO",
                "merchandiseSpots":"TODO"
            },
            {
                "id":"TODO",
                "commercialSpots":"TODO",
                "merchandiseSpots":"TODO"
            },
            {
                "id":"TODO",
                "commercialSpots":"TODO",
                "merchandiseSpots":"TODO"
            },
             {
                "id":"TODO",
                "commercialSpots":"TODO",
                "merchandiseSpots":"TODO"
            },
             {
                "id":"TODO",
                "commercialSpots":"TODO",
                "merchandiseSpots": "TODO"
            },
        ]