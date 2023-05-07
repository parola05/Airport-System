from .StationManager.StationManager import StationManagerAgent
from .RunwayManager.RunwayManager import RunwayManagerAgent
from .Airline.Airline import AirlineAgent
import random, json, datetime
from Conf import Conf

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
            nAirlines = 20,
            nRunways = 10,
            nAirplanes = 1,
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
        print("server:",Conf().get_openfire_server())
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
            airplane = AirlineAgent(
                agent_name=airplaneID+"@" + Conf().get_openfire_server(),
                password=Conf().get_openfire_password(),
                airline=random.choice(airlinesID),
                typeTransport = None,
                origin = None,
                destination = None,
                date = None,
                time = None,
                status = None,
                priority = None
            )
            airplane.typeTransport = airplane.getRandomTypeTransport()
            airplane.origin = airplane.getRandomOrigin(self.cities)
            airplane.destiny = airplane.getRandomDestiny(self.cities, airplane.origin)
            airplane.datetime = datetime.datetime.now()
            airplane.priority = airplane.getRandomPriority()

            self.airplanes.append(airplane)

        # INIT Runways
        self.runwayManager:RunwayManagerAgent = RunwayManagerAgent(
            "runway@" + Conf().get_openfire_server(),
            Conf().get_openfire_password(),
            nRunways=nRunways                                     
        )    

        # INIT Control Tower
        # TODO

    def simulate(self):
        future = self.stationManager.start()
        future.result()
        for airline in self.airlines:
            airline.start()