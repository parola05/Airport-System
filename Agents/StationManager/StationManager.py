from spade import Agent
from typing import Dict, List
import sys 
sys.path.append("..")
from GlobalTypes import Coord, SpotType

class Station():
    def __init__(self,id:str,coord:Coord,vagas_mercadoria:int,vagas_transporte:int) -> None:
        '''
            id: identificador único do Gare
            coord: localização do Gare
            n_vagas_mercadoria: Número de vagas disponíveis para aviões de mercadoria
            n_vagas_transporte: Número de vagas disponíveis para aviões de transporte
            vagas_mercadoria: Dicionário que mapeia o id de uma companhia aérea para o objeto {vagas compradas, vagas disponiveis} para vagas do tipo de avião de mercadoria
            vagas_comercial: Dicionário que mapeia o id de uma companhia aérea para o objeto {vagas compradas, vagas disponiveis} para vagas do tipo de avião comercial
        '''
        self.id:str = id
        self.coord:Coord = coord
        self.spots_available_merchandise:int = vagas_mercadoria
        self.spots_available_transport:int = vagas_transporte
        self.spots_merchandise:Dict[str,Dict[str,str]] = {}
        self.spots_commercial:Dict[str,Dict[str,str]] = {}

    def isSpotAvailable(self,spotType:SpotType,airline_name:str):
        if spotType == SpotType.MERCHANDISE:
            if self.spots_merchandise[airline_name]["vagas_disponiveis"] > 0:return True
            else: return False
        elif spotType == SpotType.COMMERICIAL:
            if self.spots_commercial[airline_name]["vagas_disponiveis"] > 0:return True
            else: return False
        
class StationManagerAgent(Agent):
    async def setup(self):
        self.stations: Dict[str,Station] = {}

    def addStation(self,station:Station):
        if station.id in self.stations:
            raise ValueError("Identificador já utilizado para o Gare")
        self.stations[station.id] = station

    def getStationsAvailable(self,spotType:SpotType,airline_name:str):
        '''
            return: list of the id's of the stations that have spot availablen for the airline 
        '''
        spotsAvailable: List[str] = []
        for station in self.stations:
            if station.isSpotAvailable(spotType,airline_name):
                spotsAvailable.append(station.id)
        return spotsAvailable