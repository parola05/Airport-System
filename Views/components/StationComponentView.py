import customtkinter
import sys
import platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\..")
else:
    print("Unsupported operating system")

from Controllers.StationComponentController import StationComponentController
    
class StationComponentView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # get Stations Controller
        self.controller = StationComponentController()
        # get list of stations
        stations = self.controller.getStations()

        self.toplevel_window = None

        # Create the Title of the Frame
        labelID = customtkinter.CTkLabel(master=self, text="Stations")
        labelID.grid(row=0, column=0)

        # Create the "Table" that will show the list of stations
        stationsTable = customtkinter.CTkScrollableFrame(master=self)
        stationsTable.grid(row=1,column=0,padx=10, pady=10,sticky="nsew")

        # Create the first row
        labelID = customtkinter.CTkLabel(master=stationsTable, text="Station ID")
        labelID.grid(row=0, column=0, padx=10, pady=(0, 20))
        labelCommercialSpots = customtkinter.CTkLabel(master=stationsTable, text="Commercial Spots Capacity")
        labelCommercialSpots.grid(row=0, column=1, padx=10, pady=(0, 20))
        labelMerchandiseSpots = customtkinter.CTkLabel(master=stationsTable, text="Merchandise Sposts Capacity")
        labelMerchandiseSpots.grid(row=0, column=2, padx=10, pady=(0, 20))

        # Create the n rows
        for rowIndex,station in enumerate(stations):
            labelID = customtkinter.CTkLabel(master=stationsTable, text=station["id"])
            labelID.grid(row=rowIndex+1, column=0, padx=10, pady=(0, 20))
            labelCommercialSpots = customtkinter.CTkLabel(master=stationsTable, text=str(station["commercialSpots"]))
            labelCommercialSpots.grid(row=rowIndex+1, column=1, padx=10, pady=(0, 20))
            labelMerchandiseSpots = customtkinter.CTkLabel(master=stationsTable, text=str(station["merchandiseSpots"]))
            labelMerchandiseSpots.grid(row=rowIndex+1, column=2, padx=10, pady=(0, 20))

        # Create the button to add more stations
        createStationButton = customtkinter.CTkButton(self, text="Add Station", command=self.openAddStationsForm)
        createStationButton.grid(row=2,column=0, padx=10, pady=10,sticky="nsew")

    def openAddStationsForm(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CreateStationFormView(self)  
        else:
            self.toplevel_window.focus()  

class CreateStationFormView(customtkinter.CTkToplevel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Create the form widgets
        self.labelStationID = customtkinter.CTkLabel(self, text="Station ID")
        self.entryStationID = customtkinter.CTkEntry(self)
        self.labelCommercialSpotsCapacity = customtkinter.CTkLabel(self, text="Nº commercial spots")
        self.entryCommercialSpotsCapacity = customtkinter.CTkEntry(self)
        self.labelMerchandiseSpotsCapacity = customtkinter.CTkLabel(self, text="Nº merchandise spots")
        self.entryMerchandiseSpotsCapacity = customtkinter.CTkEntry(self)
        self.buttonCreateStation = customtkinter.CTkButton(self, text="Create Station", command=self.sendForm)
        
        # Lay out the form widgets using grid
        self.labelStationID.grid(row=0, column=0, padx=10, pady=10)
        self.entryStationID.grid(row=0, column=1, padx=10, pady=10)
        self.labelCommercialSpotsCapacity.grid(row=1, column=0, padx=10, pady=10)
        self.entryCommercialSpotsCapacity.grid(row=1, column=1, padx=10, pady=10)
        self.labelMerchandiseSpotsCapacity.grid(row=2, column=0, padx=10, pady=10)
        self.entryMerchandiseSpotsCapacity.grid(row=2, column=1, padx=10, pady=10)
        self.buttonCreateStation.grid(row=3, column=1, padx=10, pady=10)
        
    def sendForm(self):
        # Get the form data
        stationID = self.entryStationID.get()
        commericialSpotsCapacity = self.entryCommercialSpotsCapacity.get()
        merchandiseSpotsCapacity = self.entryMerchandiseSpotsCapacity.get()
        
        # TODO: Send the form data to a server or do something else with it
        
        # Close the form window
        self.destroy()
