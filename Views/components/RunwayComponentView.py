import customtkinter
import sys
import platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\..")
else:
    print("Unsupported operating system")

from Controllers.RunwayComponentController import RunwayComponentController
from GlobalTypes.Coord import Coord
    
class RunwayComponentView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.controller = RunwayComponentController()
        runways = self.controller.getRunways()

        self.toplevel_window = None

        # Create the title of the frame
        labelID = customtkinter.CTkLabel(master=self, text="Runways")
        labelID.grid(row=0, column=0)

        # Create the "Table" that will show the list of runways
        runwaysTable = customtkinter.CTkScrollableFrame(master=self)
        runwaysTable.grid(row=1,column=0,padx=10, pady=10,sticky="nsew")

        # Create the first row
        labelID = customtkinter.CTkLabel(master=runwaysTable, text="Runway ID")
        labelID.grid(row=0, column=0, padx=20, pady=(0, 20))
        labelSpots = customtkinter.CTkLabel(master=runwaysTable, text="Position")
        labelSpots.grid(row=0, column=1, padx=20, pady=(0, 20))

        # Create the n rows
        for rowIndex, runway in enumerate(runways):
            labelID = customtkinter.CTkLabel(master=runwaysTable, text=runway["id"])
            labelID.grid(row=rowIndex+1, column=0, padx=10, pady=(0, 20))
            labelSpots = customtkinter.CTkLabel(master=runwaysTable, text="( "+str(runway["x"])+" ; "+str(runway["y"])+" )")
            labelSpots.grid(row=rowIndex+1, column=1, padx=10, pady=(0, 20))

        # Create the button to add more stations
        createStationButton = customtkinter.CTkButton(self, text="Add Runway", command=self.openAddRunwaysForm)
        createStationButton.grid(row=2,column=0, padx=10, pady=10,sticky="nsew")

    def openAddRunwaysForm(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CreateRunwayFormView(self)  
        else:
            self.toplevel_window.focus()  

class CreateRunwayFormView(customtkinter.CTkToplevel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.title("Create a new runway")

        # Create the form widgets
        self.labelRunwayID = customtkinter.CTkLabel(self, text="Runway ID")
        self.entryRunwayID = customtkinter.CTkEntry(self)
        self.labelRunwayPosition = customtkinter.CTkLabel(self, text="Position")
        self.labelSeparator1 = customtkinter.CTkLabel(self, text="(")
        self.labelSeparator2 = customtkinter.CTkLabel(self, text=";")
        self.labelSeparator3 = customtkinter.CTkLabel(self, text=")")
        self.entryRunwayX = customtkinter.CTkEntry(self)
        self.entryRunwayY = customtkinter.CTkEntry(self)
        self.buttonCreateRunway = customtkinter.CTkButton(self, text="Create Runway", command=self.sendForm)
        
        # Lay out the form widgets using grid
        self.labelRunwayID.grid(row=0, column=0, padx=10, pady=10)
        self.entryRunwayID.grid(row=0, column=1, padx=10, pady=10)
        self.labelRunwayPosition.grid(row=1, column=0, padx=5, pady=0)
        self.labelSeparator1.grid(row=1, column=1, padx=5, pady=0)
        self.entryRunwayX.grid(row=1, column=2, padx=5, pady=0)
        self.labelSeparator2.grid(row=1, column=3, padx=5, pady=0)
        self.entryRunwayY.grid(row=1, column=4, padx=5, pady=0)
        self.labelSeparator3.grid(row=1, column=5, padx=5, pady=0)
        self.buttonCreateRunway.grid(row=2, column=0, padx=10, pady=10)
        
    def sendForm(self):
        # Get the form data
        runwayID = self.entryRunwayID.get()
        runwayCoord = Coord(self.entryRunwayX.get(), self.entryRunwayY.get())
        
        # TODO: Send the form data to a server or do something else with it
        
        # Close the form window
        self.destroy()
