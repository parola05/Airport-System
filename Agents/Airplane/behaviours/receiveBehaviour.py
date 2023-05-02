import time
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Airplane.Airplane import AirplaneAgent
from GlobalTypes.Types import StatusType, RequestType

class ReceiveBehaviour(CyclicBehaviour):

    async def run(self):

        receiveMsg = await self.receive(timeout=60)

        sendMsg = Message(to=self.get("control_tower_jid"))

        if receiveMsg:
            performative = receiveMsg.get_metadata('performative')

            # Recebe informação de que a fila de espera está cheia ou quase cheia
            if performative == 'refuse':
                print("Agent {}".format(str(self.agent.jid)) + "is informed that queue in air is full")
                sendMsg.set_metadata("performative", "cancel")
                sendMsg.body = "Going to another airport"
                AirplaneAgent.status = StatusType.TO_ANOTHER_AIRPORT

            # Recebe indicação de que deve esperar (porque não existe gare ou pista disponível)
            elif performative == 'inform':
                print("Agent {}".format(str(self.agent.jid)) + "is waiting..")
                if "land" in receiveMsg.body:
                    AirplaneAgent.status = StatusType.WAITING_LAND
                else:
                    AirplaneAgent.status = StatusType.WAITING_TAKEOFF

            # Recebe informação da gare e da pista selecionadas para a aterragem ou a partida
            elif performative == 'confirm':
                """
                InfoForAirplaneAction:
                    requestType : LAND or TAKEOFF
                    stationCoord : Coord            # None se o tipo for 'LAND'
                    runwayCoord : Coord
                """
                #sendMsg.set_metadata("performative", "inform")
                if receiveMsg.body.requestType == RequestType.TAKEOFF:
                    #sendMsg.body = "Flying"
                    AirplaneAgent.status = StatusType.FLYING
                else:
                    #sendMsg.body = "Landing"
                    AirplaneAgent.status = StatusType.LANDING
                    time.sleep(30)
                    AirplaneAgent.status = StatusType.IN_STATION
                    #time.sleep(60)
                    #AirplaneAgent.status = StatusType.PARKED

        else:
            print("Agent {}".format(str(self.agent.jid)) + "did not receive any message after 1 minute")
            sendMsg.set_metadata("performative", "cancel")
            sendMsg.body = "Going to another airport"
            AirplaneAgent.status = StatusType.TO_ANOTHER_AIRPORT