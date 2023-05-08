from spade.behaviour import CyclicBehaviour
from spade.message import Message
from MessagesProtocol.DashboardAirlinesMessage import DashboardAirlinesMessage, AirlineInfo
from GlobalTypes.Types import DashboardAirlineMessageType, SpotType
from Conf import Conf
import jsonpickle

class ReceiveProposalAnswerBehaviour(CyclicBehaviour):
    async def on_start(self):
        #print("[Airline] ReceiveProposalAnswerBehaviour")
        pass

    async def run(self):
        msg = await self.receive(timeout=100) 

        if msg:
            performative = msg.get_metadata('performative')
            
            # If Airline bought spots -> inform DashboardAirline to update the view
            # with the new value of spots bought
            if performative == 'agree':
                msg = Message(to="dashboardAirline@" + Conf().get_openfire_server())
                msg.set_metadata("performative", "inform")

                nSpotsCommercial = 0
                nSpotsMerchandise = 0
                if self.agent.spotType == SpotType.COMMERCIAL:
                    nSpotsCommercial = self.agent.n_spots
                if self.agent.spotType == SpotType.MERCHANDISE:
                    nSpotsMerchandise = self.agent.n_spots

                airlineInfo:AirlineInfo = AirlineInfo(
                    id=self.agent.airlineID,
                    nSpotsCommercial=nSpotsCommercial,
                    nSpotsMerchandise=nSpotsMerchandise,
                )

                body:DashboardAirlinesMessage = DashboardAirlinesMessage(
                    type=DashboardAirlineMessageType.UPDATE,
                    airlineInfo=airlineInfo
                )

                msg.body = jsonpickle.encode(body)
                await self.send(msg)
            elif performative == 'reject-proposal':
                pass
        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")