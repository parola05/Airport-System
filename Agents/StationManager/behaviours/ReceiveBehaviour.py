from spade.behaviour import CyclicBehaviour
import jsonpickle
import sys 
sys.path.append("..\\..")
from MessagesProtocol import StationAvailable
from typing import List
from spade.message import Message

class ReceiveBehaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1) 

        if msg:
            performative = msg.get_metadata('performative')
            if performative == 'query-if':
                stationAvailableMsg:StationAvailable = jsonpickle.decode(msg.body)
                stationsAvailable:List[str] = self.agent.getStationsAvailable(stationAvailableMsg.spotType,stationAvailableMsg.airline_name)
                if len(stationsAvailable) != 0:
                    replyMsg = Message(to=self.get("control_tower_jid"))
                    replyMsg.set_metadata("performative","confirm")
                    replyMsg.body = jsonpickle.encode(stationsAvailable)
                    self.send(replyMsg)
                else:
                    replyMsg = Message(to=self.get("control_tower_jid"))
                    replyMsg.set_metadata("performative","inform")
                    replyMsg.body = "No stations available"
                    self.send(replyMsg)
        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")