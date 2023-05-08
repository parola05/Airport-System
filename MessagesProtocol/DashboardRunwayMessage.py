from typing import List
from GlobalTypes.Types import DashboardRunwayMessageType

class DashboardRunwayMessage():
    def __init__(self,type:DashboardRunwayMessageType) -> None:
        self.type = type

        # This list will be active when type is INFO
        self.runways:List[RunwayInfo] = []

# Object sended when type is INFO
class RunwayInfo():
    def __init__(self,id,coord,available) -> None:
        self.id = id 
        self.coord = coord
        self.available = available