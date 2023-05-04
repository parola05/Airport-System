from .StationManager.StationManager import StationManagerAgent
from .Airline.Airline import AirlineAgent
import random

class Airport():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__ (
            self, 
            nStations = 3, 
            nMerchandiseSpotsPerStation = 10, 
            nCommercialSpotsPerStation = 10,
            nAirlines = 20,
            ) -> None:

        # INIT Stations
        self.stationManager:StationManagerAgent = StationManagerAgent(
            "station@laptop-vun6ls3v.lan",
            "12345678",
            nStations=nStations,
            nMerchandiseSpotsPerStation=nMerchandiseSpotsPerStation,
            nCommercialSpotsPerStation=nCommercialSpotsPerStation                                      
            )           

        # INIT Airlines
        self.airlines = []
        for i in range(0,nAirlines):
            airlineID = "Airline_" + str(i)
            airline = AirlineAgent(
                agent_name=airlineID+"@laptop-vun6ls3v.lan",
                password="12345678",
                airlineID=airlineID,
                n_spots=random.randint(1, 10),
                price_per_spot=random.randint(1000, 10000),
                spotType=random.randint(1,2)
                )
            self.airlines.append(airline)
            
        # INIT Airplanes
        # TODO

        # INIT Runways
        # TODO

        # INIT Control Tower
        # TODO

    def simulate(self):
        self.stationManager.start()
        for airline in self.airlines:
            airline.start()