from spade.behaviour import CyclicBehaviour
import jsonpickle
from MessagesProtocol.InitStateStations import InitStateStations,StationInfo
import customtkinter

class ReceiveUpdatesBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("Starting Receive Updates from Stations behaviour . . .")

    async def run(self):
        msg = await self.receive(timeout=100) 
        if msg:
            initStateStations:InitStateStations = jsonpickle.decode(msg.body)

            # Create the n rows
            for rowIndex,station in enumerate(initStateStations.stations):
                labelID = customtkinter.CTkLabel(master=self.agent.view.stationsTable, text=station.id)
                labelID.grid(row=rowIndex+1, column=0, padx=7, pady=(0, 20))
                labelCommercialSpots = customtkinter.CTkLabel(master=self.agent.view.stationsTable, text=str(station.merchandise_capacity))
                labelCommercialSpots.grid(row=rowIndex+1, column=1, padx=7, pady=(0, 20))
                labelMerchandiseSpots = customtkinter.CTkLabel(master=self.agent.view.stationsTable, text=str(station.commercial_capacity))
                labelMerchandiseSpots.grid(row=rowIndex+1, column=2, padx=7, pady=(0, 20))