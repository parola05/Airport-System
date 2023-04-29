import sys
import platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\..")
else:
    print("Unsupported operating system")

from Agents.Agents import Agents

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
                - Airplanes Origin
                - Airplanes Destiny
                - Airplanes Date
                - Airplanes Time
        '''
        return [
            {
                "id": "TODO",
                "airline": "TODO",
                "type": "TODO",
                "origin": "TODO",
                "destiny": "TODO",
                "date": "TODO",
                "time": "TODO",
                "stauts": "TODO",
            },
            {
                "id":"TODO",
                "airline": "TODO",
                "type": "TODO",
                "origin": "TODO",
                "destiny": "TODO",
                "date": "TODO",
                "time": "TODO",
                "stauts": "TODO",
            },
            {
                "id":"TODO",
                "airline": "TODO",
                "type": "TODO",
                "origin": "TODO",
                "destiny": "TODO",
                "date": "TODO",
                "time": "TODO",
                "stauts": "TODO",
            },
            {
                "id":"TODO",
                "airline": "TODO",
                "type": "TODO",
                "origin": "TODO",
                "destiny": "TODO",
                "date": "TODO",
                "time": "TODO",
                "stauts": "TODO",
            },
            {
                "id":"TODO",
                "airline": "TODO",
                "type": "TODO",
                "origin": "TODO",
                "destiny": "TODO",
                "date": "TODO",
                "time": "TODO",
                "stauts": "TODO",
            },
            {
                "id":"TODO",
                "airline": "TODO",
                "type": "TODO",
                "origin": "TODO",
                "destiny": "TODO",
                "date": "TODO",
                "time": "TODO",
                "stauts": "TODO",
            },
             {
                "id":"TODO",
                "airline": "TODO",
                "type": "TODO",
                "origin": "TODO",
                "destiny": "TODO",
                "date": "TODO",
                "time": "TODO",
                "stauts": "TODO",
            },
             {
                "id":"TODO",
                "airline": "TODO",
                "type": "TODO",
                "origin": "TODO",
                "destiny": "TODO",
                "date": "TODO",
                "time": "TODO",
                "stauts": "TODO",
            },
        ]