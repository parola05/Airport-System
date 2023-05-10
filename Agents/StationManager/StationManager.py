import sys, platform
if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
    sys.path.append("../../")
elif platform.system() == "Windows":
    sys.path.append("..") 
    sys.path.append("..\\..") 
else:
    print("Unsupported operating system")
from spade.agent import Agent
from typing import Dict, List
from spade.template import Template
from GlobalTypes.Coord import Coord
from GlobalTypes.Types import SpotType
from .behaviours.ReceiveSpotQueryBehaviour import ReceiveSpotQueryBehaviour
from .behaviours.ReceiveAirlinesProposalsBehaviour import ReceiveAirlinesProposalsBehaviour
from .behaviours.EvaluateAirlinesProposalsBehaviour import EvaluateAirlinesProposalsBehaviour
from .behaviours.InformDashboardInitStateBehaviour import InformDashBoardInitStateBehaviour
from .behaviours.UpdateStationAvailabilityBehaviour import UpdateStationAvailabilityBehaviour
import datetime

class Station():
    def __init__(self, id: str, coord: Coord, merchandise_spots: int, commercial_spots: int) -> None:
        '''
            id: Station unique identifier
            coord: Station Location
            spots_available_merchandise: number of spots available for merchandise planes
            spots_available_transport: number of spots available for transport planes
            spots_merchandise: dictionary that maps an airlineID to the object {nº spots bought, nº spots available} for merchandise plane type 
            spots_commercial: dictionary that maps an airlineID to the object {nº spots bought, nº spots available} for commercial plane type 
        '''
        self.id: str = id
        self.coord: Coord = coord
        self.spots_available_merchandise: int = merchandise_spots
        self.spots_available_commercial: int = commercial_spots
        self.spots_merchandise: Dict[str, Dict[str,int]] = {}
        self.spots_commercial: Dict[str, Dict[str,int]] = {}

    '''
        Description: 
            Verify if the airline has spots yet to put their airplane in the Station
        Params: 
            - spotType: spot type (merchandise or commercial)
            - airlineID: identification of the airline
        Return:
            True if there are spots available. Otherwise, return False
    '''
    def isSpotAvailable(self, spotType: SpotType, airlineID: str):
        if spotType == SpotType.MERCHANDISE:
            if self.spots_merchandise[airlineID]["spotsAvailable"] > 0: return True
            else: return False
        elif spotType == SpotType.COMMERCIAL:
            if self.spots_commercial[airlineID]["spotsAvailable"] > 0: return True
            else: return False
        
    '''
        Description: 
            Get the number of unbought spots of type <spotType> in the Station
        Params: 
            - spotType: spot type (merchandise or commercial)
    '''
    def getNumberOfSpotsAvailableByType(self, spotType: SpotType):
        cont = 0
        if spotType == SpotType.MERCHANDISE:
            for airline in self.spots_merchandise.values():
                cont += airline["spotsBuy"]
            return self.spots_available_merchandise - cont
        elif spotType == SpotType.COMMERCIAL:
            for airline in self.spots_commercial.values():
                cont += airline["spotsBuy"]
            return self.spots_available_commercial - cont

    '''
        Description: 
            Fill <self.spots_merchandise> or <self.spots_commercial> Dict in the airlineID key
        Params: 
            - nSpots: number of spots that the airline ID wants to buy
            - spotType: spot type (merchandise or commercial)
            - airlineID: identification of the airline
        Details: 
            If the number of spots exceed the number os spots available, the airline will gonna
            buy only the number of spots available in this Station. The rest of spots will be
            bought in others Stations. 
    '''
    def buySpots(self,nSpots,spotType,airlineID):
        nSpotsAvailable = self.getNumberOfSpotsAvailableByType(spotType=spotType)
        nSpotsBuy = nSpots 
        if nSpotsAvailable < nSpots:
            nSpotsBuy = nSpotsAvailable

        if spotType == SpotType.MERCHANDISE:
            self.spots_merchandise[airlineID] = {}
            self.spots_merchandise[airlineID]["spotsBuy"] = nSpotsBuy
            self.spots_merchandise[airlineID]["spotsAvailable"] = nSpotsBuy
        elif spotType == SpotType.COMMERCIAL:
            self.spots_commercial[airlineID] = {}
            self.spots_commercial[airlineID]["spotsBuy"] = nSpotsBuy
            self.spots_commercial[airlineID]["spotsAvailable"] = nSpotsBuy

        return nSpotsBuy
        
