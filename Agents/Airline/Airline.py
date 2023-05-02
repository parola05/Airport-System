from spade import Agent
import sys, platform

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from GlobalTypes.Types import SpotType

class Airline(Agent):
    async def setup(self,id):
        self.id = id