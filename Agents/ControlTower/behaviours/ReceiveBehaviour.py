from typing import Dict, List
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import platform, sys, jsonpickle

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from MessagesProtocol.RequestFromAirplane import RequestFromAirplane
from MessagesProtocol.DashboardControlTowerMessage import DashboardControlTowerMessage
from MessagesProtocol.IsRunwayAvailable import IsRunwayAvailable
from MessagesProtocol.IsStationAvailable import IsStationAvailable
from GlobalTypes.Types import RequestType, DashboardControlTowerMessageType, StatusType
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
                        print("queue not full!")
                        self.agent.requestsInProcess[sender_name] = requestFromAirplane

                        sendMsg = Message(to="station@" + Conf().get_openfire_server())
                        sendMsg.set_metadata("performative", "query-if")
                        sendMsg.body = jsonpickle.encode(requestFromAirplane)
                        await self.send(sendMsg)

                    else:
                        print("queue full!")
                        sendMsg = Message(to=sender_name)
                        sendMsg.set_metadata("performative", "refuse")
                        sendMsg.body = "Go to another airport, the queue is full"
                        await self.send(sendMsg)

                    ############### Update Dashboard ###############
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
                    self.agent.requestsInProcess[sender_name] = requestFromAirplane

                    sendMsg = Message(to="runway@" + Conf().get_openfire_server())
                    sendMsg.set_metadata("performative", "query-if")
                    sendMsg.body = jsonpickle.encode(requestFromAirplane)
                    await self.send(sendMsg)
                    
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
                requestFromAirplane:RequestFromAirplane = jsonpickle.decode(receiveMsg.body)
                if sender_name in self.agent.requestsInProcess:
                    del self.agent.requestsInProcess[sender_name]

                ############ Update Dashboard ############
                msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                msg.set_metadata("performative", "inform")
                bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                    type=DashboardControlTowerMessageType.AIRPLANE_REQUEST,
                    informStatus=StatusType.TO_ANOTHER_AIRPORT, 
                    requestText=str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " is going to another airport" 
                )
                msg.body = jsonpickle.encode(bodyMessage)
                await self.send(msg)
                
            
            # Recebe a informação de que não existem gares ou pistas disponíveis
            elif performative == "refuse":
                requestFromAirplane:RequestFromAirplane = jsonpickle.decode(receiveMsg.body)

                airlineID = requestFromAirplane.airlineID
                if airlineID not in self.agent.queueInTheAir:
                    self.agent.queueInTheAir[airlineID] = [requestFromAirplane]
                else: self.agent.queueInTheAir[airlineID].append(requestFromAirplane)

                sendMsg = Message(to=str(requestFromAirplane.id) + "@" + Conf().get_openfire_server())
                sendMsg.set_metadata("performative", "inform")
                sendMsg.body = jsonpickle.encode(requestFromAirplane)
                await self.send(sendMsg)
                
                ############ Update Dashboard ############
                msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                msg.set_metadata("performative", "inform")
                if requestFromAirplane.typeRequest == RequestType.LAND:
                    requestText=str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " is waiting to land.." 
                else:
                    requestText=str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " is waiting to take off.." 
                bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                    type=DashboardControlTowerMessageType.AIRPLANE_IN_QUEUE,
                    requestType=requestFromAirplane.typeRequest,
                    requestText=requestText
                )
                msg.body = jsonpickle.encode(bodyMessage)
                await self.send(msg)

            # Recebe a informação de que existem gares ou pistas disponíveis
            elif performative == "confirm":
                receiveMsgDecoded:tuple = jsonpickle.decode(receiveMsg)
                airplane = receiveMsgDecoded[0]
                airplane_addr = airplane + "@" + Conf().get_openfire_server()
                airline = self.agent.requestsInProcess[airplane_addr].airlineID

                if "station@" in str(sender_name):
                    self.stationsAvailable = receiveMsgDecoded[1]
                    sendMsg = Message(to="runway@" + Conf().get_openfire_server())
                    sendMsg.set_metadata("performative", "query-if")
                    sendMsg.body = jsonpickle.encode(self.agent.requestsInProcess[airplane_addr])
                
                elif "runway@" in str(sender_name):
                    runwaysAvailable = receiveMsgDecoded[1]
                    # atualizar o objeto do pedido com as coordenadas da pista escolhida aleatoriamente
                    self.agent.requestsInProcess[airplane_addr].runway = runwaysAvailable[0]
                    
                    # se for para aterrar, calcular a gare mais perto da pista e atualizar o objeto do pedido com as suas coordenadas
                    if self.agent.requestsInProcess[airplane_addr].typeRequest == RequestType.LAND:
                        closestStation = self.agent.closestStationToRunway(runwaysAvailable[0].coord, self.stationsAvailable)
                        self.agent.requestsInProcess[airplane_addr].station = closestStation
                        # reservar um spot da station (será ocupada)
                        sendMsg = Message(to="station@" + Conf().get_openfire_server())
                        sendMsg.set_metadata("performative", "inform-ref")
                        stationAvailabilityInfo = IsStationAvailable(
                                                    isAvailable=False,
                                                    stationInfo=closestStation,
                                                    airline=requestFromAirplane.airlineID,
                                                    spotType=self.agent.requestsInProcess[airplane_addr].spotType
                                                  )
                        sendMsg.body = jsonpickle.encode(stationAvailabilityInfo)
                        await self.send(sendMsg)

                    # reservar a pista (será ocupada)
                    sendMsg = Message(to="runway@" + Conf().get_openfire_server())
                    sendMsg.set_metadata("performative", "inform-ref")
                    runwayAvailabilityInfo = IsRunwayAvailable(
                                                isAvailable=False,
                                                runwayInfo=runwaysAvailable[0]
                                             )
                    sendMsg.body = jsonpickle.encode(runwayAvailabilityInfo)
                    await self.send(sendMsg)
                    
                    # remove o avião da fila de espera (caso ele esteja na fila de espera)
                    self.agent.removeAirplaneFromQueue(airline,airplane)

                    sendMsg = Message(to=airplane_addr)
                    sendMsg.set_metadata("performative", "agree")
                    sendMsg.body = jsonpickle.encode(self.agent.requestsInProcess[airplane_addr])

            # Recebe informação do avião após ser permitido a sua aterragem ou partida
            elif performative == 'inform':
                requestFromAirplane = self.agent.requestsInProcess[sender_name]

                if sender_name in self.agent.requestsInProcess:
                    del self.agent.requestsInProcess[sender_name]

                ########### UPDATE DASHBOARD ###########
                msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                msg.set_metadata("performative", "inform")

                # tanto a pista, como a gare já foram reservadas na performativa "confirm"
                if requestFromAirplane.status == StatusType.LANDING:
                    informStatus = StatusType.LANDING
                    requestText = str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " is landing in runway " + str(requestFromAirplane.runway.coord)

                # a pista fica livre quando o avião estaciona, mas a station permanece ocupada
                elif requestFromAirplane.status == StatusType.IN_STATION:
                    informStatus = StatusType.LANDING
                    requestText = str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " is parked in station " + str(requestFromAirplane.station.coord)

                    sendMsg = Message(to="runway@" + Conf().get_openfire_server())
                    sendMsg.set_metadata("performative", "inform-ref")
                    runwayAvailabilityInfo = IsRunwayAvailable(
                                                isAvailable=True,
                                                runwayInfo=requestFromAirplane.runway
                                             )
                    sendMsg.body = jsonpickle.encode(runwayAvailabilityInfo)
                    await self.send(sendMsg)
                
                # a pista já foi reservada na performativa "confirm", mas a station fica livre
                elif requestFromAirplane.status == StatusType.TAKING_OFF:
                    informStatus = StatusType.TAKING_OFF
                    requestText = str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " is taking off in runway " + str(requestFromAirplane.runway.coord)
                    sendMsg = Message(to="station@" + Conf().get_openfire_server())
                    sendMsg.set_metadata("performative", "inform-ref")
                    stationAvailabilityInfo = IsStationAvailable(
                                                isAvailable=True,
                                                stationInfo=requestFromAirplane.station,
                                                spotType=requestFromAirplane.spotType
                                            )
                    sendMsg.body = jsonpickle.encode(stationAvailabilityInfo)
                    await self.send(sendMsg)

                # a pista fica livre
                elif requestFromAirplane.status == StatusType.FLYING:
                    informStatus = StatusType.LANDING
                    requestText = str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " is flying"
                    
                    sendMsg = Message(to="runway@" + Conf().get_openfire_server())
                    sendMsg.set_metadata("performative", "inform-ref")
                    runwayAvailabilityInfo = IsRunwayAvailable(
                                                isAvailable=True,
                                                runwayInfo=requestFromAirplane.runway
                                             )
                    sendMsg.body = jsonpickle.encode(runwayAvailabilityInfo)
                    await self.send(sendMsg)

                bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                    type=DashboardControlTowerMessageType.AIRPLANE_REQUEST,
                    informStatus=informStatus,
                    requestText=requestText
                )
                msg.body = jsonpickle.encode(bodyMessage)
                await self.send(msg)