from spade.behaviour import OneShotBehaviour
from MessagesProtocol.DashboardAirlines import DashboardAirlines, AirlineInfo
from GlobalTypes.Types import DashboardAirlineUpdate
from spade.message import Message
import jsonpickle

class InformDashBoardInitStateBehaviour(OneShotBehaviour):
    async def on_start(self):
        print("Starting Inform Dashboard Init State Behaviour . . .")

    async def run(self):
        msg = Message(to="dashboardAirline@laptop-vun6ls3v.lan")
        msg.set_metadata("performative", "inform")
        
        airlineInfo:AirlineInfo = AirlineInfo(
            id=self.agent.airlineID
        )

        body:DashboardAirlines = DashboardAirlines(
            type=DashboardAirlineUpdate.INFO,
            airlineInfo=airlineInfo
        )
            
        msg.body = jsonpickle.encode(body)
        await self.send(msg)