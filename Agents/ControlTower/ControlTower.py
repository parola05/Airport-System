from spade import Agent
from typing import Dict, List

class ControlTower(Agent):
    async def setup(self):
        #self.queueInTheAir: Dict[str:AirplaneRequest] 

    def addRunway(self, runway: Runway):
        if runway.id in self.runways:
            raise ValueError("This identifier was already taken by another runway")
        self.runways[runway.id] = runway