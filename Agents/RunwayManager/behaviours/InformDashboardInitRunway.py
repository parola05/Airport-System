from spade.behaviour import OneShotBehaviour
from MessagesProtocol.InitStateRunways import InitStateRunways, RunwayInfo
from spade.message import Message
import jsonpickle
from Conf import Conf

class InformDashboardInitRunway(OneShotBehaviour):
    async def on_start(self):
        print("[RUNWAY] Starting Inform Dashboard Init State Behaviour . . .")

    async def run(self):
        msg = Message(to="dashboardRunway@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "inform")
        
        initStateRunways:InitStateRunways = InitStateRunways()
        for runway in self.agent.runways.values():
            initStateRunways.stations.append(
                RunwayInfo(
                    id=runway.id,
                    coord=runway.coord,  
                    available=runway.available
                )
            )
            
        msg.body = jsonpickle.encode(initStateRunways)
        await self.send(msg)