class StationManagerAgent(Agent):
    async def setup(self):
        receiveAirlinesProposals = ReceiveAirlinesProposalsBehaviour()
        evaluateAirlinesProposals = EvaluateAirlinesProposalsBehaviour(period=5,start_at=(datetime.datetime.now() + datetime.timedelta(seconds=5)))
        receiveSpotsQueryBehaviour = ReceiveSpotQueryBehaviour()
        informDashBoardInitStateBehaviour = InformDashBoardInitStateBehaviour()
        updateStationAvailability = UpdateStationAvailabilityBehaviour()

        template1 = Template()
        template1.set_metadata("performative","propose")
        template2 = Template()
        template2.set_metadata("performative","query-if")
        template3 = Template()
        template3.set_metadata("performative","inform-ref")
        
        self.add_behaviour(receiveAirlinesProposals,template1)
        self.add_behaviour(evaluateAirlinesProposals)
        self.add_behaviour(receiveSpotsQueryBehaviour,template2)
        self.add_behaviour(informDashBoardInitStateBehaviour)
        self.add_behaviour(updateStationAvailability,template3)

    def __init__(self, agent_name, password, nStations = None, nMerchandiseSpotsPerStation = None, nCommercialSpotsPerStation = None):
        super().__init__(agent_name,password)
        self.stations: Dict[str,Station] = {}
        if nStations is not None:
            for i in range(0,nStations):
                self.addStation(Station(
                    id = 'Station_' + str(i),
                    coord = Coord(),
                    merchandise_spots = nMerchandiseSpotsPerStation, 
                    commercial_spots = nCommercialSpotsPerStation 
                ))
        self.airlinesProposals = []
        
    def addStation(self, station: Station):
        if station.id in self.stations:
            raise ValueError("This identifier was already taken by another station")
        self.stations[station.id] = station

    '''
        Description: 
            Get the list of the id's of the stations that have spot availablen for the airline 
        Params: 
            - spotType: spot type (merchandise or commercial)
            - airlineID: identification of the airline
    '''
    def getStationsAvailable(self, spotType: SpotType, airlineID: str) -> List[Station]:
        spotsAvailable: List[Station] = []
        for station in self.stations:
            if self.stations[station].isSpotAvailable(spotType,airlineID):
                spotsAvailable.append(self.stations[station])
        return spotsAvailable
    
    '''
        Description: 
            Verify if some airline can buy <nSpots> of type <spotType>
        Params: 
            - nSpots: number of spots that the airline ID wants to buy
            - spotType: spot type (merchandise or commercial)
    '''
    def checkIfAirlineCanBuy(self,nSpots,spotType):
        spotsAvailable = 0
        for station in self.stations.values():
            spotsAvailable += station.getNumberOfSpotsAvailableByType(spotType)
        if spotsAvailable >= nSpots: return True 
        else: return False

    '''
        Description: 
            Fill <spots_merchandise> or <spots_commercial> Dict in the airlineID key 
            for each Station until the <nSpots> are totally bought
        Params: 
            - nSpots: number of spots that the airline ID wants to buy
            - spotType: spot type (merchandise or commercial)
            - airlineID: identification of the airline
        Details: 
            The airline will buy the spots in the first Station in the <self.stations>.
            If this Station does not have enough spots, the rest of the purchases 
            will be made at the next stations, and so on.
    '''
    def buySpots(self,nSpots,spotType,airlineID):
        spotsBoughtInStation = 0
        for station in self.stations.values():
            spotsBoughtInStation += station.buySpots(nSpots,spotType,airlineID)
            nSpots = nSpots - spotsBoughtInStation
            if nSpots == 0:
                return

    '''
        Description: 
            Update <spots_merchandise> or <spots_commercial> of station in case 
            the spot has become available or occupied
        Params: 
            - isAvailable: spot available (true) or occupied (false)
            - stationID: identification of the station
            - spotType: spot type (merchandise or commercial)
    '''      
    def updateStationSpots(self,isAvailable,stationID,spotType):
        if isAvailable:
            if spotType == SpotType.COMMERCIAL:
                self.stations[stationID].spots_commercial += 1
            else:
                self.stations[stationID].spots_merchandise += 1
        else:
            if spotType == SpotType.COMMERCIAL:
                self.stations[stationID].spots_commercial -= 1
            else:
                self.stations[stationID].spots_merchandise -= 1