import uuid, datetime, random, json
from spade import agent
from GlobalTypes.Types import SpotType, StatusType, Priority

class AirplaneAgent(agent.Agent):

    id : str = ""
    airline : str = ""              # tap, ryanair
    typeTransport : SpotType
    origin : str = ""
    destination : str = ""
    datetime : datetime.datetime
    status : StatusType
    priority : Priority

    def __init__(self, jid, password, id, airline, typeTransport, origin, destination, datetime, priority):
        super.__init__(jid,password)
        self.id = id
        self.airline = airline
        self.typeTransport = typeTransport
        self.origin = origin
        self.destination = destination
        self.datetime = datetime
        self.priority = priority

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")

    def getRandomTypeTransport():
        random = random.randint(0,9)
        if random % 2 == 0:
            return SpotType.COMMERCIAL
        else:
            return SpotType.MERCHANDISE
        
    def getRandomPriority():
        random = random.randint(0,15)
        if random % 3 == 0:
            return Priority.LOW
        elif random % 2 == 0:
            return Priority.MEDIUM
        else:
            return Priority.HIGH
    
    def getRandomOrigin(self, cities):
        return random.choice(cities)

    def getRandomDestiny(self, cities, origin):
        return random.choice(cities.remove(origin))
