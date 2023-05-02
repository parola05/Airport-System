from spade import Agent
from typing import Dict, List
import sys 
import platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")
    
from MessagesProtocol.RequestFromAirplane import RequestFromAirplane

class ControlTower(Agent):
    async def setup(self):
        self.queueInTheAir: Dict[str:List[RequestFromAirplane]] 

    '''
    def addRunway(self, runway: Runway):
        if runway.id in self.runways:
            raise ValueError("This identifier was already taken by another runway")
        self.runways[runway.id] = runway
    '''