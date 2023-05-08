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
from MessagesProtocol.RunwayAvailable import RunwayAvailable
from typing import List
from spade.message import Message

class ReceiveSpotQueryBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("[RunwayManager] Starting Receive Spot Query Behaviour")
        with open("output.txt", "w") as f:
            print("[RUNWAY] Starting Receive Spot Query Behaviour", file=f)

    async def run(self):
        msg = await self.receive(timeout=100) 

        if msg:
            runwayAvailableMsg:RunwayAvailable = jsonpickle.decode(msg.body)
            runwaysAvailable:List[str] = self.agent.getRunwaysAvailable()
            if len(runwaysAvailable) != 0:
                #replyMsg = Message(to=self.get("control_tower_jid"))
                #replyMsg.set_metadata("performative","confirm")
                #replyMsg.body = jsonpickle.encode(runwaysAvailable)
                #self.send(replyMsg)
                print("Existem pistas disponíveis!")
            else:
                #replyMsg = Message(to=self.get("control_tower_jid"))
                #replyMsg.set_metadata("performative","refuse")
                #replyMsg.body = "No runways available"
                #self.send(replyMsg)
                print("Não existem pistas disponíveis!")
        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")