from spade.behaviour import OneShotBehaviour
from MessagesProtocol.DashboardAirlinesMessage import DashboardAirlinesMessage, AirlineInfo
from GlobalTypes.Types import DashboardAirlineMessageType
from spade.message import Message
import jsonpickle
from Conf import Conf

class InformDashBoardInitStateBehaviour(OneShotBehaviour):
    async def on_start(self):
        #print("[Airline] Starting  InformDashboardInitStateBehaviour"")
        pass

    async def run(self):
        msg = Message(to="dashboardAirline@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "inform")
        
        airlineInfo:AirlineInfo = AirlineInfo(
            id=self.agent.airlineID,
            nSpotsCommercial=0,
            nSpotsMerchandise=0,
        )

        body:DashboardAirlinesMessage = DashboardAirlinesMessage(
            type=DashboardAirlineMessageType.INFO,
            airlineInfo=airlineInfo
        )
            
        msg.body = jsonpickle.encode(body)
        await self.send(msg)