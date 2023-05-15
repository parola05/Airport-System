from spade.agent import Agent
import customtkinter
import sys
import platform
from .behaviours.ReceiveUpdates import ReceiveUpdatesBehaviour

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

class DashboardControlTower(Agent):
    async def setup(self):
        receiveUpdatesBehaviour = ReceiveUpdatesBehaviour()
        self.add_behaviour(receiveUpdatesBehaviour)

    def __init__(self,agent_name,password,master):
        super().__init__(agent_name,password)
        self.view = ControlTowerComponentView(master=master)
        self.tab_1_line = 0
        self.tab_2_line = 0

class ControlTowerComponentView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid(row=0, column=2, sticky="nsew")
        self.add("Airplane Requests")
        self.add("Queue")
        self.add("Global Stats")
        self.tab("Airplane Requests").grid_columnconfigure(0, weight=1)
        self.tab("Queue").grid_columnconfigure(0, weight=1)
        self.tab("Global Stats").grid_columnconfigure(0, weight=1)

        self.tab_1 = AirplanesRequests(self.tab("Airplane Requests"))
        self.tab_1.grid(row=0, column=0,sticky="nsew")
        self.tab_1.grid_rowconfigure(0, weight=1)
        self.tab_1.grid_columnconfigure(0, weight=1)
        
        self.tab_2 = QueueInTheAir(self.tab("Queue"))
        self.tab_2.grid(row=0, column=0,sticky="nsew")
        self.tab_2.grid_rowconfigure(0, weight=1)
        self.tab_2.grid_columnconfigure(0, weight=1)

        self.tab_3 = GlobalStats(self.tab("Global Stats"),fg_color="transparent")
        self.tab_3.grid(row=0, column=0,sticky="nsew")
        self.tab_3.grid_rowconfigure(0, weight=1)
        self.tab_3.grid_columnconfigure(0, weight=1)

class AirplanesRequests(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        progressbar = customtkinter.CTkProgressBar(master=self)
        progressbar.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        progressbar.configure(mode="indeterminnate")
        progressbar.start()

        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=1,column=0,sticky="nsew")
        
        self.textbox.tag_config("tag1", foreground="#5D78FF")
        self.textbox.tag_config("tag2", foreground="#73FF3A")
        self.textbox.tag_config("tag3", foreground="#FF5C5C")
        self.textbox.tag_config("tag4", foreground="#BD52FF")
        self.textbox.tag_config("tag5", foreground="#013220")
        self.textbox.tag_config("tag6", foreground="#BD52FF")
        self.textbox.tag_config("tag7", foreground="#FF915D")

class QueueInTheAir(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        progressbar = customtkinter.CTkProgressBar(master=self)
        progressbar.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        progressbar.configure(mode="indeterminnate")
        progressbar.start()

        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=1,column=0,sticky="nsew")
        
        self.textbox.tag_config("tag1", foreground="#5D78FF")
        self.textbox.tag_config("tag2", foreground="#73FF3A")
        self.textbox.tag_config("tag3", foreground="red")

class GlobalStats(customtkinter.CTkFrame):
     def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.labelTitle = customtkinter.CTkLabel(master=self, text="Global Stats About Airplane", font=("Helvetica", 18, "bold"))
        self.labelTitle.grid(row=0, column=0)

        self.timeInTheAirFrame = customtkinter.CTkFrame(master=self) 
        self.timeInTheAirFrame.grid(row=1, column=0)

        self.timeInTheAirLabel = customtkinter.CTkLabel(self.timeInTheAirFrame, text="Queue in the air avg. time:", anchor="w")
        self.timeInTheAirLabel.grid(row=0, column=0, padx=20, pady=(10, 0))

        self.timeInTheAirValue = customtkinter.CTkLabel(self.timeInTheAirFrame, text="0", anchor="w")
        self.timeInTheAirValue.grid(row=0, column=1, padx=20, pady=(10, 0))