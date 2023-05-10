import time, jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Airplane.Airplane import AirplaneAgent
from GlobalTypes.Types import StatusType, RequestType
from MessagesProtocol.RequestFromAirplane import RequestFromAirplane
from Conf import Conf
class ReceiveBehaviour(CyclicBehaviour):

    async def run(self):

        receiveMsg = await self.receive(timeout=60)

        sendMsg = Message(to="controlTower@" + Conf().get_openfire_server())

        if receiveMsg:
            performative = receiveMsg.get_metadata('performative')

            # Recebe informação de que a fila de espera está cheia ou quase cheia
            if performative == 'refuse':
                print("Agent {}".format(str(self.agent.jid)) + "is informed that queue in air is full")
                sendMsg.set_metadata("performative", "cancel")
                sendMsg.body = "Going to another airport"

            # Recebe indicação de que deve esperar (porque não existe gare ou pista disponível)
            elif performative == 'inform':
                print("Agent {}".format(str(self.agent.jid)) + "is waiting..")
                requestFromAirplane:RequestFromAirplane = jsonpickle.decode(receiveMsg.body)
                if requestFromAirplane.typeRequest == RequestType.LAND:
                    self.agent.status = StatusType.WAITING_LAND
                else:
                    self.agent.status = StatusType.WAITING_TAKEOFF

            # Recebe informação da gare e da pista selecionadas para a aterragem ou a partida
            elif performative == 'confirm':
                requestFromAirplane:RequestFromAirplane = jsonpickle.decode(receiveMsg.body)
                if requestFromAirplane.requestType == RequestType.TAKEOFF:
                    self.agent.status = StatusType.TAKING_OFF
                    time.sleep(10)
                    self.agent.status = StatusType.FLYING
                else:
                    self.agent.status = StatusType.LANDING
                    time.sleep(10)
                    self.agent.status = StatusType.IN_STATION
                sendMsg.set_metadata("performative", "inform")
                sendMsg.body = "Action required completed!"

        else:
            print("Agent {}".format(str(self.agent.jid)) + "did not receive any message after 1 minute")
            self.agent.status = StatusType.TO_ANOTHER_AIRPORT
            sendMsg.set_metadata("performative", "cancel")
            sendMsg.body = "Going to another airport"

        await self.send(sendMsg)