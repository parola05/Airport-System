from spade import Agent
from typing import Dict, List
import sys
sys.path.append("..")
from GlobalTypes.Coord import Coord

class Runway():
    def __init__(self, id: str, coord: Coord, available: bool) -> None:
        '''
            id: identificador único da pista
            coord: localização da pista
            spots_available: número de pistas disponíveis
        '''
        self.id: str = id
        self.coord: Coord = coord
        self.available: bool = available
    
    def isSpotAvailable(self):
        return self.available

class RunwayManagerAgent(Agent):
    async def setup(self):
        self.runways: Dict[str,Runway] = {}

    def addRunway(self, runway: Runway):
        if runway.id in self.runways:
            raise ValueError("This identifier was already taken by another runway")
        self.runways[runway.id] = runway

    def getRunwaysAvailable(self):
        '''
            return: list of the id's of the stations that have spot availablen for the airline 
        '''
        runwaysAvailable: List[str] = []
        for runway in self.runways:
            if self.runways[runway].isSpotAvailable():
                runwaysAvailable.append(self.runways[runway].id)
        return runwaysAvailable