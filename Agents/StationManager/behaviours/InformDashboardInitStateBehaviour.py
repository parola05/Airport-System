from spade.behaviour import OneShotBehaviour
from MessagesProtocol.InitStateStations import InitStateStations, StationInfo
from spade.message import Message
import jsonpickle
from Conf import Conf

class InformDashBoardInitStateBehaviour(OneShotBehaviour):
    async def on_start(self):
        print("Starting Inform Dashboard Init State Behaviour . . .")

    async def run(self):
        msg = Message(to="dashboardStation@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "inform")
        
        initStateStations:InitStateStations = InitStateStations()
        for station in self.agent.stations.values():
            initStateStations.stations.append(
                StationInfo(
                    id=station.id,
                    merchandise_capacity=station.spots_available_merchandise,  
                    commercial_capacity=station.spots_available_commercial
                )
            )
            
        msg.body = jsonpickle.encode(initStateStations)
        await self.send(msg)