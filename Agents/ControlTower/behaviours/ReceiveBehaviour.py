from typing import Dict, List
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from ControlTower.ControlTower import ControlTower
import platform, sys

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from MessagesProtocol.StationAvailable import StationAvailable
from MessagesProtocol.RequestFromAirplane import RequestFromAirplane
from MessagesProtocol.RunwayAvailable import RunwayAvailable
from GlobalTypes.Types import RequestType


class ReceiveBehaviour(CyclicBehaviour):

    def isQueueFull(queueInTheAir: Dict):
        amountWaiting = 0
        for airline in queueInTheAir:
            amountWaiting += len(airline[airline])
        return amountWaiting >= 30

    async def run(self):

        receiveMsg = await self.receive()

        # sender_name, sender_address
        sender_name, _ = receiveMsg.sender

        if receiveMsg:
            performative = receiveMsg.get_metadata('performative')

            """
            >>> PEDIDOS DOS AVIÕES <<<
            """
            if performative == 'request':
                requestType = receiveMsg.body.requestType

                # Recebe um pedido do avião para aterrar
                if requestType == RequestType.LAND:
                    isFull = self.isQueueFull(ControlTower.queueInTheAir)

                    if not isFull:
                        ControlTower.requestsInProcess[sender_name] = receiveMsg.body

                        checkStationsAvailable = Message(to="station_manager_jid")
                        checkStationsAvailable.set_metadata("performative", "query-if")
                        checkStationsAvailable.body("Are there any stations available?")

                        await self.send(checkStationsAvailable)
                    
                    else:
                        refuseRequestFromAirplane = Message(to=sender_name)
                        refuseRequestFromAirplane.set_metadata("performative", "refuse")
                        refuseRequestFromAirplane.body("Go to another airport, the queue is full.")

                        await self.send(checkStationsAvailable)

                # Recebe um pedido do avião para levantar voo
                elif requestType == RequestType.TAKEOFF:
                    ControlTower.requestsInProcess[sender_name] = receiveMsg.body
                    
                    checkRunwaysAvailable = Message(to=self.get("runway_manager_jid"))
                    checkRunwaysAvailable.set_metadata("performative", "query-if")
                    checkRunwaysAvailable.body("Are there any runways available?")

                    await self.send(checkRunwaysAvailable)

            # Recebe a informação de que não existem gares ou pistas disponíveis
            elif performative == "refuse":
                airlineID = receiveMsg.body.airlineID
                ControlTower.queueInTheAir[airlineID].append(receiveMsg.body)

                informAirplaneToWait = Message(to=sender_name)
                informAirplaneToWait.set_metadata("performative", "inform")
                informAirplaneToWait.body("Please, wait.")

            # Recebe a informação de que existem gares ou pistas disponíveis
            elif performative == "confirm":

                if isinstance(receiveMsg.body, StationAvailable):
                    ControlTower.requestsInProcess[sender_name].stationCoord = receiveMsg.body.coord

                    checkRunwaysAvailable = Message(to="runway_manager_jid")
                    checkRunwaysAvailable.set_metadata("performative", "query-if")
                    checkRunwaysAvailable.body("Are there any runways available?")

                    await self.send(checkRunwaysAvailable)
                
                elif isinstance(receiveMsg.body, RunwayAvailable):
                    ControlTower.requestsInProcess[sender_name].runwayCoord = receiveMsg.body.coord

                    confirmAirplane = Message(to=sender_name)
                    confirmAirplane.set_metadata("performative", "confirm")
                    confirmAirplane.body = ControlTower.requestsInProcess[sender_name]

                    await self.send(confirmAirplane)

            # Outras performativas
            # inform do airplane - realizou ação, ou foi para outro aeroporto
            else:
                pass