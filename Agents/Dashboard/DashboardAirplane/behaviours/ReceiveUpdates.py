from spade.behaviour import CyclicBehaviour
import jsonpickle
from MessagesProtocol.DashboardAirplaneMessage import DashboardAirplaneMessage
from GlobalTypes.Types import DashboardAirplaneMessageType, StatusType
import customtkinter

class ReceiveUpdatesBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("[DashboardAirplane] Starting ReceiveUpdatesBehaviour")

    async def run(self):
        msg = await self.receive(timeout=100) 
        if msg:
            dashboardAirplane:DashboardAirplaneMessage = jsonpickle.decode(msg.body)

            # add airplane in airplanes list
            if dashboardAirplane.type == DashboardAirplaneMessageType.CREATE:

                # add label entry for airplane ID
                labelId = customtkinter.CTkLabel(master=self.agent.view.airplanesTable)
                labelId.grid(row=self.agent.rowIndex, column=0, padx=20, pady=(0,10))
                labelId.configure(text=dashboardAirplane.airplaneInfo.id)

                # add label entry for airplane STATUS
                labelStatus = customtkinter.CTkLabel(master=self.agent.view.airplanesTable, text=self.agent.view.airplaneType(dashboardAirplane.airplaneInfo.typeTransport))
                labelStatus.grid(row=self.agent.rowIndex, column=1, padx=10, pady=(0,10), sticky="ew")
                
                # add label entry for airplane STATUS
                labelStatus = customtkinter.CTkLabel(master=self.agent.view.airplanesTable, text=self.agent.view.airplaneStatus(dashboardAirplane.airplaneInfo.status))
                labelStatus.grid(row=self.agent.rowIndex, column=2, padx=10, pady=(0,10), sticky="ew")
                
                # update rowIndex for next label
                self.agent.rowIndex += 1

                # keep STATUS to eventually updates some value in this label
                self.agent.view.labels[dashboardAirplane.airplaneInfo.id] = {}
                self.agent.view.labels[dashboardAirplane.airplaneInfo.id]["status"] = labelStatus

            elif dashboardAirplane.type == DashboardAirplaneMessageType.UPDATE:
                # self.agent.view.labels[dashboardAirplane.airplaneInfo.id] 
                self.agent.view.labels[dashboardAirplane.airplaneInfo.id]["status"].configure(text=self.agent.view.airplaneStatus(dashboardAirplane.airplaneInfo.status))