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

        # instance variable to use in behaviour
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

        #createStationButton = customtkinter.CTkButton(self, text="Add Runway", command=self.openAddRunwaysForm)
        #createStationButton.grid(row=2,column=0, padx=10, pady=10,sticky="nsew")

    def openAddRunwaysForm(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CreateRunwayFormView(self)  
        else:
            self.toplevel_window.focus()  

    def isAvailable(self,isAvailable):
        if isAvailable:
            return "Yes"
        else:
            return "No"

class CreateRunwayFormView(customtkinter.CTkToplevel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.title("Create a new runway")

        self.labelRunwayID = customtkinter.CTkLabel(self, text="Runway ID")
        self.entryRunwayID = customtkinter.CTkEntry(self)
        self.labelRunwayPosition = customtkinter.CTkLabel(self, text="Position")
        self.labelSeparator1 = customtkinter.CTkLabel(self, text="(")
        self.entryRunwayX = customtkinter.CTkEntry(self)
        self.labelSeparator2 = customtkinter.CTkLabel(self, text=";")
        self.entryRunwayY = customtkinter.CTkEntry(self)
        self.labelSeparator3 = customtkinter.CTkLabel(self, text=")")
        self.buttonCreateRunway = customtkinter.CTkButton(self, text="Create Runway", command=self.sendForm)

        self.labelRunwayID.grid(row=0, column=0, padx=10, pady=10)
        self.entryRunwayID.grid(row=0, column=1, padx=10, pady=10)
        self.labelRunwayPosition.grid(row=1, column=0, padx=(10,10), pady=(10,10))
        self.labelSeparator1.grid(row=1, column=1, padx=10, pady=10)
        self.entryRunwayX.grid(row=1, column=2, padx=10, pady=10)
        self.labelSeparator2.grid(row=1, column=3, padx=10, pady=10)
        self.entryRunwayY.grid(row=1, column=4, padx=10, pady=10)
        self.labelSeparator3.grid(row=1, column=5, padx=10, pady=10)
        self.buttonCreateRunway.grid(row=2, column=2, padx=10, pady=10)
        
    def sendForm(self):
        runwayID = self.entryRunwayID.get()
        runwayCoord = Coord(self.entryRunwayX.get(), self.entryRunwayY.get())
        runwayAvailable = True

        # TODO: Send the form data to a server or do something else with it
        
        # Close the form window
        self.destroy()

    def isAvailable(isAvailable):
        if isAvailable:
            return "Yes"
        else:
            return "No"
