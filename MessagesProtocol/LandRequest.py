import sys
sys.path.append("..\\..")
from GlobalTypes import SpotType
from GlobalTypes.Types import SpotType
from datetime import date

class LandRequest():
    def __init__(self, spotType:SpotType, airlineID: str, requestTime: date, airplaneID: str) -> None:
        '''
            requestTime :hora que o avião pediu a aterragem. Critério de desempate para avioes da mesma companhia com o 
            mesmo nível de prioridade
        '''
        self.spotType: SpotType = spotType 
        self.airlineID: str = airlineID 
        self.requestTime: date = requestTime 
        self.airplaneID:str = airplaneID