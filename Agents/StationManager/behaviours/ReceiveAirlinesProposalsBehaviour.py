from spade.behaviour import CyclicBehaviour
from MessagesProtocol.BuySpots import BuySpots
import jsonpickle

class ReceiveAirlinesProposalsBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("Starting Receive Airline Proposal Behaviour . . .")

    async def run(self):
        msg = await self.receive(timeout=100) 
        if msg:
            buySpotMsg:BuySpots = jsonpickle.decode(msg.body)
            self.agent.airlinesProposals.append({
                "agentID":msg.sender,
                "proposal":buySpotMsg
            })
        