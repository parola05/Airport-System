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
        self.queueInTheAir: Dict[str:List[RequestFromAirplane]] = {} # AirlineID : List[RequestFromAirplane]
        self.requestsInProcess: Dict[str:RequestFromAirplane] = {}  # AirplaneID : RequestFromAirplane
        self.queueInTheAirMaxSize = queueInTheAirMaxSize
        self.avgTimeInQueueInTheAir = 0
        self.numberOfAirplaneThatLand = 0
        self.lockRequests: Dict[str:RequestFromAirplane] = {} 

    async def setup(self): 
        receiveBehaviour:ReceiveBehaviour = ReceiveBehaviour()
        self.add_behaviour(receiveBehaviour)

    def removeAirplaneFromQueue(self,airlineID,airplaneID):
        if airlineID in self.queueInTheAir:
            indexToRemove = 0
            index = 0
            for request in self.queueInTheAir[airlineID]:
                if request.id == airplaneID:
                    indexToRemove = index
                index += 1
            del self.queueInTheAir[airlineID][indexToRemove]
    
    def closestStationToRunway(self,runwayCoord:Coord, stations):
        runwayCoordTuple = (runwayCoord.x, runwayCoord.y)
        firstStationCoord = (stations[0].coord.x, stations[0].coord.y)
        minDistance = dist(firstStationCoord, runwayCoordTuple)
        minStation = stations[0]
        for st in stations:
            stationCoordTuple = (st.coord.x, st.coord.y)
            distance = dist(stationCoordTuple, runwayCoordTuple)
            if distance < minDistance:
                minStation = st
        return minStation # objeto Station