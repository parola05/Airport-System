from spade.behaviour import OneShotBehaviour
from spade.message import Message
from datetime import datetime, timedelta
import sys, platform, jsonpickle
from Conf import Conf
from GlobalTypes.Types import RequestType

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from MessagesProtocol.RequestFromAirplane import RequestFromAirplane
from MessagesProtocol.DashboardAirplaneMessage import DashboardAirplaneMessage, DashboardAirplaneMessageType, AirplaneInfo

class WantsToLandBehaviour(OneShotBehaviour):
    async def on_start(self):
        print("[Airplane] starting WantsToLandBehaviour")

    async def run(self):
        msg = Message(to="controlTower@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "request")

        requestToLand = RequestFromAirplane(
            typeRequest=RequestType.LAND,
            id=self.agent.airplaneID, 
            spotType=self.agent.typeTransport,
            status=self.agent.status,
            airlineID=self.agent.airline,
            requestTime=datetime.now(), 
            priority=self.agent.priority
        )
        msg.body = jsonpickle.encode(requestToLand)
        await self.send(msg)

        ############ Update Dashboard ############
        msg = Message(to="dashboardAirplane@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "inform")
        bodyMessage:DashboardAirplaneMessage = DashboardAirplaneMessage(
            type=DashboardAirplaneMessageType.UPDATE,
            airplaneInfo=AirplaneInfo(
                id=self.agent.airplaneID,
                status=self.agent.status,
                airlineID=self.agent.airline,
            )
        )
        msg.body = jsonpickle.encode(bodyMessage)
        await self.send(msg)