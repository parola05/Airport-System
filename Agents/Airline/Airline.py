from spade.agent import Agent
from .behaviours.BuySpotsBehaviour import BuySpotsBehaviour
from .behaviours.ReceiveProposalAnswerBehaviour import ReceiveProposalAnswerBehaviour
from .behaviours.InformDashboardInitStateBehaviour import InformDashBoardInitStateBehaviour

class AirlineAgent(Agent):
    async def setup(self):
        receiveSpotsQueryBehaviour = ReceiveProposalAnswerBehaviour()
        buySpotsBehaviour = BuySpotsBehaviour()
        informDashBoardInitStateBehaviour = InformDashBoardInitStateBehaviour()

        self.add_behaviour(receiveSpotsQueryBehaviour)
        self.add_behaviour(buySpotsBehaviour)
        self.add_behaviour(informDashBoardInitStateBehaviour)

    def __init__(self,agent_name,password,airlineID,n_spots=None,price_per_spot=None,spotType=None) -> None:
        super().__init__(agent_name,password)
        self.airlineID = airlineID
        self.n_spots: int = n_spots
        self.price_per_spot: float = price_per_spot
        self.spotType = spotType 