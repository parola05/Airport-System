from spade import Agent
from typing import Dict, List
import sys, platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")
    
from MessagesProtocol.RequestFromAirplane import RequestFromAirplane

class ControlTower(Agent):

    def __init__(self, queueInTheAir, requestsInProcess):
        self.queueInTheAir = queueInTheAir
        self.requestsInProcess = requestsInProcess

    async def setup(self):
        self.queueInTheAir: Dict[str:List[RequestFromAirplane]]
        self.requestsInProcess: Dict[str:RequestFromAirplane] # sender_name : RequestFromAirplane