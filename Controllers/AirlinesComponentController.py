import sys
sys.path.append("..\..")
from Agents.Agents import Agents

class AirlinesComponentController():
    def __init__(self) -> None:
        '''
            Get Airlines from Agents Singleton
        '''
        self.airlines = Agents().airlines

    def getAirlines(self):
        return [
            {"id":"Indigo Airlines"},
            {"id":"Air India"},
            {"id":"AirAsia India"},
            {"id":"Vistara"},
            {"id":"SpiceJet"}
        ]