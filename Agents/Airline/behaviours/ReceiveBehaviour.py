from spade.behaviour import CyclicBehaviour
import jsonpickle

class ReceiveBehaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1) 

        if msg:
            performative = msg.get_metadata('performative')
            if performative == 'agree':
                print("Proposta de compra de vagas aceite")
            elif performative == 'reject-proposal':
                print("Proposta de compra de vagas recusada")
        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")