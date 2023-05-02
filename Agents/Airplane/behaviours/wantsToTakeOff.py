from spade.behaviour import OneShotBehaviour
from spade.message import Message

import sys
import platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from Airplane.Airplane import AirplaneAgent
from MessagesProtocol.RequestFromAirplane import RequestFromAirplane

class WantsToTakeOffBehaviour(OneShotBehaviour):

    async def on_start(self):
        pass

    async def run(self):
        msg = Message(to=self.get("control_tower_jid"))
        msg.set_metadata("performative", "request")

        requestToTakeOff = RequestFromAirplane(2, AirplaneAgent.typeTransport, AirplaneAgent.airline, datetime.now(), AirplaneAgent.id, AirplaneAgent.priority)

        msg.body = requestToTakeOff

        await self.send(msg)