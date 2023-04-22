import uuid
import datetime
from spade import agent


class AirplaneAgent(agent.Agent):

    id : str = ""
    airline : str = ""              # tap, ryanair
    typeTransport : str = ""        # merchandise, commercial
    origin : str = ""
    destination : str = ""
    date : datetime.date
    time: datetime.time

    def __init__(self, jid, password, airline, typeTransport, origin, destination, date, time):
        super.__init__(jid,password)
        self.id = str(uuid.uuid4())
        self.airline = airline
        self.typeTransport = typeTransport
        self.origin = origin
        self.destination = destination
        self.date = date
        self.time = time
    
    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")