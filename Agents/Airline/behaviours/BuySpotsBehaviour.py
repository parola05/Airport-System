import sys
sys.path.append("..\\..")
from spade.behaviour import OneShotBehaviour
from MessagesProtocol.BuySpots import BuySpots
from spade.message import Message
import jsonpickle

class BuySpotsBehaviour(OneShotBehaviour):
    async def run(self):
        msg = Message(to="TODO")
        msg.set_metadata("performative", "propose")
        bodyMessage:BuySpots = BuySpots() # TODO: specify values from tkinter form
        msg.body = jsonpickle.encode(bodyMessage)
        await self.send(msg)