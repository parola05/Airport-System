import sys, platform, datetime

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from GlobalTypes.Types import SpotType, Priority, RequestType
from GlobalTypes.Coord import Coord

class RequestFromAirplane():
    def __init__(self, id: str, typeRequest: RequestType, spotType: SpotType, airlineID: str, requestTime: datetime, priority: Priority, stationCoord: Coord, runwayCoord: Coord) -> None:
        '''
            typeRequest: levantar voo ou aterrar
            spotType: tipo da vaga requerida pelo avião (comercial ou mercadoria)
            airlineID: ID da companhia aérea do avião
            requestTime: hora em que o pedido foi feito e critério de desempate para avioes da mesma companhia com o mesmo nível de prioridade
            priority: grau de prioridade do avião
            stationCoord: coordenadas da gare para a concretização do pedido
            runwayCoord: coordenadas da pista mais próxima da gare para a concretização do pedido
        '''
        self.id: str = id
        self.typeRequest: RequestType = typeRequest
        self.spotType: SpotType = spotType 
        self.airlineID: str = airlineID 
        self.requestTime: datetime = requestTime 
        self.priority: Priority = priority
        self.stationCoord: Coord = stationCoord
        self.runwayCoord: Coord = runwayCoord