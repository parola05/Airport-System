from spade.behaviour import CyclicBehaviour
import jsonpickle
from MessagesProtocol.DashboardRunwayMessage import DashboardRunwayMessage
from GlobalTypes.Types import DashboardRunwayMessageType
import customtkinter

class ReceiveUpdatesBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("[DashboardRunway] Starting ReceiveUpdatesBehaviour")

    async def run(self):
        msg = await self.receive(timeout=100) 
        if msg:
            dashboardRunwayMessage:DashboardRunwayMessage = jsonpickle.decode(msg.body)

            # add runway in runways list
            if dashboardRunwayMessage.type == DashboardRunwayMessageType.INFO:

                 for rowIndex, runway in enumerate(dashboardRunwayMessage.runways):

                    # add label entry for runway ID
                    labelID = customtkinter.CTkLabel(master=self.agent.view.runwaysTable, text=runway.id)
                    labelID.grid(row=self.agent.rowIndex, column=0, padx=20, pady=(0, 20),sticky="nsew")

                    # add label entry for runway position
                    labelPosition = customtkinter.CTkLabel(master=self.agent.view.runwaysTable, text="( "+str(round(runway.coord.x,2))+" ; "+str(round(runway.coord.y,2))+" )")
                    labelPosition.grid(row=self.agent.rowIndex, column=1, padx=20, pady=(0, 20),sticky="nsew")

                    # add label entry for runway available status
                    labelAvailable = customtkinter.CTkLabel(master=self.agent.view.runwaysTable, text=self.agent.view.isAvailable(runway.available))
                    labelAvailable.grid(row=self.agent.rowIndex, column=2, padx=20, pady=(0, 20),sticky="nsew")
                
                    # update rowIndex for next label
                    self.agent.rowIndex += 1

                    # keep label of available status to eventually update some value in this label
                    self.agent.view.labels[runway.id] = {}
                    self.agent.view.labels[runway.id]["available"] = labelAvailable

            elif dashboardRunwayMessage.type == DashboardRunwayMessageType.UPDATE:
                self.agent.view.labels[dashboardRunwayMessage.runwayToUpdate.id]["available"].configure(text=self.agent.view.isAvailable(dashboardRunwayMessage.runwayToUpdate.available))