import sys
import platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")
    
from Agents.Agents import Agents

class AirlinesComponentController():
    def __init__(self) -> None:
        '''
            Get Airlines from Agents Singleton
        '''
        self.airlines = Agents().airlines

    def getAirlines(self):
        return [
            {"id":"Indigo Airlines"},
            {"id":"Air India"},
            {"id":"AirAsia India"},
            {"id":"Vistara"},
            {"id":"SpiceJet"}
        ]