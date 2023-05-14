import sys, platform, datetime

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from GlobalTypes.Types import SpotType, Priority, RequestType, StatusType
from GlobalTypes.Coord import Coord

class RequestFromAirplane():
    def __init__(self, id: str, typeRequest: RequestType, spotType: SpotType, status: StatusType, airlineID: str, requestTime: datetime, priority: Priority, station=None, runway=None, haveRunway=False) -> None:
        '''
            typeRequest: levantar voo ou aterrar
            spotType: tipo da vaga requerida pelo avião (comercial ou mercadoria)
            airlineID: ID da companhia aérea do avião
            requestTime: hora em que o pedido foi feito e critério de desempate para avioes da mesma companhia com o mesmo nível de prioridade
            priority: grau de prioridade do avião
            station: gare mais próxima da pista para a concretização do pedido
            runway: pista para a concretização do pedido
        '''
        self.id: str = id
        self.typeRequest: RequestType = typeRequest
        self.spotType: SpotType = spotType
        self.status: StatusType = status 
        self.airlineID: str = airlineID
        self.requestTime: datetime = requestTime 
        self.priority: Priority = priority
        self.station = station # objecto Station
        self.runway = runway # objeto Runway
        self.haveRunway = haveRunway