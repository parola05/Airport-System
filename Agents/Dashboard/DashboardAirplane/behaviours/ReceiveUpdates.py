from spade.behaviour import CyclicBehaviour
import jsonpickle
from MessagesProtocol.DashboardAirplane import DashboardAirplane
from GlobalTypes.Types import DashboardAirplaneUpdate, StatusType
import customtkinter

class ReceiveUpdatesBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("Starting Receive Updates from Airplanes behaviour . . .")

    async def run(self):
        msg = await self.receive(timeout=100) 
        if msg:
            dashboardAirplane:DashboardAirplane = jsonpickle.decode(msg.body)

            # add airplane in airplanes list
            if dashboardAirplane.type == DashboardAirplaneUpdate.INFO:

                # add label entry for airplane ID
                labelID = customtkinter.CTkLabel(master=self.agent.view.airplanesTable, text=dashboardAirplane.airplaneInfo.id) 
                labelID.grid(row=self.agent.rowIndex, column=0, padx=10, pady=(0,10), sticky="ew")
                
                # add button to activate airplane actions (land, request to fly, etc)
                if dashboardAirplane.airplaneInfo.status == StatusType.IN_STATION: 
                    labelAction = customtkinter.CTkButton(master=self.agent.view.airplanesTable, command=lambda airplaneID=dashboardAirplane.airplaneInfo.id: self.agent.view.requestToTakeOff(airplaneID))
                    labelAction.grid(row=self.agent.rowIndex, column=1, padx=20, pady=(0,10))
                    labelAction.configure(text="Take Off")
                elif dashboardAirplane.airplaneInfo.status == StatusType.FLYING:
                    labelAction = customtkinter.CTkButton(master=self.agent.view.airplanesTable, command=lambda airplaneID=dashboardAirplane.airplaneInfo.id: self.agent.view.requestToLand(airplaneID))
                    labelAction.grid(row=self.agent.rowIndex, column=1, padx=20, pady=(0,10))
                    labelAction.configure(text="Land")
                else:
                    labelAction = customtkinter.CTkLabel(master=self.agent.view.airplanesTable, text="--None--")
                    labelAction.grid(row=self.agent.rowIndex, column=1, padx=20, pady=(0,10))
                
                # add label entry for airplane STATUS
                labelStatus = customtkinter.CTkLabel(master=self.agent.view.airplanesTable, text=self.agent.view.airplaneStatus(dashboardAirplane.airplaneInfo.status))
                labelStatus.grid(row=self.agent.rowIndex, column=2, padx=10, pady=(0,10), sticky="ew")
                
                # update rowIndex for next label
                self.agent.rowIndex += 1

                # keep STATUS to eventually updates some value in this label
                self.agent.view.labels[dashboardAirplane.airplaneInfo.id] = {}
                self.agent.view.labels[dashboardAirplane.airplaneInfo.id]["status"] = labelStatus