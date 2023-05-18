import customtkinter
import sys
import platform
from spade.agent import Agent
from .behaviours.ReceiveUpdates import ReceiveUpdatesBehaviour

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

class DashboardStation(Agent):
    async def setup(self):
        receiveUpdatesBehaviour = ReceiveUpdatesBehaviour()
        self.add_behaviour(receiveUpdatesBehaviour)

    def __init__(self,agent_name,password,master):
        super().__init__(agent_name,password)
        self.view = StationComponentView(master=master)
    
class StationComponentView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.toplevel_window = None

        stations = []

        labelID = customtkinter.CTkLabel(master=self, text="\U0001F689 Stations", font=("Helvetica", 18, "bold"))
        labelID.grid(row=0, column=0)

        # Create the "Table" that will show the list of stations
        self.stationsTable = customtkinter.CTkScrollableFrame(master=self)
        self.stationsTable.grid(row=1,column=0,padx=10, pady=10,sticky="nsew")

        # Create the first row
        labelID = customtkinter.CTkLabel(master=self.stationsTable, text="Station ID", font=("Helvetica", 12, "bold"))
        labelID.grid(row=0, column=0, padx=10, pady=(0, 20))
        
        labelCommercialSpots = customtkinter.CTkLabel(master=self.stationsTable, text="C-Capacity", font=("Helvetica", 12, "bold"))
        labelCommercialSpots.grid(row=0, column=1, padx=10, pady=(0, 20))
        
        labelMerchandiseSpots = customtkinter.CTkLabel(master=self.stationsTable, text="M-Capacity", font=("Helvetica", 12, "bold"))
        labelMerchandiseSpots.grid(row=0, column=2, padx=10, pady=(0, 20))
        
        labelCommercialSpotsAvailable = customtkinter.CTkLabel(master=self.stationsTable, text="C-Available", font=("Helvetica", 12, "bold"))
        labelCommercialSpotsAvailable.grid(row=0, column=3, padx=10, pady=(0, 20))
        
        labelMerchandiseSpotsAvailable = customtkinter.CTkLabel(master=self.stationsTable, text="M-Available", font=("Helvetica", 12, "bold"))
        labelMerchandiseSpotsAvailable.grid(row=0, column=4, padx=10, pady=(0, 20))

        self.labels = {}

        for rowIndex,station in enumerate(stations):
            labelID = customtkinter.CTkLabel(master=self.stationsTable, text=station["id"])
            labelID.grid(row=rowIndex+1, column=0, padx=7, pady=(0, 20))
            labelCommercialSpots = customtkinter.CTkLabel(master=self.stationsTable, text=str(station["commercialSpots"]))
            labelCommercialSpots.grid(row=rowIndex+1, column=1, padx=7, pady=(0, 20))
            labelMerchandiseSpots = customtkinter.CTkLabel(master=self.stationsTable, text=str(station["merchandiseSpots"]))
            labelMerchandiseSpots.grid(row=rowIndex+1, column=2, padx=7, pady=(0, 20))
