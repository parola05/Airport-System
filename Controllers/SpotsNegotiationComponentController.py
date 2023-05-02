import sys, platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from Agents.Agents import Agents

class SpotsNegotiationComponentController():
    def __init__(self) -> None:
        '''
            Get Stations from Agents Singleton
        '''
        self.stationManager = Agents().stationManager