import customtkinter, sys, platform, tkinter
from spade.agent import Agent
from .behaviours.ReceiveUpdates import ReceiveUpdatesBehaviour

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from GlobalTypes.Coord import Coord
    
class DashboardRunway(Agent):
    async def setup(self):
        receiveUpdatesBehaviour = ReceiveUpdatesBehaviour()
        self.add_behaviour(receiveUpdatesBehaviour) 

    def __init__(self,agent_name,password,master):
        super().__init__(agent_name,password)
        self.view = RunwayComponentView(master=master)
        self.rowIndex = 1

class RunwayComponentView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.labels = {}
        
        self.toplevel_window = None

        labelID = customtkinter.CTkLabel(master=self, text="🛬 Runways", font=("Helvetica", 18, "bold"))
        labelID.grid(row=0, column=0)

        self.runwaysTable = customtkinter.CTkScrollableFrame(master=self)
        self.runwaysTable.grid(row=1,column=0,padx=10, pady=10,sticky="nsew")

        labelID = customtkinter.CTkLabel(master=self.runwaysTable, text="Runway ID", font=("Helvetica", 12, "bold"))
        labelID.grid(row=0, column=0, padx=20, pady=(0, 20),sticky="nsew")
        labelCoord = customtkinter.CTkLabel(master=self.runwaysTable, text="Position", font=("Helvetica", 12, "bold"))
        labelCoord.grid(row=0, column=1, padx=20, pady=(0, 20),sticky="nsew")
        labelAvailable = customtkinter.CTkLabel(master=self.runwaysTable, text="Available", font=("Helvetica", 12, "bold"))
        labelAvailable.grid(row=0, column=2, padx=20, pady=(0, 20),sticky="nsew")

    def isAvailable(self,isAvailable):
        if isAvailable:
            return "Yes"
        else:
            return "No"