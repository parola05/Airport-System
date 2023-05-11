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
from MessagesProtocol.DashboardRunwayMessage import DashboardRunwayMessage, DashboardRunwayMessageType, RunwayInfo
from Conf import Conf

class UpdateRunwayAvailabilityBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("[RunwayManager] Starting UpdateRunwayAvailabilityBehaviour")

    async def run(self):
        msg = await self.receive(timeout=100) 

        if msg:
            runwayInfo:IsRunwayAvailable = jsonpickle.decode(msg.body)
            self.agent.updateRunwayAvailability(runwayInfo.isAvailable, runwayInfo.runway.id)
            
            ############ Update Dashboard ############
            msg = Message(to="dashboardRunway@" + Conf().get_openfire_server())
            msg.set_metadata("performative", "inform")
            bodyMessage:DashboardRunwayMessage = DashboardRunwayMessage(
                type=DashboardRunwayMessageType.UPDATE,
                runwayToUpdate=RunwayInfo(
                    id=runwayInfo.runway.id,
                    coord=runwayInfo.runway.coord,
                    available=runwayInfo.runway.available
                )
            )
            msg.body = jsonpickle.encode(bodyMessage)
            await self.send(msg)

        else:
            print("Agent {}".format(str(self.agent.jid)) + " did not received any message after 10 seconds")