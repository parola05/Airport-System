from typing import Dict, List
from spade.behaviour import CyclicBehaviour
from spade.message import Message
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
from MessagesProtocol.DashboardControlTowerMessage import DashboardControlTowerMessage
from GlobalTypes.Types import RequestType, DashboardControlTowerMessageType, StatusType
import jsonpickle
from Conf import Conf


class ReceiveBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("[Control Tower] starting ReceiveBehaviour")

    def isQueueFull(self,queueInTheAir: Dict):
        amountWaiting = 0
        for airline in queueInTheAir:
            amountWaiting += len(airline[airline])
        return amountWaiting >= self.agent.queueInTheAirMaxSize

    async def run(self):

        receiveMsg = await self.receive()

        if receiveMsg:
            sender_name = receiveMsg.sender
            performative = receiveMsg.get_metadata('performative')

            if performative == 'request':
                requestFromAirplane:RequestFromAirplane = jsonpickle.decode(receiveMsg.body)

                # Recebe um pedido do avião para aterrar
                if requestFromAirplane.typeRequest == RequestType.LAND:
                    isFull = self.isQueueFull(self.agent.queueInTheAir)

                    if not isFull:
                        self.agent.requestsInProcess[sender_name] = receiveMsg.body

                        sendMsg = Message(to="station@" + Conf().get_openfire_server())
                        sendMsg.set_metadata("performative", "query-if")
                        sendMsg.body = "Are there any stations available?"

                    else:
                        sendMsg = Message(to=sender_name)
                        sendMsg.set_metadata("performative", "refuse")
                        sendMsg.body = "Go to another airport, the queue is full"

                        ############ Update Dashboard Control Tower ############
                        msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                        msg.set_metadata("performative", "inform")
                        bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                            type=DashboardControlTowerMessageType.AIRPLANE_REQUEST,
                            informStatus=StatusType.TO_ANOTHER_AIRPORT, 
                            requestText=str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " is going to another airport" 
                        )
                        msg.body = jsonpickle.encode(bodyMessage)
                        await self.send(msg)

                    ############### Update Dashboard Control Tower ###############
                    msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                    msg.set_metadata("performative", "inform")
                    bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                        type=DashboardControlTowerMessageType.AIRPLANE_REQUEST,
                        requestType=RequestType.LAND, 
                        requestText=str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " request to land" 
                    )
                    msg.body = jsonpickle.encode(bodyMessage)
                    await self.send(msg)

                # Recebe um pedido do avião para levantar voo
                elif requestFromAirplane.typeRequest == RequestType.TAKEOFF:
                    '''
                    self.agent.requestsInProcess[sender_name] = receiveMsg.body
                    
                    sendMsg = Message(to=self.get("runway_manager_jid"))
                    sendMsg.set_metadata("performative", "query-if")
                    sendMsg.body("Are there any runways available?")
                    '''
                    
                    ############### Update Dashboard ###############
                    msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                    msg.set_metadata("performative", "inform")
                    bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                        type=DashboardControlTowerMessageType.AIRPLANE_REQUEST,
                        requestType=RequestType.TAKEOFF, 
                        requestText=str(requestFromAirplane.id) + " request to take-off" 
                    )
                    msg.body = jsonpickle.encode(bodyMessage)
                    await self.send(msg)

            # Recebe informação de que o avião partiu para outro aeroporto
            elif performative == "cancel":
                '''
                if sender_name in self.agent.requestsInProcess:
                    del self.agent.requestsInProcess[sender_name]
                '''
            
            # Recebe a informação de que não existem gares ou pistas disponíveis
            elif performative == "refuse":
                '''
                airlineID = receiveMsg.body.airlineID
                self.agent.queueInTheAir[airlineID].append(receiveMsg.body)

                sendMsg = Message(to=sender_name)
                sendMsg.set_metadata("performative", "inform")
                sendMsg.body("Please, wait.")
                '''
                pass

            # Recebe a informação de que existem gares ou pistas disponíveis
            elif performative == "confirm":
                '''
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
                '''
                pass

            # Outras performativas
            # inform do airplane - realizou ação, ou foi para outro aeroporto
            else:
                pass

            # await self.send(sendMsg)