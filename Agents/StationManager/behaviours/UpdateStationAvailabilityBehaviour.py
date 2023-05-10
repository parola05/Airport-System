from spade.behaviour import CyclicBehaviour
from typing import List
from spade.message import Message
import sys, jsonpickle, platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
    sys.path.append("../../")
elif platform.system() == "Windows":
    sys.path.append("..") 
    sys.path.append("..\\..") 
else:
    print("Unsupported operating system")

from MessagesProtocol.IsStationAvailable import IsStationAvailable

class UpdateStationAvailabilityBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("[StationManager] Starting UpdateStationAvailabilityBehaviour")

    async def run(self):
        msg = await self.receive(timeout=100) 

        if msg:
            stationInfo:IsStationAvailable = jsonpickle.decode(msg.body)
            self.agent.updateStationSpots(stationInfo.isAvailable, stationInfo.station.id, stationInfo.spotType)
        
        else:
            print("Agent {}".format(str(self.agent.jid)) + " did not received any message after 10 seconds")