from spade.behaviour import CyclicBehaviour
from spade.message import Message

class ReceiveBehaviour(CyclicBehaviour):

    async def run(self):

        receiveMsg = await self.receive(timeout=60)

        sendMsg = Message(to=self.get("control_tower_jid"))

        if receiveMsg:
            performative = receiveMsg.get_metadata('performative')

            # Recebe informação de que a fila de espera está cheia ou quase cheia
            if performative == 'refuse':
                sendMsg.set_metadata("performative", "inform")
                sendMsg.body = "Going to another airport"

            # Recebe informação da gare e da pista selecionadas para a aterragem ou a partida
            elif performative == 'confirm':
                pass

        else:
            print("Agent {}".format(str(self.agent.jid)) + "did not receive any message after 1 minute")
            # Informa a Torre de Controlo que vai para outro aeroporto
            sendMsg.set_metadata("performative", "inform")
            sendMsg.body = "Going to another airport"