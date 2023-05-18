from spade.behaviour import CyclicBehaviour
import jsonpickle
from MessagesProtocol.DashboardStationMessage import DashboardStationMessage
from GlobalTypes.Types import DashboardStationMessageType
import customtkinter

class ReceiveUpdatesBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("[DashboardStation] Starting ReceiveUpdatesBehaviour")

    async def run(self):
        msg = await self.receive(timeout=100) 
        if msg:
            dashboardStationMessage:DashboardStationMessage = jsonpickle.decode(msg.body)

            if dashboardStationMessage.type == DashboardStationMessageType.INFO:
                
                for rowIndex,station in enumerate(dashboardStationMessage.stations):
                    labelID = customtkinter.CTkLabel(master=self.agent.view.stationsTable, text=station.id)
                    labelID.grid(row=rowIndex+1, column=0, padx=7, pady=(0, 20))
                    
                    labelCommercialSpots = customtkinter.CTkLabel(master=self.agent.view.stationsTable, text=str(station.merchandise_capacity))
                    labelCommercialSpots.grid(row=rowIndex+1, column=1, padx=7, pady=(0, 20))
                    
                    labelMerchandiseSpots = customtkinter.CTkLabel(master=self.agent.view.stationsTable, text=str(station.commercial_capacity))
                    labelMerchandiseSpots.grid(row=rowIndex+1, column=2, padx=7, pady=(0, 20))

                    labelCommercialSpotsAvailable = customtkinter.CTkLabel(master=self.agent.view.stationsTable, text=str(station.merchandise_available))
                    labelCommercialSpotsAvailable.grid(row=rowIndex+1, column=3, padx=7, pady=(0, 20))
                    
                    labelMerchandiseSpotsAvailable = customtkinter.CTkLabel(master=self.agent.view.stationsTable, text=str(station.commercial_available))
                    labelMerchandiseSpotsAvailable.grid(row=rowIndex+1, column=4, padx=7, pady=(0, 20))

                    self.agent.view.labels[station.id] = {}
                    self.agent.view.labels[station.id]["Commercial Available"] = labelCommercialSpotsAvailable
                    self.agent.view.labels[station.id]["Merchandise Available"] = labelMerchandiseSpotsAvailable

            elif dashboardStationMessage.type == DashboardStationMessageType.UPDATE:
                self.agent.view.labels[dashboardStationMessage.stationToUpdate.id]["Commercial Available"].configure(text=str(dashboardStationMessage.stationToUpdate.commercial_available))
                self.agent.view.labels[dashboardStationMessage.stationToUpdate.id]["Merchandise Available"].configure(text=str(dashboardStationMessage.stationToUpdate.merchandise_available))