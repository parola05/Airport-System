from spade.behaviour import OneShotBehaviour
from spade.message import Message

class WantsToLandBehaviour(OneShotBehaviour):

    async def on_start(self):
        pass

    async def run(self):
        msg = Message(to=self.get("control_tower_jid"))
        msg.set_metadata("performative", "request")
        msg.body = "Requesting to land"

        await self.send(msg)