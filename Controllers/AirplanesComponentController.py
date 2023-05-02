import sys, platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\..")
else:
    print("Unsupported operating system")

from Agents.Agents import Agents
from GlobalTypes.Types import SpotType, StatusType, Priority

class AirplanesComponentController():
    def __init__(self) -> None:
        '''
            Get Airplanes from Agents Singleton
        '''
        self.airplanes = Agents().airplaines

    def getAirplanes(self):
        '''
            Get a list where each item have:
                - Airplanes ID
                - Airplanes Airline
                - Airplanes Type
                - Airplanes Priority
                - Airplanes Origin
                - Airplanes Destiny
                - Airplanes Date
                - Airplanes Time
                - Airplanes Status
        '''
        return [
            {
                "id": "TODO",
                "airline": "TODO",
                "type": "TODO",
                "priority": "TODO",
                "origin": "TODO",
                "destiny": "TODO",
                "date": "TODO",
                "time": "TODO",
                "status": StatusType.IN_STATION,
            },
            {
                "id":"TODO",
                "airline": "TODO",
                "type": "TODO",
                "priority": "TODO",
                "origin": "TODO",
                "destiny": "TODO",
                "date": "TODO",
                "time": "TODO",
                "status": "TODO",
            },
            {
                "id":"TODO",
                "airline": "TODO",
                "type": "TODO",
                "priority": "TODO",
                "origin": "TODO",
                "destiny": "TODO",
                "date": "TODO",
                "time": "TODO",
                "status": StatusType.FLYING,
            },
            {
                "id":"TODO",
                "airline": "TODO",
                "type": "TODO",
                "priority": "TODO",
                "origin": "TODO",
                "destiny": "TODO",
                "date": "TODO",
                "time": "TODO",
                "status": "TODO",
            },
            {
                "id":"TODO",
                "airline": "TODO",
                "type": "TODO",
                "priority": "TODO",
                "origin": "TODO",
                "destiny": "TODO",
                "date": "TODO",
                "time": "TODO",
                "status": "TODO",
            },
            {
                "id":"TODO",
                "airline": "TODO",
                "type": "TODO",
                "priority": "TODO",
                "origin": "TODO",
                "destiny": "TODO",
                "date": "TODO",
                "time": "TODO",
                "status": "TODO",
            },
             {
                "id":"TODO",
                "airline": "TODO",
                "type": "TODO",
                "priority": "TODO",
                "origin": "TODO",
                "destiny": "TODO",
                "date": "TODO",
                "time": "TODO",
                "status": "TODO",
            },
             {
                "id":"TODO",
                "airline": "TODO",
                "type": "TODO",
                "priority": "TODO",
                "origin": "TODO",
                "destiny": "TODO",
                "date": "TODO",
                "time": "TODO",
                "status": "TODO",
            },
        ]