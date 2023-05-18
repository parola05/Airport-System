from spade.behaviour import OneShotBehaviour
from MessagesProtocol.BuySpots import BuySpots
from MessagesProtocol.DashboardAirlinesMessage import DashboardAirlinesMessage
from GlobalTypes.Types import DashboardAirlineMessageType, NegotiationStatus, SpotType
from spade.message import Message
import jsonpickle
from Conf import Conf

class BuySpotsBehaviour(OneShotBehaviour):
    async def on_start(self):
        #print("[Airline] Starting BuySpotBehaviour")
        pass

    async def run(self):
        ############### Send proposal ###################
        msg = Message(to="station@" + Conf().get_openfire_server())
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
        msg = Message(to="dashboardAirline@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "inform")
        bodyMessage:DashboardAirlinesMessage = DashboardAirlinesMessage(
            type=DashboardAirlineMessageType.NEGOTIATION,
            negotiationStatus=NegotiationStatus.PROPOSE,
            negotiationText=self.agent.airlineID + " proposal " + str(self.agent.price_per_spot) + "Є for " + str(self.agent.n_spots) + " spots of type " + self.spotTypeToString(self.agent.spotType)
        )
        msg.body = jsonpickle.encode(bodyMessage)
        await self.send(msg)

    def spotTypeToString(self,spotType:SpotType=None):
        if spotType == SpotType.COMMERCIAL: return "Comercial"
        if spotType == SpotType.MERCHANDISE: return "Merchandise"