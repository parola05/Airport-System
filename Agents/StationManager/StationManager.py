from spade import Agent
from typing import Dict, List
import sys
sys.path.append("..")
from GlobalTypes import Coord
from GlobalTypes.Types import SpotType

class Station():
    def __init__(self, id: str, coord: Coord, merchandise_spots: int, transport_spots: int) -> None:
        '''
            id: identificador único do gare
            coord: localização do gare
            spots_available_merchandise: número de vagas disponíveis para aviões de mercadoria
            spots_available_transport: número de vagas disponíveis para aviões de transporte
            spots_merchandise: dicionário que mapeia o id de uma companhia aérea para o objeto {vagas compradas, vagas disponiveis} para vagas do tipo de avião de mercadoria
            spots_commercial: dicionário que mapeia o id de uma companhia aérea para o objeto {vagas compradas, vagas disponiveis} para vagas do tipo de avião comercial
        '''
        self.id: str = id
        self.coord: Coord = coord
        self.spots_available_merchandise: int = merchandise_spots
        self.spots_available_transport: int = transport_spots
        self.spots_merchandise: Dict[str, Dict[str,str]] = {}
        self.spots_commercial: Dict[str, Dict[str,str]] = {}

    def isSpotAvailable(self, spotType: SpotType, airline_name: str):
        if spotType == SpotType.MERCHANDISE:
            if self.spots_merchandise[airline_name]["spots_available"] > 0: return True
            else: return False
        elif spotType == SpotType.COMMERCIAL:
            if self.spots_commercial[airline_name]["spots_available"] > 0: return True
            else: return False
        
class StationManagerAgent(Agent):
    async def setup(self):
        self.stations: Dict[str,Station] = {}

    def addStation(self, station: Station):
        if station.id in self.stations:
            raise ValueError("This identifier was already taken by another station")
        self.stations[station.id] = station

    def getStationsAvailable(self, spotType: SpotType, airline_name: str):
        '''
            return: list of the id's of the stations that have spot availablen for the airline 
        '''
        spotsAvailable: List[str] = []
        for station in self.stations:
            if station.isSpotAvailable(spotType,airline_name):
                spotsAvailable.append(station.id)
        return spotsAvailable