import customtkinter
from Agents.Dashboard.DashboardStation.DashboardStation import DashboardStation
from Agents.Dashboard.DashboardAirline.DashboardAirline import DashboardAirline
from Agents.Dashboard.DashboardRunway.DashboardRunway import DashboardRunway
from Agents.Dashboard.DashboardAirplane.DashboardAirplane import DashboardAirplane
from Agents.Airport import Airport
from Conf import Conf

customtkinter.set_appearance_mode("System") 
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
        self.grid_rowconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_rowconfigure((2), weight=3)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Simulation", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_automatic = customtkinter.CTkButton(self.sidebar_frame, command=self.openConfigureSimulation)
        self.sidebar_automatic.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_automatic.configure(text="Configure Simulation")

        self.sidebar_automatic = customtkinter.CTkButton(self.sidebar_frame, command=self.simulate)
        self.sidebar_automatic.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_automatic.configure(text="Start Simulation")

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

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
        self.dashboardAirline.start()

        # Airplanes Component
        self.airplanesComponent = DashboardAirplane("dashboardAirplane@" + Conf().get_openfire_server(),Conf().get_openfire_password(),master=self)
        self.airplanesComponent.view.grid(row=2, column=1, padx=20, pady=(20, 0), sticky="nsew")
        self.airplanesComponent.view.grid_columnconfigure(0, weight=1)
        self.airplanesComponent.view.grid_rowconfigure(1, weight=1)

        # Runway Component
        self.runwayComponent = DashboardRunway("dashboardRunway@" + Conf().get_openfire_server(),Conf().get_openfire_password(),master=self)
        self.runwayComponent.view.grid(row=2, column=2, padx=20, pady=(20, 0), sticky="nsew")
        self.runwayComponent.view.grid_columnconfigure(0, weight=1)
        self.runwayComponent.view.grid_rowconfigure(1, weight=1)

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

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
        self.geometry(f"{600}x{600}")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.saveButton = customtkinter.CTkButton(self, command=self.save)
        self.saveButton.grid(row=4, column=0, padx=20, pady=10)
        self.saveButton.configure(text="Save")

        ################ Number of Stations ##################

        self.nStationsFrame = customtkinter.CTkFrame(master=self)
        self.nStationsFrame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.nStationsLabel = customtkinter.CTkLabel(self.nStationsFrame, text="Number of Stations", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.nStationsLabel.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.nStationsSelectedLabel = customtkinter.CTkLabel(self.nStationsFrame, text="0", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.nStationsSelectedLabel.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))

        self.nStations = customtkinter.CTkSlider(self.nStationsFrame, from_=1, to=10, number_of_steps=10)
        self.nStations.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")

        ################ Merchandise Spots ##################

        self.nMerchandiseSpotsPerStationFrame = customtkinter.CTkFrame(master=self)
        self.nMerchandiseSpotsPerStationFrame.grid(row=1, column=0, padx=(10, 10), pady=(10, 10))

        self.nMerchandiseSpotsPerStationLabel = customtkinter.CTkLabel(self.nMerchandiseSpotsPerStationFrame, text="Number of Merchandise Spots per Station", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.nMerchandiseSpotsPerStationLabel.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.nMerchandiseSpotsPerStationSelectedLabel = customtkinter.CTkLabel(self.nMerchandiseSpotsPerStationFrame, text="0", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.nMerchandiseSpotsPerStationSelectedLabel.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))
        
        self.nMerchandiseSpotsPerStation = customtkinter.CTkSlider(self.nMerchandiseSpotsPerStationFrame, from_=10, to=50, number_of_steps=20)
        self.nMerchandiseSpotsPerStation.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")

        ################ Commercial Spots ##################

        self.nCommercialSpotsPerStationFrame = customtkinter.CTkFrame(master=self)
        self.nCommercialSpotsPerStationFrame.grid(row=2, column=0, padx=(10, 10), pady=(10, 10))

        self.nCommercialSpotsPerStationLabel = customtkinter.CTkLabel(self.nCommercialSpotsPerStationFrame, text="Number of Commercial Spots per Station", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.nCommercialSpotsPerStationLabel.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.nCommercialSpotsPerStationSelectedLabel = customtkinter.CTkLabel(self.nCommercialSpotsPerStationFrame, text="0", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.nCommercialSpotsPerStationSelectedLabel.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))

        self.nCommercialSpotsPerStation = customtkinter.CTkSlider(self.nCommercialSpotsPerStationFrame, from_=10, to=50, number_of_steps=20)
        self.nCommercialSpotsPerStation.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")

        ################ Airlines ###########################

        self.nAirlinesFrame = customtkinter.CTkFrame(master=self)
        self.nAirlinesFrame.grid(row=3, column=0, padx=(10, 10), pady=(10, 10))

        self.nAirlinesLabel = customtkinter.CTkLabel(self.nAirlinesFrame, text="Number of Airlines", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.nAirlinesLabel.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.nAirlinesSelectedLabel = customtkinter.CTkLabel(self.nAirlinesFrame, text="0", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.nAirlinesSelectedLabel.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))
        
        self.nAirlines = customtkinter.CTkSlider(self.nAirlinesFrame, from_=1, to=20, number_of_steps=20)
        self.nAirlines.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")

        ############### Callback functions for each slider

        self.nStations.configure(command=self.nStationsUpdate)
        self.nCommercialSpotsPerStation.configure(command=self.nCommercialSpotsPerStationUpdate)
        self.nMerchandiseSpotsPerStation.configure(command=self.nMerchandiseSpotsPerStationUpdate)
        self.nAirlines.configure(command=self.nAirlinesUpdate)

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

    def save(self):
        # Instantiate airport with configuration values
        airport = Airport(
            nStations=int(self.nStations.get()),
            nMerchandiseSpotsPerStation=int(self.nMerchandiseSpotsPerStation.get()),
            nCommercialSpotsPerStation=int(self.nCommercialSpotsPerStation.get()),
            nAirlines=int(self.nAirlines.get())
        )
        print("Saved!")