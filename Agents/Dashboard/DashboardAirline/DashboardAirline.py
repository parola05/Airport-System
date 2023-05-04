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
        self.rowIndex = 0

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

        # Create the "Table" that will show the list of airlines
        self.airlinesTable = customtkinter.CTkScrollableFrame(master=self)
        self.airlinesTable.grid(row=1,column=0,padx=10, pady=10,sticky="nsew")

        # Create the first row
        labelID = customtkinter.CTkLabel(master=self.airlinesTable, text="Airline ID")
        labelID.grid(row=0, column=0, padx=10, pady=(0, 20))

        # Create the button to add more airline
        createAirlineButton = customtkinter.CTkButton(self, text="Add Airline", command=self.openAddAirlineForm)
        createAirlineButton.grid(row=2,column=0, padx=10, pady=10,sticky="nsew")

    def openAddAirlineForm(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CreateAirlineFormView(self)  
        else:
            self.toplevel_window.focus()  

class CreateAirlineFormView(customtkinter.CTkToplevel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Create the form widgets
        self.labelAirlineID = customtkinter.CTkLabel(self, text="Airline ID")
        self.entryAirlineID = customtkinter.CTkEntry(self)

        # Lay out the form widgets using grid
        self.labelAirlineID.grid(row=0, column=0, padx=10, pady=10)
        self.entryAirlineID.grid(row=0, column=1, padx=10, pady=10)
        
    def sendForm(self):
        # Get the form data
        airlineID = self.entryAirlineID.get()

        print(airlineID)

        # TODO: Send the form data to a server or do something else with it
        
        # Close the form window
        self.destroy()

class SpotsNegotiation(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        progressbar = customtkinter.CTkProgressBar(master=self)
        progressbar.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        progressbar.configure(mode="indeterminnate")
        progressbar.start()

        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=1,column=0,sticky="nsew")