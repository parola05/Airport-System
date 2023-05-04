from spade.behaviour import PeriodicBehaviour
from spade.message import Message

class EvaluateAirlinesProposalsBehaviour(PeriodicBehaviour):
    async def on_start(self):
        print("Starting Evaluate Airlines Proposals Behaviour . . .")

    async def run(self):
        proposalsByPrice = sorted(self.agent.airlinesProposals, key=lambda proposal: proposal["proposal"].price_per_spot)
        for proposal in proposalsByPrice:
            airlineCanBuy = self.agent.checkIfAirlineCanBuy(
                proposal["proposal"].n_spots,
                proposal["proposal"].spotType
            )
            #print("Airline can buy? " + str(airlineCanBuy))
            if airlineCanBuy:
                self.agent.buySpots(
                    proposal["proposal"].n_spots,
                    proposal["proposal"].spotType,
                    proposal["proposal"].airlineID,
                )

                msg = Message(to=str(proposal["agentID"]))
                msg.set_metadata("performative", "agree")
                msg.body = "Proposal of spots accepted. " + str(proposal["proposal"].n_spots) + " spots bought."
                await self.send(msg)
            else:
                msg = Message(to=str(proposal["agentID"]))
                msg.set_metadata("performative", "reject-proposal")
                msg.body = "Proposal of spots was not accepted. " + str(proposal["proposal"].n_spots) + " spots not available to buy."
                await self.send(msg)
        self.agent.airlinesProposals = []