import sys
import platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\..")
else:
    print("Unsupported operating system")

from Agents.Agents import Agents

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
                - Runways Coordinates
        '''
        return [
            {
                "id": "TODO",
                "x": "TODO",
                "y": "TODO",
            },
            {
                "id":"TODO",
                "x": "TODO",
                "y": "TODO",
            },
            {
                "id":"TODO",
                "x": "TODO",
                "y": "TODO",
            },
            {
                "id":"TODO",
                "x": "TODO",
                "y": "TODO",
            },
            {
                "id":"TODO",
                "x": "TODO",
                "y": "TODO",
            },
            {
                "id":"TODO",
                "x": "TODO",
                "y": "TODO",
            },
             {
                "id":"TODO",
                "x": "TODO",
                "y": "TODO",
            },
             {
                "id":"TODO",
                "x": "TODO",
                "y": "TODO",
            },
        ]