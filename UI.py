import customtkinter
from Agents.Dashboard.DashboardStation.DashboardStation import DashboardStation
from Agents.Dashboard.DashboardAirline.DashboardAirline import DashboardAirline
from Agents.Dashboard.DashboardRunway.DashboardRunway import DashboardRunway
from Agents.Dashboard.DashboardAirplane.DashboardAirplane import DashboardAirplane
from Agents.Airport import Airport

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

        self.sidebar_automatic = customtkinter.CTkButton(self.sidebar_frame, command=self.openAutomaticSimulation)
        self.sidebar_automatic.grid(row=4, column=0, padx=20, pady=10)
        self.sidebar_automatic.configure(text="Configure Simulation")

        self.sidebar_automatic = customtkinter.CTkButton(self.sidebar_frame, command=self.simulate)
        self.sidebar_automatic.grid(row=5, column=0, padx=20, pady=10)
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
        self.dashboardStation = DashboardStation("dashboardStation@laptop-vun6ls3v.lan","12345678",master=self)
        self.dashboardStation.view.grid(row=2, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.dashboardStation.view.grid_columnconfigure(0, weight=1)
        self.dashboardStation.view.grid_rowconfigure(1, weight=1)
        self.dashboardStation.start()

        # Airlines Component
        self.dashboardAirline = DashboardAirline("dashboardAirline@laptop-vun6ls3v.lan","12345678",master=self)
        self.dashboardAirline.view.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.dashboardAirline.start()

        # Airplanes Component
        self.airplanesComponent = DashboardAirplane("dashboardAirplane@laptop-vun6ls3v.lan","12345678",master=self)
        self.airplanesComponent.view.grid(row=2, column=1, padx=20, pady=(20, 0), sticky="nsew")
        self.airplanesComponent.view.grid_columnconfigure(0, weight=1)
        self.airplanesComponent.view.grid_rowconfigure(1, weight=1)

        # Runway Component
        self.runwayComponent = DashboardRunway("dashboardRunway@laptop-vun6ls3v.lan","12345678",master=self)
        self.runwayComponent.view.grid(row=2, column=2, padx=20, pady=(20, 0), sticky="nsew")
        self.runwayComponent.view.grid_columnconfigure(0, weight=1)
        self.runwayComponent.view.grid_rowconfigure(1, weight=1)

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

    def openAutomaticSimulation(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CreateAutomaticSimulationView(self)  
        else:
            self.toplevel_window.focus()  

    def simulate(self):
        airport = Airport()
        airport.simulate() 

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

class CreateAutomaticSimulationView(customtkinter.CTkToplevel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Automatic Simulation")
        self.geometry(f"{1000}x{800}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)

        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        self.seg_button_1.set("Value 2")

        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")

        self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

        self.slider_1.configure(command=self.progressbar_2.set)
        self.slider_2.configure(command=self.progressbar_3.set)

        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()