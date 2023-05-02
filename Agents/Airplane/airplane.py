import uuid, datetime
from spade import agent
from GlobalTypes.Types import SpotType, StatusType, Priority

class AirplaneAgent(agent.Agent):

    id : str = ""
    airline : str = ""              # tap, ryanair
    typeTransport : SpotType
    origin : str = ""
    destination : str = ""
    date : datetime.date
    time : datetime.time
    status : StatusType
    priority : Priority

    def __init__(self, jid, password, airline, typeTransport, origin, destination, date, time, priority):
        super.__init__(jid,password)
        self.id = str(uuid.uuid4())
        self.airline = airline
        self.typeTransport = typeTransport
        self.origin = origin
        self.destination = destination
        self.date = date
        self.time = time
        self.priority = priority
    
    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
