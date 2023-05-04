from spade.behaviour import CyclicBehaviour
import jsonpickle
from MessagesProtocol.DashboardAirlines import DashboardAirlines
from GlobalTypes.Types import DashboardAirlineUpdate

class ReceiveUpdatesBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("Starting Receive Updates from Airlines behaviour . . .")

    async def run(self):
        msg = await self.receive(timeout=100) 
        if msg:
            dashboardAirlines:DashboardAirlines = jsonpickle.decode(msg.body)

            if dashboardAirlines.type == DashboardAirlineUpdate.NEGOTIATION:
                self.agent.view.tab_2.textbox.insert(str(self.agent.line) + ".0", dashboardAirlines.negotiationtext + "\n")
                self.agent.line += 1 