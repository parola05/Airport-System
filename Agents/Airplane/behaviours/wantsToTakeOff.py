from spade.behaviour import OneShotBehaviour
from spade.message import Message

import sys, platform, datetime, jsonpickle

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from Airplane.Airplane import AirplaneAgent
from MessagesProtocol.RequestFromAirplane import RequestFromAirplane
from GlobalTypes.Types import RequestType
from Conf import Conf

class WantsToTakeOffBehaviour(OneShotBehaviour):

    async def on_start(self):
        print("[Airplane] starting WantsToTakeOffBehaviour")

    async def run(self):
        msg = Message(to="controlTower@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "request")

        requestToTakeOff = RequestFromAirplane(
            typeRequest=RequestType.TAKEOFF,
            id=self.agent.id,
            spotType=self.agent.typeTransport,
            airlineID=self.agent.airline,
            requestTime=datetime.now(), 
            priority=self.agent.priority,
        )
        msg.body = jsonpickle.encode(requestToTakeOff)

        await self.send(msg)