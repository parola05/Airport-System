from spade.behaviour import OneShotBehaviour
from MessagesProtocol.DashboardAirplaneMessage import DashboardAirplaneMessage, AirplaneInfo
from GlobalTypes.Types import DashboardAirplaneMessageType
from spade.message import Message
import jsonpickle
from Conf import Conf

class InformDashBoardInitStateBehaviour(OneShotBehaviour):
    async def on_start(self):
        print("[Airplane] starting InformDashBoardInitStateBehaviour")

    async def run(self):
        msg = Message(to="dashboardAirplane@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "inform")
        
        airplaneInfo:AirplaneInfo = AirplaneInfo(
            id=self.agent.airplaneID,
            status=self.agent.status,
            airlineID=self.agent.airline,
            typeTransport=self.agent.typeTransport
        )

        body:DashboardAirplaneMessage = DashboardAirplaneMessage(
            type=DashboardAirplaneMessageType.CREATE,
            airplaneInfo=airplaneInfo
        )
            
        msg.body = jsonpickle.encode(body)
        await self.send(msg)