from spade import Agent
import sys
sys.path.append("..\\..")
from GlobalTypes import SpotType

class Airline(Agent):
    async def setup(self,id):
        self.id = id