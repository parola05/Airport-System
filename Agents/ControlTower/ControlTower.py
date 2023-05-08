from spade.agent import Agent
from typing import Dict, List
import sys, platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")
    
from MessagesProtocol.RequestFromAirplane import RequestFromAirplane
from .behaviours.ReceiveBehaviour import ReceiveBehaviour

class ControlTower(Agent):
    def __init__(self,agent_name,password,queueInTheAirMaxSize=30):
        super().__init__(agent_name,password)
        self.queueInTheAir: Dict[str:List[RequestFromAirplane]] = {}
        self.requestsInProcess: Dict[str:RequestFromAirplane] = {}  # sender_name : RequestFromAirplane
        self.queueInTheAirMaxSize = queueInTheAirMaxSize

    async def setup(self): 
        receiveBehaviour:ReceiveBehaviour = ReceiveBehaviour()
        self.add_behaviour(receiveBehaviour)