from .StationManager.StationManager import StationManagerAgent
from .RunwayManager.RunwayManager import RunwayManagerAgent
from .Airline.Airline import AirlineAgent
from .Airplane.airplane import AirplaneAgent
from .ControlTower.ControlTower import ControlTower
import random, json, datetime
from Conf import Conf
import time

class Airport():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__(*args, **kwargs)
        return cls._instance
    
    def __init__ (
            self,
            nStations = 3, 
            nMerchandiseSpotsPerStation = 10, 
            nCommercialSpotsPerStation = 10,
            nAirlines = 5,
            nRunways = 5,
            nAirplanes = 10,
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
                spotType=random.randint(1,2)
            )
            self.airlines.append(airline)
        
        # INIT Airplanes
        self.airplanes = []
        for i in range(0, nAirplanes):
            airplaneID = "Airplane_" + str(i)
            airplane = AirplaneAgent(
                agent_name=airplaneID+"@" + Conf().get_openfire_server(),
                password=Conf().get_openfire_password(),
                airplaneID=airplaneID,
                airline=random.choice(airlinesID),
                origin=random.choice(self.cities),
                destination=random.choice(self.cities),
            )
            self.airplanes.append(airplane)

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
        future2 = self.controlTower.start()
        future2.result()
        future = self.stationManager.start()
        future.result()
        for airline in self.airlines:
            airline.start()
        for airplane in self.airplanes:
            airplane.start()
        self.runwayManager.start()