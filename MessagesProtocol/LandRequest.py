import sys
import platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from GlobalTypes.Types import SpotType, Priority
from datetime import date

class LandRequest():
    def __init__(self, spotType:SpotType, airlineID: str, requestTime: date, airplaneID: str, priority: Priority) -> None:
        '''
            spotType: tipo da vaga requerida pelo avião (comercial ou mercadoria)
            airlineID: ID da companhia aérea do avião
            requestTime: hora que o avião pediu a aterragem. Critério de desempate para avioes da mesma companhia com o 
            mesmo nível de prioridade
            airplaneID: ID do avião
        '''
        self.spotType: SpotType = spotType 
        self.airlineID: str = airlineID 
        self.requestTime: date = requestTime 
        self.airplaneID:str = airplaneID
        self.priority: Priority = priority