from spade.behaviour import OneShotBehaviour
from MessagesProtocol.DashboardAirlines import DashboardAirlines, AirlineInfo
from GlobalTypes.Types import DashboardAirlineUpdate
from spade.message import Message
import jsonpickle
from Conf import Conf

class InformDashBoardInitStateBehaviour(OneShotBehaviour):
    async def on_start(self):
        #print("Starting Inform Dashboard Init State Behaviour from Airline . . .")
        pass

    async def run(self):
        msg = Message(to="dashboardAirline@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "inform")
        
        airlineInfo:AirlineInfo = AirlineInfo(
            id=self.agent.airlineID,
            nSpotsCommercial=0,
            nSpotsMerchandise=0,
        )

        body:DashboardAirlines = DashboardAirlines(
            type=DashboardAirlineUpdate.INFO,
            airlineInfo=airlineInfo
        )
            
        msg.body = jsonpickle.encode(body)
        await self.send(msg)