from spade.behaviour import CyclicBehaviour
import jsonpickle, sys, platform
if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
    sys.path.append("../../")
elif platform.system() == "Windows":
    sys.path.append("..") 
    sys.path.append("..\\..") 
else:
    print("Unsupported operating system")
from MessagesProtocol.RequestFromAirplane import RequestFromAirplane
from typing import List
from spade.message import Message
from Conf import Conf

class ReceiveSpotQueryBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("[RunwayManager] Starting ReceiveSpotQueryBehaviour")

    async def run(self):
        msg = await self.receive(timeout=100) 

        if msg:
            requestFromAirplane:RequestFromAirplane = jsonpickle.decode(msg.body)
            runwaysAvailable = self.agent.getRunwaysAvailable()
            if len(runwaysAvailable) != 0:
                replyMsg = Message(to="controlTower@" + Conf().get_openfire_server())
                replyMsg.set_metadata("performative","confirm")
                replyMsg.body = jsonpickle.encode((requestFromAirplane.id, runwaysAvailable))
                await self.send(replyMsg)
            else:
                replyMsg = Message(to="controlTower@" + Conf().get_openfire_server())
                replyMsg.set_metadata("performative","refuse")
                replyMsg.body = jsonpickle.encode(requestFromAirplane)
                await self.send(replyMsg)
        else:
            print("Agent {} ".format(str(self.agent.jid)) + " did not received any message after 10 seconds")