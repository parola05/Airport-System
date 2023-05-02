import customtkinter
import sys
import platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from Controllers.AirplanesComponentController import AirplanesComponentController
from GlobalTypes.Types import StatusType, Priority, SpotType

class AirplanesComponentView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.controller = AirplanesComponentController()
        airplanes = self.controller.getAirplanes()

        self.toplevel_window = None
        
        labelID = customtkinter.CTkLabel(master=self, text="\U0001F6EA Airplanes", font=("Helvetica", 18, "bold"))
        labelID.grid(row=0, column=0)

        airplanesTable = customtkinter.CTkScrollableFrame(master=self)
        airplanesTable.grid(row=1,column=0,padx=10,pady=10,sticky="nsew")

        labelID = customtkinter.CTkLabel(master=airplanesTable, text="Airplane ID")
        labelID.grid(row=0, column=0, padx=10, pady=(0, 10))
        labelTakeOff = customtkinter.CTkLabel(master=airplanesTable, text="Action")
        labelTakeOff.grid(row=0, column=1, padx=10, pady=(0, 10))
        labelTakeOff = customtkinter.CTkLabel(master=airplanesTable, text="Status")
        labelTakeOff.grid(row=0, column=2, padx=10, pady=(0, 10))

        for rowIndex, airplane in enumerate(airplanes):
            labelID = customtkinter.CTkLabel(master=airplanesTable, text=airplane["id"])
            labelID.grid(row=rowIndex+1, column=0, padx=10, pady=(0,10), sticky="ew")
            if airplane["status"] == StatusType.IN_STATION: #StatusType.PARKED:
                labelAction = customtkinter.CTkButton(master=airplanesTable, command=lambda airplaneID=airplane["id"]: self.requestToTakeOff(airplaneID))
                labelAction.grid(row=rowIndex+1, column=1, padx=20, pady=(0,10))
                labelAction.configure(text="Take Off")
            elif airplane["status"] == StatusType.FLYING:
                labelAction = customtkinter.CTkButton(master=airplanesTable, command=lambda airplaneID=airplane["id"]: self.requestToLand(airplaneID))
                labelAction.grid(row=rowIndex+1, column=1, padx=20, pady=(0,10))
                labelAction.configure(text="Land")
            else:
                labelAction = customtkinter.CTkLabel(master=airplanesTable, text="--None--")
                labelAction.grid(row=rowIndex+1, column=1, padx=20, pady=(0,10))
            labelID = customtkinter.CTkLabel(master=airplanesTable, text=self.airplaneStatus(airplane["status"]))
            labelID.grid(row=rowIndex+1, column=2, padx=10, pady=(0,10), sticky="ew")

        createStationButton = customtkinter.CTkButton(self, text="Create Airplane", command=self.openCreateAirplanesForm)
        createStationButton.grid(row=2,column=0, padx=10, pady=10,sticky="nsew")

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
        #elif statusType == 7:
        #    return "Parked"
        
    def requestToTakeOff(self, airplaneID):
        print(f"Airplane {airplaneID} has request to take off")

    def requestToLand(self, airplaneID):
        print(f"Airplane {airplaneID} has request to land")

    def openCreateAirplanesForm(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CreateAirplaneFormView(self)  
        else:
            self.toplevel_window.focus()  

class CreateAirplaneFormView(customtkinter.CTkToplevel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.title("Create a new airplane")

        self.labelAirplaneAirline = customtkinter.CTkLabel(self, text="Airline")
        self.entryAirline = customtkinter.CTkEntry(self)
        self.labelTypeTransport = customtkinter.CTkLabel(self, text="Type of Transport")
        self.labelCommercial = customtkinter.CTkCheckBox(self, text="Commercial", command=self.checkOnlyOneType, onvalue="on", offvalue="off")
        self.labelMerchandise = customtkinter.CTkCheckBox(self, text="Merchandise", command=self.checkOnlyOneType, onvalue="on", offvalue="off")
        self.labelPriority = customtkinter.CTkLabel(self, text="Priority")
        self.labelHigh= customtkinter.CTkCheckBox(self, text="High", command=self.checkOnlyOneType, onvalue="on", offvalue="off")
        self.labelMedium = customtkinter.CTkCheckBox(self, text="Medium", command=self.checkOnlyOneType, onvalue="on", offvalue="off")
        self.labelLow = customtkinter.CTkCheckBox(self, text="Low", command=self.checkOnlyOneType, onvalue="on", offvalue="off")
        self.labelOrigin = customtkinter.CTkLabel(self, text="Origin")
        self.entryOrigin = customtkinter.CTkEntry(self)
        self.labelDestiny = customtkinter.CTkLabel(self, text="Destiny")
        self.entryDestiny = customtkinter.CTkEntry(self)
        self.labelDate = customtkinter.CTkLabel(self, text="Date (DD/MM/YYYY)")
        self.entryDate = customtkinter.CTkEntry(self)
        self.labelTime = customtkinter.CTkLabel(self, text="Time (hh:mm)")
        self.entryTime = customtkinter.CTkEntry(self)
        self.buttonCreateAirplane = customtkinter.CTkButton(self, text="Create", command=self.sendForm)
        
        self.labelAirplaneAirline.grid(row=0, column=0, padx=10, pady=10)
        self.entryAirline.grid(row=0, column=1, padx=10, pady=10)
        self.labelTypeTransport.grid(row=1, column=0, padx=10, pady=10)
        self.labelCommercial.grid(row=1, column=1, padx=10, pady=10)
        self.labelMerchandise.grid(row=1, column=2, padx=10, pady=10)
        self.labelPriority.grid(row=2, column=0, padx=10, pady=10)
        self.labelHigh.grid(row=2, column=1, padx=10, pady=10)
        self.labelMedium.grid(row=2, column=2, padx=10, pady=10)
        self.labelLow.grid(row=2, column=3, padx=10, pady=10)
        self.labelOrigin.grid(row=3, column=0, padx=10, pady=10)
        self.entryOrigin.grid(row=3, column=1, padx=10, pady=10)
        self.labelDestiny.grid(row=4, column=0, padx=10, pady=10)
        self.entryDestiny.grid(row=4, column=1, padx=10, pady=10)
        self.labelDate.grid(row=5, column=0, padx=10, pady=10)
        self.entryDate.grid(row=5, column=1, padx=10, pady=10)
        self.labelTime.grid(row=6, column=0, padx=10, pady=10)
        self.entryTime.grid(row=6, column=1, padx=10, pady=10)
        self.buttonCreateAirplane.grid(row=7, column=0, padx=10, pady=10, columnspan=4)

    def checkOnlyOneType(self):
        if self.labelCommercial.get() == 'on':
            self.labelCommercial.select()
            self.labelMerchandise.deselect()
        elif self.labelMerchandise.get() == 'on':
            self.labelCommercial.deselect()
            self.labelMerchandise.select()

        if self.labelHigh.get() == 'on':
            self.labelHigh.select()
            self.labelMedium.deselect()
            self.labelLow.deselect()
        elif self.labelMedium.get() == 'on':
            self.labelMedium.select()
            self.labelHigh.deselect()
            self.labelLow.deselect()
        elif self.labelLow.get() == 'on':
            self.labelLow.select()
            self.labelHigh.deselect()
            self.labelMedium.deselect()


    def sendForm(self):
        airplaneAirline = self.entryAirline.get()
        if self.labelCommercial.get() == 'on':
            airplaneType = SpotType.COMMERCIAL
        elif self.labelMerchandise.get() == 'on':
            airplaneType = SpotType.MERCHANDISE
        else:
            airplaneType = ''
        if self.labelLow.get() == 'on':
            priority = Priority.LOW
        elif self.labelMedium.get() == 'on':
            priority = Priority.MEDIUM
        elif self.labelHigh.get() == 'on':
            priority = Priority.HIGH
        else:
            priority = ''
        airplaneOrigin = self.entryOrigin.get()
        airplaneDestiny = self.entryDestiny.get()
        airplaneDate = self.entryDate.get()
        airplaneTime = self.entryTime.get()
        airplaneStatus = StatusType.IN_STATION #StatusType.PARKED
        
        # TODO: Send the form data to a server or do something else with it
        
        self.destroy()
