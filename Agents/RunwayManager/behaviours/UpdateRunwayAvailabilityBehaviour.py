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

from MessagesProtocol.IsRunwayAvailable import IsRunwayAvailable
from MessagesProtocol.DashboardRunwayMessage import DashboardRunwayMessage, DashboardRunwayMessageType
from Conf import Conf

class UpdateRunwayAvailabilityBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("[RunwayManager] Starting UpdateRunwayAvailabilityBehaviour")

    async def run(self):
        msg = await self.receive(timeout=100) 

        if msg:
            runwayInfo:IsRunwayAvailable = jsonpickle.decode(msg.body)
            self.agent.updateRunwayAvailability(runwayInfo.isAvailable, runwayInfo.runway.id)

        else:
            print("Agent {}".format(str(self.agent.jid)) + " did not received any message after 10 seconds")