import customtkinter
import sys
import platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")
    
from Controllers.AirlinesComponentController import AirlinesComponentController

class AirlinesComponentView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.toplevel_window = None

        self.controller = AirlinesComponentController()
        self.airlines = self.controller.getAirlines()

        labelID = customtkinter.CTkLabel(master=self, text="\U0001F6EB Airlines",font=("Helvetica", 18, "bold"))
        labelID.grid(row=0, column=0,padx=4,pady=4)

        airlinesTable = customtkinter.CTkScrollableFrame(master=self)
        airlinesTable.grid(row=1,column=0,padx=10, pady=10,sticky="nsew")

        labelID = customtkinter.CTkLabel(master=airlinesTable, text="Airline ID")
        labelID.grid(row=0, column=0, padx=10, pady=(0, 20))

        for rowIndex,airline in enumerate(self.airlines):
            labelID = customtkinter.CTkLabel(master=airlinesTable, text=airline["id"])
            labelID.grid(row=rowIndex+1, column=0, padx=10, pady=(0, 20))

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
        
        self.labelAirlineID = customtkinter.CTkLabel(self, text="Airline ID")
        self.entryAirlineID = customtkinter.CTkEntry(self)

        self.labelAirlineID.grid(row=0, column=0, padx=10, pady=10)
        self.entryAirlineID.grid(row=0, column=1, padx=10, pady=10)
        
    def sendForm(self):
        airlineID = self.entryAirlineID.get()
        print(airlineID)

        # TODO: Send the form data to a server or do something else with it
        
        self.destroy()