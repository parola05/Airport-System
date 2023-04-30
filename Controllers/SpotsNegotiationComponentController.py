import sys
sys.path.append("..\..")
from Agents.Agents import Agents

class SpotsNegotiationComponentController():
    def __init__(self) -> None:
        '''
            Get Stations from Agents Singleton
        '''
        self.stationManager = Agents().stationManager