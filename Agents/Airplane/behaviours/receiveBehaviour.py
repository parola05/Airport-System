import time, jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from GlobalTypes.Types import StatusType, RequestType
from MessagesProtocol.RequestFromAirplane import RequestFromAirplane
from MessagesProtocol.DashboardAirplaneMessage import DashboardAirplaneMessage, AirplaneInfo
from GlobalTypes.Types import DashboardAirplaneMessageType
from Conf import Conf
import asyncio

class ReceiveBehaviour(CyclicBehaviour):

    async def on_start(self):
        print("[Airplane] starting ReceiveBehaviour")

    async def run(self):

        receiveMsg = await self.receive(timeout=60)

        sendMsg = Message(to="controlTower@" + Conf().get_openfire_server())

        if receiveMsg:
            performative = receiveMsg.get_metadata("performative")

            # Recebe informação de que a fila de espera está cheia ou quase cheia
            if performative == "refuse":
                print("Agent {}".format(str(self.agent.jid)) + " is informed that queue in air is full")
                self.agent.status = StatusType.TO_ANOTHER_AIRPORT
                sendMsg.set_metadata("performative", "cancel")
                sendMsg.body = "Going to another airport"
                await self.send(sendMsg)

            # Recebe indicação de que deve esperar (porque não existe gare ou pista disponível)
            elif performative == "inform":
                # print("Agent {}".format(str(self.agent.jid)) + " is waiting..")
                requestFromAirplane:RequestFromAirplane = jsonpickle.decode(receiveMsg.body)
                if requestFromAirplane.typeRequest == RequestType.LAND:
                    self.agent.status = StatusType.WAITING_LAND
                else:
                    self.agent.status = StatusType.WAITING_TAKEOFF

            # Recebe informação da gare e da pista selecionadas para a aterragem ou a partida
            elif performative == "agree":
                requestFromAirplane:RequestFromAirplane = jsonpickle.decode(receiveMsg.body)

                if requestFromAirplane.typeRequest == RequestType.TAKEOFF:

                    self.agent.status = StatusType.TAKING_OFF
                    requestFromAirplane.status = self.agent.status
                    sendMsg.set_metadata("performative", "inform")
                    sendMsg.body = jsonpickle.encode(requestFromAirplane)
                    await self.send(sendMsg)

                    ############ Update Dashboard with TAKING OFF STATE############
                    msg = Message(to="dashboardAirplane@" + Conf().get_openfire_server())
                    msg.set_metadata("performative", "inform")
                    bodyMessage:DashboardAirplaneMessage = DashboardAirplaneMessage(
                        type=DashboardAirplaneMessageType.UPDATE,
                        airplaneInfo=AirplaneInfo(
                            id=self.agent.airplaneID,
                            status=self.agent.status,
                            airlineID=self.agent.airline,
                        )
                    )
                    msg.body = jsonpickle.encode(bodyMessage)
                    await self.send(msg)

                    await asyncio.sleep(15)

                    self.agent.status = StatusType.FLYING
                    requestFromAirplane.status = self.agent.status
                    sendMsg.set_metadata("performative", "inform")
                    sendMsg.body = jsonpickle.encode(requestFromAirplane)
                    await self.send(sendMsg)

                    self.kill(exit_code=10)

                else:
                    self.agent.stationPark = requestFromAirplane.station
                    self.agent.status = StatusType.LANDING
                    requestFromAirplane.status = self.agent.status
                    sendMsg.set_metadata("performative", "inform")
                    sendMsg.body = jsonpickle.encode(requestFromAirplane)
                    await self.send(sendMsg)

                    ############ Update Dashboard WITH LANDING STATE ############
                    msg = Message(to="dashboardAirplane@" + Conf().get_openfire_server())
                    msg.set_metadata("performative", "inform")
                    bodyMessage:DashboardAirplaneMessage = DashboardAirplaneMessage(
                        type=DashboardAirplaneMessageType.UPDATE,
                        airplaneInfo=AirplaneInfo(
                            id=self.agent.airplaneID,
                            status=self.agent.status,
                            airlineID=self.agent.airline,
                        )
                    )
                    msg.body = jsonpickle.encode(bodyMessage)
                    await self.send(msg)

                    await asyncio.sleep(15)
                    
                    self.agent.status = StatusType.IN_STATION
                    requestFromAirplane.status = self.agent.status
                    sendMsg.set_metadata("performative", "inform")
                    sendMsg.body = jsonpickle.encode(requestFromAirplane)
                    await self.send(sendMsg)

                    self.kill(exit_code=10)
                    
        else:
            print("Agent {}".format(str(self.agent.jid)) + " did not receive any message after 1 minute")
            self.agent.status = StatusType.TO_ANOTHER_AIRPORT
            sendMsg.set_metadata("performative", "cancel")
            sendMsg.body = "Going to another airport"

        ############ Update Dashboard ############
        msg = Message(to="dashboardAirplane@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "inform")
        bodyMessage:DashboardAirplaneMessage = DashboardAirplaneMessage(
            type=DashboardAirplaneMessageType.UPDATE,
            airplaneInfo=AirplaneInfo(
                id=self.agent.airplaneID,
                status=self.agent.status,
                airlineID=self.agent.airline,
            )
        )
        msg.body = jsonpickle.encode(bodyMessage)
        await self.send(msg)