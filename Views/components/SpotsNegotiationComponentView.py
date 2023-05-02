import customtkinter
import sys
import platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")
    
from Controllers.SpotsNegotiationComponentController import SpotsNegotiationComponentController

class SpotsNegotiationComponentView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.controller = SpotsNegotiationComponentController()

        self.grid_columnconfigure(1, weight=6)
        self.grid_columnconfigure(0, weight=2)

        labelTimer = customtkinter.CTkLabel(master=self, text="00:01",font=("Helvetica", 28, "bold"))
        labelTimer.grid(row=1, column=0,padx=2,pady=2,sticky="nw")

        progressbar = customtkinter.CTkProgressBar(master=self)
        progressbar.grid(row=0, column=1, padx=2, pady=2, sticky="ew")
        progressbar.configure(mode="indeterminnate")
        progressbar.start()

        textbox = customtkinter.CTkTextbox(master=self)
        textbox.grid(row=1,column=1,sticky="nsew")

        textbox.insert("0.0", "Station: receive propose from TAP\n") 
        textbox.insert("1.0", "Station: receive propose from TAP\n") 
        textbox.insert("2.0", "Station: receive propose from TAP\n") 
        textbox.insert("3.0", "Station: receive propose from TAP\n") 
        textbox.insert("4.0", "Station: receive propose from TAP\n") 
        textbox.insert("5.0", "Station: receive propose from TAP\n") 
        textbox.insert("6.0", "Station: receive propose from TAP\n") 
        textbox.insert("7.0", "Station: receive propose from TAP") 
