from spade.agent import Agent
import random
import datetime
from GlobalTypes.Types import SpotType, StatusType, Priority
from .behaviours.InformDashboardInitStateBehaviour import InformDashBoardInitStateBehaviour
from .behaviours.wantsToLand import WantsToLandBehaviour
from .behaviours.receiveBehaviour import ReceiveBehaviour

class AirplaneAgent(Agent):
    def __init__(
            self, 
            agent_name, 
            password, 
            airplaneID, 
            airline,
            typeTransport=None, 
            origin=None, 
            destination=None, 
            date=None, 
            priority=None,
            stationPark=None, # objeto Station
            status:StatusType=StatusType.FLYING):
        super().__init__(agent_name,password)
        
        self.airplaneID = airplaneID
        self.airline = airline
        
        if typeTransport == None:
            self.typeTransport = self.getRandomTypeTransport()
        else: self.typeTransport = typeTransport
        
        if origin is not None:
            self.origin = origin
       
        if destination is not None:
            self.destination = destination
        
        if date == None:
            self.datetime = datetime.datetime.now()
        else: self.datetime = datetime 

        if priority == None:
            self.priority = self.getRandomPriority()
        else: self.priority = priority

        self.status = status

    async def setup(self):
        informDashBoardInitStateBehaviour:InformDashBoardInitStateBehaviour = InformDashBoardInitStateBehaviour()
        wantsToLandBehaviour:WantsToLandBehaviour = WantsToLandBehaviour()
        receiveBehaviour:ReceiveBehaviour = ReceiveBehaviour()

        self.add_behaviour(informDashBoardInitStateBehaviour)
        
        # TODO add condition to only automatic airplanes generated add this behaviour in setup
        self.add_behaviour(wantsToLandBehaviour)

        self.add_behaviour(receiveBehaviour)

    def getRandomTypeTransport(self):
        randomChoice = random.randint(0,9)
        if randomChoice % 2 == 0:
            return SpotType.COMMERCIAL
        else:
            return SpotType.MERCHANDISE
        
    def getRandomPriority(self):
        randomChoice = random.randint(0,15)
        if randomChoice % 3 == 0:
            return Priority.LOW
        elif randomChoice % 2 == 0:
            return Priority.MEDIUM
        else:
            return Priority.HIGH