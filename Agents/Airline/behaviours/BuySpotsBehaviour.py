from spade.behaviour import OneShotBehaviour
from MessagesProtocol.BuySpots import BuySpots
from MessagesProtocol.DashboardAirlines import DashboardAirlines
from GlobalTypes.Types import DashboardAirlineUpdate
from spade.message import Message
import jsonpickle

class BuySpotsBehaviour(OneShotBehaviour):
    async def on_start(self):
        print("Starting Buy Spot Behaviour Behaviour . . .")

    async def run(self):
        ############### Send proposal ###################
        msg = Message(to="station@laptop-vun6ls3v.lan")
        msg.set_metadata("performative", "propose")
        bodyMessage:BuySpots = BuySpots(
            self.agent.n_spots,
            self.agent.price_per_spot,
            self.agent.spotType, 
            self.agent.airlineID
        ) 
        msg.body = jsonpickle.encode(bodyMessage)
        await self.send(msg)

        ############### Update Dashboard ###############
        msg = Message(to="dashboardAirline@laptop-vun6ls3v.lan")
        msg.set_metadata("performative", "inform")
        bodyMessage:DashboardAirlines = DashboardAirlines(
            type=DashboardAirlineUpdate.NEGOTIATION,
            negotiationText=self.agent.airlineID + " proposal " + str(self.agent.price_per_spot) + " for " + str(self.agent.n_spots) + " spots" 
        )
        msg.body = jsonpickle.encode(bodyMessage)
        await self.send(msg)