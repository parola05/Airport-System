import sys
import platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from GlobalTypes.Types import SpotType, Priority, RequestType
import datetime

class RequestFromAirplane():
    def __init__(self, typeRequest: RequestType, spotType: SpotType, airlineID: str, requestTime: datetime, airplaneID: str, priority: Priority) -> None:
        '''
            typeRequest: levantar voo ou aterrar
            spotType: tipo da vaga requerida pelo avião (comercial ou mercadoria)
            airlineID: ID da companhia aérea do avião
            requestTime: hora que o avião pediu a aterragem. Critério de desempate para avioes da mesma companhia com o 
            mesmo nível de prioridade
            airplaneID: ID do avião
        '''
        self.typeRequest: RequestType = typeRequest
        self.spotType: SpotType = spotType 
        self.airlineID: str = airlineID 
        self.requestTime: datetime = requestTime 
        self.airplaneID:str = airplaneID
        self.priority: Priority = priority