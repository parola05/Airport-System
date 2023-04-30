import customtkinter
import sys
sys.path.append("..\..")
from Controllers.AirlinesComponentController import AirlinesComponentController

class AirlinesComponentView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.toplevel_window = None

        # get Airlines Controller
        self.controller = AirlinesComponentController()
        # get list of airlines
        self.airlines = self.controller.getAirlines()

        # Create the Title of the Frame
        labelID = customtkinter.CTkLabel(master=self, text="\U0001F6EB Airlines",font=("Helvetica", 18, "bold"))
        labelID.grid(row=0, column=0,padx=4,pady=4)

        # Create the "Table" that will show the list of airlines
        airlinesTable = customtkinter.CTkScrollableFrame(master=self)
        airlinesTable.grid(row=1,column=0,padx=10, pady=10,sticky="nsew")

        # Create the first row
        labelID = customtkinter.CTkLabel(master=airlinesTable, text="Airline ID")
        labelID.grid(row=0, column=0, padx=10, pady=(0, 20))

        # Create the n rows
        for rowIndex,airline in enumerate(self.airlines):
            labelID = customtkinter.CTkLabel(master=airlinesTable, text=airline["id"])
            labelID.grid(row=rowIndex+1, column=0, padx=10, pady=(0, 20))

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