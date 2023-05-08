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
from MessagesProtocol.StationAvailable import StationAvailable

class ReceiveSpotQueryBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("[StationManager] Starting ReceiveSpotQueryBehaviour")

    async def run(self):
        msg = await self.receive(timeout=100) 

        if msg:
            stationAvailableMsg:StationAvailable = jsonpickle.decode(msg.body)
            stationsAvailable:List[str] = self.agent.getStationsAvailable(stationAvailableMsg.spotType,stationAvailableMsg.airline_name)
            if len(stationsAvailable) != 0:
                #replyMsg = Message(to=self.get("control_tower_jid"))
                #replyMsg.set_metadata("performative","confirm")
                #replyMsg.body = jsonpickle.encode(stationsAvailable)
                #self.send(replyMsg)
                print("Há lugar na station!")
            else:
                #replyMsg = Message(to=self.get("control_tower_jid"))
                #replyMsg.set_metadata("performative","refuse")
                #replyMsg.body = "No stations available"
                #self.send(replyMsg)
                print("Não há lugar na station")
        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")