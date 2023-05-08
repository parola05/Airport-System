from spade.behaviour import OneShotBehaviour
from MessagesProtocol.DashboardRunwayMessage import DashboardRunwayMessage, RunwayInfo
from GlobalTypes.Types import DashboardRunwayMessageType
from spade.message import Message
import jsonpickle
from Conf import Conf

class InformDashboardInitRunway(OneShotBehaviour):
    async def on_start(self):
        print("[RUNWAY] Starting Inform Dashboard Init State Behaviour . . .")

    async def run(self):
        msg = Message(to="dashboardRunway@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "inform")
        
        # create message object with type INFO
        dashboardRunwayMessage:DashboardRunwayMessage = DashboardRunwayMessage(type=DashboardRunwayMessageType.INFO)
        
        # fill runway's list in message
        for runway in self.agent.runways.values():
            dashboardRunwayMessage.runways.append(
                RunwayInfo(
                    id=runway.id,
                    coord=runway.coord,  
                    available=runway.available
                )
            )
            
        msg.body = jsonpickle.encode(dashboardRunwayMessage)
        await self.send(msg)