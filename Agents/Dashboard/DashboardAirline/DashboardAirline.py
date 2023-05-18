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

class DashboardAirline(Agent):
    async def setup(self):
        receiveUpdatesBehaviour = ReceiveUpdatesBehaviour()
        self.add_behaviour(receiveUpdatesBehaviour)

    def __init__(self,agent_name,password,master):
        super().__init__(agent_name,password)
        self.view = AirlinesComponentView(master=master)
        self.line = 0
        self.rowIndex = 1

class AirlinesComponentView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid(row=0, column=2, sticky="nsew")
        self.add("Airlines")
        self.add("Spots Negotiation")
        self.tab("Airlines").grid_columnconfigure(0, weight=1)
        self.tab("Spots Negotiation").grid_columnconfigure(0, weight=1)
        self.tab_1 = Airlines(self.tab("Airlines"))
        self.tab_1.grid(row=0, column=0,sticky="nsew")
        self.tab_1.grid_rowconfigure(0, weight=1)
        self.tab_1.grid_columnconfigure(0, weight=1)
        self.tab_2 = SpotsNegotiation(self.tab("Spots Negotiation"),fg_color="transparent")
        self.tab_2.grid(row=0, column=0, sticky="nsew")
        self.tab_2.grid_rowconfigure(0, weight=1)
        self.tab_2.grid_columnconfigure(0, weight=1)

class Airlines(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.toplevel_window = None
        self.labels = {}

        self.airlinesTable = customtkinter.CTkScrollableFrame(master=self)
        self.airlinesTable.grid(row=1,column=0,padx=10, pady=10,sticky="nsew")

        # Create the first row
        labelID = customtkinter.CTkLabel(master=self.airlinesTable, text="Airline ID", font=("Helvetica", 12, "bold"))
        labelID.grid(row=0, column=0, padx=10, pady=(0, 20))
        labelID = customtkinter.CTkLabel(master=self.airlinesTable, text="Commercial Spots", font=("Helvetica", 12, "bold"))
        labelID.grid(row=0, column=1, padx=10, pady=(0, 20))
        labelID = customtkinter.CTkLabel(master=self.airlinesTable, text="Merchandise Spots", font=("Helvetica", 12, "bold"))
        labelID.grid(row=0, column=2, padx=10, pady=(0, 20))

class SpotsNegotiation(customtkinter.CTkFrame):
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