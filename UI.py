import customtkinter
from Agents.Dashboard.DashboardStation.DashboardStation import DashboardStation
from Agents.Dashboard.DashboardAirline.DashboardAirline import DashboardAirline
from Agents.Dashboard.DashboardRunway.DashboardRunway import DashboardRunway
from Agents.Dashboard.DashboardAirplane.DashboardAirplane import DashboardAirplane
from Agents.Dashboard.DashboardControlTower.DashboardControlTower import DashboardControlTower
from Agents.Airport import Airport
from Conf import Conf

customtkinter.set_appearance_mode("Dark") 
customtkinter.set_default_color_theme("green")

class UI():
    def __init__(self):
        self.app = MainView()

    def start(self):
        self.app.mainloop()
        
class MainView(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.toplevel_window = None

        # configure window
        self.title("Airport System")
        self.geometry(f"{1400}x{780}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_rowconfigure((2), weight=3)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        self.sidebar_frame.grid_rowconfigure((0,1,3,4,5), weight=1)
        self.sidebar_frame.grid_rowconfigure((2,), weight=2)
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Simulation", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.buttonsFrame = customtkinter.CTkFrame(self.sidebar_frame, width=120, corner_radius=0,fg_color="transparent")
        self.buttonsFrame.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_automatic = customtkinter.CTkButton(self.buttonsFrame, command=self.openConfigureSimulation)
        self.sidebar_automatic.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_automatic.configure(text="Configure Simulation")

        self.sidebar_automatic = customtkinter.CTkButton(self.buttonsFrame, command=self.simulate)
        self.sidebar_automatic.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_automatic.configure(text="Start Simulation")

        '''
        self.conf_valuesFrame = customtkinter.CTkFrame(self.sidebar_frame, width=120, corner_radius=0)
        self.conf_valuesFrame.grid(row=3, column=0, padx=20, pady=10)
        self.nAirplanesToLandValue = customtkinter.CTkLabel(self.conf_valuesFrame, text="Nº Airplanes to land:")
        self.nAirplanesToLandValue.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.nAirplanesToTakeOffValue = customtkinter.CTkLabel(self.conf_valuesFrame, text="Nº Airplanes to take-off:")
        self.nAirplanesToTakeOffValue.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.nCirculationTimeValue = customtkinter.CTkLabel(self.conf_valuesFrame, text="Circulation Time in Runway:")
        self.nCirculationTimeValue.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.nRunwaysValue = customtkinter.CTkLabel(self.conf_valuesFrame, text="Nº Runways:")
        self.nRunwaysValue.grid(row=3, column=0, padx=20, pady=(10, 0))
        '''
        
        self.appearanceFrame = customtkinter.CTkFrame(self.sidebar_frame, width=120, corner_radius=0,fg_color="transparent")
        self.appearanceFrame.grid(row=4, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.appearanceFrame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.appearanceFrame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.scaleFrame = customtkinter.CTkFrame(self.sidebar_frame, width=120, corner_radius=0,fg_color="transparent")
        self.scaleFrame.grid(row=5, column=0, padx=20, pady=10)
        self.scaling_label = customtkinter.CTkLabel(self.scaleFrame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.scaleFrame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=1, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.bottomFrame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.bottomFrame.grid(row=3, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.label = customtkinter.CTkLabel(self.bottomFrame, text="👥 Criado por Ana Henriques e Henrique Parola", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Station Component
        self.dashboardStation = DashboardStation("dashboardStation@" + Conf().get_openfire_server(),Conf().get_openfire_password(),master=self)
        self.dashboardStation.view.grid(row=2, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.dashboardStation.view.grid_columnconfigure(0, weight=1)
        self.dashboardStation.view.grid_rowconfigure(1, weight=1)
        future = self.dashboardStation.start()
        future.result()

        # Airlines Component
        self.dashboardAirline = DashboardAirline("dashboardAirline@" + Conf().get_openfire_server(),Conf().get_openfire_password(),master=self)
        self.dashboardAirline.view.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        future2 = self.dashboardAirline.start()
        future2.result()

        # Airplanes Component
        self.dashboardAirplane = DashboardAirplane("dashboardAirplane@" + Conf().get_openfire_server(),Conf().get_openfire_password(),master=self)
        self.dashboardAirplane.view.grid(row=2, column=1, padx=20, pady=(20, 0), sticky="nsew")
        self.dashboardAirplane.view.grid_columnconfigure(0, weight=1)
        self.dashboardAirplane.view.grid_rowconfigure(1, weight=1)
        future3 = self.dashboardAirplane.start()
        future3.result()

        # Runway Component
        self.dashboardRunway = DashboardRunway("dashboardRunway@" + Conf().get_openfire_server(),Conf().get_openfire_password(),master=self)
        self.dashboardRunway.view.grid(row=2, column=2, padx=20, pady=(20, 0), sticky="nsew")
        self.dashboardRunway.view.grid_columnconfigure(0, weight=1)
        self.dashboardRunway.view.grid_rowconfigure(1, weight=1)
        future4 = self.dashboardRunway.start()
        future4.result()

        # Control Tower Component
        self.controlTower = DashboardControlTower("dashboardControlTower@" + Conf().get_openfire_server(),Conf().get_openfire_password(),master=self)
        self.controlTower.view.grid(row=0, column=1, padx=20, pady=(20, 0), sticky="nsew", columnspan=2)
        self.controlTower.view.grid_columnconfigure(0, weight=1)
        self.controlTower.view.grid_rowconfigure(1, weight=1)
        future5 = self.controlTower.start()
        future5.result()

        # set default values
        self.appearance_mode_optionemenu.set("Light")
        self.scaling_optionemenu.set("100%")

    def openConfigureSimulation(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ConfigureSimulationView(self)  
        else:
            self.toplevel_window.focus()  

    def simulate(self):
        # With Airport not configured, default values are used. Otherwise the singleton
        # class already being created is used
        airport = Airport._instance
        if airport is not None:
            airport.simulate()
        else:
            Airport().simulate()

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

class ConfigureSimulationView(customtkinter.CTkToplevel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Automatic Simulation")
        self.geometry(f"{700}x{600}")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.saveButton = customtkinter.CTkButton(self, command=self.save)
        self.saveButton.grid(row=0, column=1, padx=20, pady=10,sticky="nsew")
        self.saveButton.configure(text="Save")

        self.titleLabel = customtkinter.CTkLabel(self, text="Airport Configuration", font=customtkinter.CTkFont(size=28, weight="bold"))
        self.titleLabel.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        ################ Number of Stations ##################

        self.nStationsFrame = customtkinter.CTkFrame(master=self)
        self.nStationsFrame.grid(row=1, column=0, padx=(10, 10), pady=(10, 10),sticky="nsew")

        self.nStationsLabel = customtkinter.CTkLabel(self.nStationsFrame, text="Number of Stations", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.nStationsLabel.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.nStationsSelectedLabel = customtkinter.CTkLabel(self.nStationsFrame, text="5", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.nStationsSelectedLabel.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))

        self.nStations = customtkinter.CTkSlider(self.nStationsFrame, from_=1, to=10, number_of_steps=10)
        self.nStations.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")

        ################ Merchandise Spots ##################

        self.nMerchandiseSpotsPerStationFrame = customtkinter.CTkFrame(master=self)
        self.nMerchandiseSpotsPerStationFrame.grid(row=1, column=1, padx=(10, 10), pady=(10, 10),sticky="nsew")

        self.nMerchandiseSpotsPerStationLabel = customtkinter.CTkLabel(self.nMerchandiseSpotsPerStationFrame, text="Number of Merchandise Spots per Station", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.nMerchandiseSpotsPerStationLabel.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.nMerchandiseSpotsPerStationSelectedLabel = customtkinter.CTkLabel(self.nMerchandiseSpotsPerStationFrame, text="30", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.nMerchandiseSpotsPerStationSelectedLabel.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))
        
        self.nMerchandiseSpotsPerStation = customtkinter.CTkSlider(self.nMerchandiseSpotsPerStationFrame, from_=10, to=50, number_of_steps=20)
        self.nMerchandiseSpotsPerStation.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")

        ################ Commercial Spots ###################

        self.nCommercialSpotsPerStationFrame = customtkinter.CTkFrame(master=self)
        self.nCommercialSpotsPerStationFrame.grid(row=2, column=0, padx=(10, 10), pady=(10, 10),sticky="nsew")

        self.nCommercialSpotsPerStationLabel = customtkinter.CTkLabel(self.nCommercialSpotsPerStationFrame, text="Number of Commercial Spots per Station", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.nCommercialSpotsPerStationLabel.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.nCommercialSpotsPerStationSelectedLabel = customtkinter.CTkLabel(self.nCommercialSpotsPerStationFrame, text="30", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.nCommercialSpotsPerStationSelectedLabel.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))

        self.nCommercialSpotsPerStation = customtkinter.CTkSlider(self.nCommercialSpotsPerStationFrame, from_=10, to=50, number_of_steps=20)
        self.nCommercialSpotsPerStation.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")

        ################ Airlines ###########################

        self.nAirlinesFrame = customtkinter.CTkFrame(master=self)
        self.nAirlinesFrame.grid(row=2, column=1, padx=(10, 10), pady=(10, 10),sticky="nsew")

        self.nAirlinesLabel = customtkinter.CTkLabel(self.nAirlinesFrame, text="Number of Airlines", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.nAirlinesLabel.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.nAirlinesSelectedLabel = customtkinter.CTkLabel(self.nAirlinesFrame, text="10", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.nAirlinesSelectedLabel.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))
        
        self.nAirlines = customtkinter.CTkSlider(self.nAirlinesFrame, from_=1, to=20, number_of_steps=20)
        self.nAirlines.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")

        ################ Airplanes to Land ###########################

        self.nAirplanesToLandFrame = customtkinter.CTkFrame(master=self)
        self.nAirplanesToLandFrame.grid(row=3, column=0, padx=(10, 10), pady=(10, 10),sticky="nsew")

        self.nAirplanesToLandLabel = customtkinter.CTkLabel(self.nAirplanesToLandFrame, text="Number of Airplanes to Land", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.nAirplanesToLandLabel.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.nAirplanesToLandSelectedLabel = customtkinter.CTkLabel(self.nAirplanesToLandFrame, text="5", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.nAirplanesToLandSelectedLabel.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))
        
        self.nAirplanesToLand = customtkinter.CTkSlider(self.nAirplanesToLandFrame, from_=1, to=10, number_of_steps=10)
        self.nAirplanesToLand.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")

        ################ Airplanes to Take-off ########################

        self.nAirplanesToTakeOffFrame = customtkinter.CTkFrame(master=self)
        self.nAirplanesToTakeOffFrame.grid(row=3, column=1, padx=(10, 10), pady=(10, 10),sticky="nsew")

        self.nAirplanesToTakeOffLabel = customtkinter.CTkLabel(self.nAirplanesToTakeOffFrame, text="Number of Airplanes to Take-off", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.nAirplanesToTakeOffLabel.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.nAirplanesToTakeOffSelectedLabel = customtkinter.CTkLabel(self.nAirplanesToTakeOffFrame, text="5", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.nAirplanesToTakeOffSelectedLabel.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))
        
        self.nAirplanesToTakeOff = customtkinter.CTkSlider(self.nAirplanesToTakeOffFrame, from_=1, to=10, number_of_steps=10)
        self.nAirplanesToTakeOff.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")

        ################ Runway ###########################

        self.nRunwaysFrame = customtkinter.CTkFrame(master=self)
        self.nRunwaysFrame.grid(row=4, column=0, padx=(10, 10), pady=(10, 10),sticky="nsew")

        self.nRunwaysLabel = customtkinter.CTkLabel(self.nRunwaysFrame, text="Number of Runways", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.nRunwaysLabel.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.nRunwaysSelectedLabel = customtkinter.CTkLabel(self.nRunwaysFrame, text="10", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.nRunwaysSelectedLabel.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))
        
        self.nRunways = customtkinter.CTkSlider(self.nRunwaysFrame, from_=1, to=20, number_of_steps=20)
        self.nRunways.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")

        ############ Queue in the air max size ############

        self.nQueueInTheAirFrame = customtkinter.CTkFrame(master=self)
        self.nQueueInTheAirFrame.grid(row=4, column=1, padx=(10, 10), pady=(10, 10),sticky="nsew")

        self.nQueueInTheAirLabel = customtkinter.CTkLabel(self.nQueueInTheAirFrame, text="Queue In The Air Max size", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.nQueueInTheAirLabel.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.nQueueInTheAirLabel = customtkinter.CTkLabel(self.nQueueInTheAirFrame, text="15", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.nQueueInTheAirLabel.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))
        
        self.nQueueInTheAir = customtkinter.CTkSlider(self.nQueueInTheAirFrame, from_=1, to=30, number_of_steps=30)
        self.nQueueInTheAir.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")


        ############### Callback functions for each slider

        self.nStations.configure(command=self.nStationsUpdate)
        self.nCommercialSpotsPerStation.configure(command=self.nCommercialSpotsPerStationUpdate)
        self.nMerchandiseSpotsPerStation.configure(command=self.nMerchandiseSpotsPerStationUpdate)
        self.nAirlines.configure(command=self.nAirlinesUpdate)
        self.nAirplanesToLand.configure(command=self.nAirplanesToLandUpdate)
        self.nAirplanesToTakeOff.configure(command=self.nAirplanesToTakeOffUpdate)
        self.nRunways.configure(command=self.nRunwaysUpdate)
        self.nQueueInTheAir.configure(command=self.queueInTheAirUpdate)

    def nStationsUpdate(self,value):
        # Update label text
        self.nStationsSelectedLabel.configure(text=str(int(value)))

    def nMerchandiseSpotsPerStationUpdate(self,value):
        # Update label text
        self.nMerchandiseSpotsPerStationSelectedLabel.configure(text=str(int(value)))

    def nCommercialSpotsPerStationUpdate(self,value):
        # Update label text
        self.nCommercialSpotsPerStationSelectedLabel.configure(text=str(int(value)))

    def nAirlinesUpdate(self,value):
        # Update label text
        self.nAirlinesSelectedLabel.configure(text=str(int(value)))

    def nAirplanesToLandUpdate(self,value):
        # Update label text
        self.nAirplanesToLandSelectedLabel.configure(text=str(int(value)))

    def nAirplanesToTakeOffUpdate(self,value):
        # Update label text
        self.nAirplanesToTakeOffSelectedLabel.configure(text=str(int(value)))

    def nRunwaysUpdate(self,value):
        # Update label text
        self.nRunwaysSelectedLabel.configure(text=str(int(value)))

    def queueInTheAirUpdate(self,value):
        # Update label text
        self.nQueueInTheAirLabel.configure(text=str(int(value)))

    def save(self):
        # Instantiate airport with configuration values
        airport = Airport(
            nStations=int(self.nStations.get()),
            nMerchandiseSpotsPerStation=int(self.nMerchandiseSpotsPerStation.get()),
            nCommercialSpotsPerStation=int(self.nCommercialSpotsPerStation.get()),
            nAirlines=int(self.nAirlines.get()),
            nAirplanesToLand=int(self.nAirplanesToLand.get()),
            nAirplanesToTakeOff=int(self.nAirplanesToTakeOff.get()),
            nRunways=int(self.nRunways.get()),
            queueInTheAirMaxSize=int(self.nQueueInTheAir.get())
        )
        self.destroy()