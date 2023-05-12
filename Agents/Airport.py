from .StationManager.StationManager import StationManagerAgent
from .RunwayManager.RunwayManager import RunwayManagerAgent
from .Airline.Airline import AirlineAgent
from .Airplane.airplane import AirplaneAgent
from .ControlTower.ControlTower import ControlTower
import random, json, datetime
from Conf import Conf
import time
from GlobalTypes.Types import StatusType, SpotType

class Airport():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__(*args, **kwargs)
        return cls._instance
    
    def __init__ (
            self,
            nStations = 1, 
            nMerchandiseSpotsPerStation = 20, 
            nCommercialSpotsPerStation = 20,
            nAirlines = 1,
            nRunways = 1,
            nAirplanesToLand = 2,
            nAirplanesToTakeOff = 2,
            queueInTheAirMaxSize = 30,
        ) -> None:

        with open('cities.json') as f:
            self.cities = json.load(f)['cities']

        # INIT Stations
        self.stationManager:StationManagerAgent = StationManagerAgent(
            "station@" + Conf().get_openfire_server(),
            Conf().get_openfire_password(),
            nStations=nStations,
            nMerchandiseSpotsPerStation=nMerchandiseSpotsPerStation,
            nCommercialSpotsPerStation=nCommercialSpotsPerStation                                      
        )           

        # INIT Airlines
        self.airlines = []
        self.airlinesMap = {} # for simulation purpose
        airlinesID = [] 
        for i in range(0,nAirlines):
            airlineID = "Airline_" + str(i)
            airlinesID.append(airlineID)
            airline = AirlineAgent(
                agent_name=airlineID+"@" + Conf().get_openfire_server(),
                password=Conf().get_openfire_password(),
                airlineID=airlineID,
                n_spots=random.randint(1, 10),
                price_per_spot=random.randint(1000, 10000),
                spotType=random.randint(1,2),
                nSpotsCommercialStart=0,
                nSpotsMerchandiseStart=0
            )
            self.airlines.append(airline)
            self.airlinesMap[airlineID] = airline
        
        # INIT Airplanes to Land
        self.airplanesToLand = []
        for i in range(0, nAirplanesToLand):
            airplaneID = "lAirplane_" + str(i)
            airplane = AirplaneAgent(
                agent_name=airplaneID+"@" + Conf().get_openfire_server(),
                password=Conf().get_openfire_password(),
                airplaneID=airplaneID,
                airline=random.choice(airlinesID),
                origin=random.choice(self.cities),
                destination=random.choice(self.cities),
                status=StatusType.FLYING
            )
            self.airplanesToLand.append(airplane)
        
        # INIT Airplanes to Take-off
        self.airplanesToTakeOff = []
        for i in range(0, nAirplanesToTakeOff):

            # get random value for transport type
            typeTransport = self.getRandomTypeTransport()

            # get random value for the airlineID
            airlineID = random.choice(airlinesID)
            
            # Update values in the stations for the airline that need
            # more one spot for the airplane.
            # The return value is the [Station] where the airplane will be
            stations = self.stationManager.buySpots(
                nSpots=1,
                airlineID=airlineID,
                spotType=typeTransport
            )

            # Increment number of spots of the airline selected
            if typeTransport == SpotType.COMMERCIAL:
                self.airlinesMap[airlineID].nSpotsCommercialStart += 1
            elif typeTransport == SpotType.MERCHANDISE:
                self.airlinesMap[airlineID].nSpotsMerchandiseStart += 1
            
            # Create Airplane Agent
            airplaneID = "tAirplane_" + str(i)
            airplane = AirplaneAgent(
                agent_name=airplaneID+"@" + Conf().get_openfire_server(),
                password=Conf().get_openfire_password(),
                airplaneID=airplaneID,
                airline=airlineID,
                origin=random.choice(self.cities),
                destination=random.choice(self.cities),
                status=StatusType.IN_STATION,
                typeTransport=typeTransport,
                stationPark=stations[0]
            )
            self.airplanesToTakeOff.append(airplane)

        # INIT Runways
        self.runwayManager:RunwayManagerAgent = RunwayManagerAgent(
            "runway@" + Conf().get_openfire_server(),
            Conf().get_openfire_password(),
            nRunways=nRunways                                     
        )    

        # INIT Control Tower
        self.controlTower:ControlTower = ControlTower(
            "controlTower@" + Conf().get_openfire_server(),
            Conf().get_openfire_password(),
            queueInTheAirMaxSize=queueInTheAirMaxSize
        )


    def simulate(self):

        future = self.controlTower.start()
        future.result()
        future2 = self.stationManager.start()
        future2.result()
        self.runwayManager.start()

        for airline in self.airlines:
            airline.start()

        for airplane in self.airplanesToLand:
            airplane.start()

        for airplane in self.airplanesToTakeOff:
            airplane.start()
            
    def getRandomTypeTransport(self):
        randomChoice = random.randint(0,9)
        if randomChoice % 2 == 0:
            return SpotType.COMMERCIAL
        else:
            return SpotType.MERCHANDISE