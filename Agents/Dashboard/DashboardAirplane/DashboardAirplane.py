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

from GlobalTypes.Types import StatusType, Priority, SpotType

class DashboardAirplane(Agent):
    async def setup(self):
        receiveUpdatesBehaviour = ReceiveUpdatesBehaviour()
        self.add_behaviour(receiveUpdatesBehaviour)

    def __init__(self,agent_name,password,master):
        super().__init__(agent_name,password)
        self.view = AirplanesComponentView(master=master)
        self.rowIndex = 1

class AirplanesComponentView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # instance variable to use in behaviour
        self.labels = {}
        self.toplevel_window = None
        
        labelID = customtkinter.CTkLabel(master=self, text="\U0001F6EA Airplanes", font=("Helvetica", 18, "bold"))
        labelID.grid(row=0, column=0)

        self.airplanesTable = customtkinter.CTkScrollableFrame(master=self)
        self.airplanesTable.grid(row=1,column=0,padx=10,pady=10,sticky="nsew")

        labelID = customtkinter.CTkLabel(master=self.airplanesTable, text="Airplane ID", font=("Helvetica", 12, "bold"))
        labelID.grid(row=0, column=0, padx=10, pady=(0, 10))
        labelID = customtkinter.CTkLabel(master=self.airplanesTable, text="Type", font=("Helvetica", 12, "bold"))
        labelID.grid(row=0, column=1, padx=10, pady=(0, 10))
        labelTakeOff = customtkinter.CTkLabel(master=self.airplanesTable, text="Status", font=("Helvetica", 12, "bold"))
        labelTakeOff.grid(row=0, column=2, padx=10, pady=(0, 10))

    def airplaneStatus(self,statusType):
        if statusType == 1:
            return "In Station"
        elif statusType == 2:
            return "Flying"
        elif statusType == 3:
            return "Landing"
        elif statusType == 4:
            return "Waiting to take off"
        elif statusType == 5:
            return "Waiting to land"
        elif statusType == 6:
            return "Going to another airport"
        elif statusType == 7:
            return "Taking Off"
        
    def airplaneType(self,spotType):
        if spotType == 1:
            return "Merchandise"
        elif spotType == 2:
            return "Commercial"