from spade.agent import Agent
from typing import Dict, List
import sys, platform
from GlobalTypes.Coord import Coord
from math import dist

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")
    
from MessagesProtocol.RequestFromAirplane import RequestFromAirplane
from .behaviours.ReceiveBehaviour import ReceiveBehaviour

class ControlTower(Agent):
    def __init__(self,agent_name,password,queueInTheAirMaxSize=30):
        super().__init__(agent_name,password)
        self.queueInTheAir: Dict[str:List[RequestFromAirplane]] = {}
        self.requestsInProcess: Dict[str:RequestFromAirplane] = {}  # sender_name : RequestFromAirplane
        self.queueInTheAirMaxSize = queueInTheAirMaxSize

    async def setup(self): 
        receiveBehaviour:ReceiveBehaviour = ReceiveBehaviour()
        self.add_behaviour(receiveBehaviour)

    def removeAirplaneFromQueue(self,airline,airplaneID):
        for request in self.queueInTheAir[airline]:
            if request.id == airplaneID:
                del self.queueInTheAir[airline][request]
    
    def closestStationToRunway(runwayCoord:Coord, stationsCoords:List[Coord]) -> Coord:
        runwayCoordTuple = (runwayCoord.x, runwayCoord.y)
        firstStationCoord = (stationsCoords[0].x, stationsCoords[0].y)
        minDistance = dist(firstStationCoord, runwayCoordTuple)
        minStation = stationsCoords[0]
        for stationCoord in stationsCoords:
            stationCoordTuple = (stationCoord.x, stationCoord.y)
            distance = dist(stationCoordTuple, runwayCoordTuple)
            if distance < minDistance:
                minStation = stationCoord
        return minStation


