from spade.behaviour import OneShotBehaviour
from spade.message import Message
from datetime import datetime, timedelta
import sys, platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from MessagesProtocol.RequestFromAirplane import RequestFromAirplane

class WantsToLandBehaviour(OneShotBehaviour):

    async def on_start(self):
        pass

    async def run(self):
        msg = Message(to=self.get("control_tower_jid"))
        msg.set_metadata("performative", "request")
        now = datetime.now()

        requestToLand = RequestFromAirplane(1, self.agent.id, self.agent.typeTransport, self.agent.airline, now, self.agent.priority, None, None)
        msg.body = requestToLand

        await self.send(msg)

