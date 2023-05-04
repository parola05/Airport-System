from spade.behaviour import CyclicBehaviour
import jsonpickle
from MessagesProtocol.DashboardAirlines import DashboardAirlines, NegotiationStatus
from GlobalTypes.Types import DashboardAirlineUpdate
import customtkinter

class ReceiveUpdatesBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("Starting Receive Updates from Airlines behaviour . . .")

    async def run(self):
        msg = await self.receive(timeout=100) 
        if msg:
            dashboardAirlines:DashboardAirlines = jsonpickle.decode(msg.body)

            if dashboardAirlines.type == DashboardAirlineUpdate.NEGOTIATION:

                # SET tag for text color
                tag = ""
                if dashboardAirlines.negotiationStatus == NegotiationStatus.PROPOSE:
                    tag = "tag1"
                elif dashboardAirlines.negotiationStatus == NegotiationStatus.SUCCESS:
                    tag = "tag2"
                elif dashboardAirlines.negotiationStatus == NegotiationStatus.FAIL:
                    tag = "tag3"

                self.agent.view.tab_2.textbox.insert(str(self.agent.line) + ".0", "> " + dashboardAirlines.negotiationtext + "\n",tag)
                self.agent.line += 1 

            elif dashboardAirlines.type == DashboardAirlineUpdate.INFO:
                labelID = customtkinter.CTkLabel(master=self.agent.view.tab_1.airlinesTable, text=dashboardAirlines.airlineInfo.id)
                labelID.grid(row=self.agent.rowIndex, column=0, padx=10, pady=(0, 20))
                self.agent.rowIndex += 1