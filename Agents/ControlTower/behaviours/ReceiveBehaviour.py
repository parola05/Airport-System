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

        sender_name, _ = receiveMsg.sender

        if receiveMsg:
            performative = receiveMsg.get_metadata('performative')

            if performative == 'request':
                requestType = receiveMsg.body.requestType

                # Recebe um pedido do avião para aterrar
                if requestType == RequestType.LAND:
                    isFull = self.isQueueFull(self.agent.queueInTheAir)

                    if not isFull:
                        self.agent.requestsInProcess[sender_name] = receiveMsg.body

                        sendMsg = Message(to="station_manager_jid")
                        sendMsg.set_metadata("performative", "query-if")
                        sendMsg.body("Are there any stations available?")

                    else:
                        sendMsg = Message(to=sender_name)
                        sendMsg.set_metadata("performative", "refuse")
                        sendMsg.body("Go to another airport, the queue is full.")

                # Recebe um pedido do avião para levantar voo
                elif requestType == RequestType.TAKEOFF:
                    self.agent.requestsInProcess[sender_name] = receiveMsg.body
                    
                    sendMsg = Message(to=self.get("runway_manager_jid"))
                    sendMsg.set_metadata("performative", "query-if")
                    sendMsg.body("Are there any runways available?")

            # Recebe informação de que o avião partiu para outro aeroporto
            elif performative == "cancel":
                if sender_name in self.agent.requestsInProcess:
                    del self.agent.requestsInProcess[sender_name]
            
            # Recebe a informação de que não existem gares ou pistas disponíveis
            elif performative == "refuse":
                airlineID = receiveMsg.body.airlineID
                self.agent.queueInTheAir[airlineID].append(receiveMsg.body)

                sendMsg = Message(to=sender_name)
                sendMsg.set_metadata("performative", "inform")
                sendMsg.body("Please, wait.")

            # Recebe a informação de que existem gares ou pistas disponíveis
            elif performative == "confirm":

                if isinstance(receiveMsg.body, StationAvailable):
                    self.agent.requestsInProcess[sender_name].stationCoord = receiveMsg.body.coord

                    sendMsg = Message(to="runway_manager_jid")
                    sendMsg.set_metadata("performative", "query-if")
                    sendMsg.body("Are there any runways available?")
                
                elif isinstance(receiveMsg.body, RunwayAvailable):
                    self.agent.requestsInProcess[sender_name].runwayCoord = receiveMsg.body.coord

                    sendMsg = Message(to=sender_name)
                    sendMsg.set_metadata("performative", "confirm")
                    sendMsg.body = self.agent.requestsInProcess[sender_name]

                    del self.agent.requestsInProcess[sender_name]

            # Outras performativas
            # inform do airplane - realizou ação, ou foi para outro aeroporto
            else:
                pass

            await self.send(sendMsg)
        