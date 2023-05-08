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

class ControlTowerComponentView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid(row=0, column=2, sticky="nsew")
        self.add("Airplane Requests")
        self.add("Queue in the air")
        self.tab("Airplane Requests").grid_columnconfigure(0, weight=1)
        self.tab("Queue in the air").grid_columnconfigure(0, weight=1)

        self.tab_1 = AirplanesRequests(self.tab("Airplane Requests"))
        self.tab_1.grid(row=0, column=0,sticky="nsew")
        self.tab_1.grid_rowconfigure(0, weight=1)
        self.tab_1.grid_columnconfigure(0, weight=1)
        
        self.tab_2 = QueueInTheAir(self.tab("Queue in the air"))
        self.tab_2.grid(row=0, column=0,sticky="nsew")
        self.tab_2.grid_rowconfigure(0, weight=1)
        self.tab_2.grid_columnconfigure(0, weight=1)

class AirplanesRequests(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        progressbar = customtkinter.CTkProgressBar(master=self)
        progressbar.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        progressbar.configure(mode="indeterminnate")
        progressbar.start()

        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=1,column=0,sticky="nsew")
        
        self.textbox.tag_config("tag1", foreground="blue")
        self.textbox.tag_config("tag2", foreground="green")
        self.textbox.tag_config("tag3", foreground="red")

class QueueInTheAir(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)