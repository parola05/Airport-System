from spade.behaviour import OneShotBehaviour
from MessagesProtocol.DashboardStationMessage import DashboardStationMessage, StationInfo
from GlobalTypes.Types import DashboardStationMessageType
from spade.message import Message
import jsonpickle
from Conf import Conf

class InformDashBoardInitStateBehaviour(OneShotBehaviour):
    async def on_start(self):
        print("[StationManager] Starting InformDashBoardInitStateBehaviour")

    async def run(self):
        msg = Message(to="dashboardStation@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "inform")
        
        dashboardStationMessage:DashboardStationMessage = DashboardStationMessage(type=DashboardStationMessageType.INFO)
        for station in self.agent.stations.values():
            dashboardStationMessage.stations.append(
                StationInfo(
                    id=station.id,
                    merchandise_capacity=station.spots_available_merchandise,  
                    commercial_capacity=station.spots_available_commercial
                )
            )
            
        msg.body = jsonpickle.encode(dashboardStationMessage)
        await self.send(msg)