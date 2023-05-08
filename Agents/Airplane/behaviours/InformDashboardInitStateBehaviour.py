from spade.behaviour import OneShotBehaviour
from MessagesProtocol.DashboardAirplane import DashboardAirplane, AirplaneInfo
from GlobalTypes.Types import DashboardAirplaneUpdate
from spade.message import Message
import jsonpickle
from Conf import Conf

class InformDashBoardInitStateBehaviour(OneShotBehaviour):
    async def on_start(self):
        print("Starting Inform Dashboard Init State Behaviour from Airplane. . .")

    async def run(self):
        msg = Message(to="dashboardAirplane@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "inform")
        
        airplaneInfo:AirplaneInfo = AirplaneInfo(
            id=self.agent.airplaneID,
            status=self.agent.status,
            airlineID=self.agent.airline
        )

        body:DashboardAirplane = DashboardAirplane(
            type=DashboardAirplaneUpdate.INFO,
            airplaneInfo=airplaneInfo
        )
            
        msg.body = jsonpickle.encode(body)
        await self.send(msg)