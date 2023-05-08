from GlobalTypes.Types import DashboardAirplaneMessageType, StatusType

class AirplaneInfo():
    def __init__(self,id,status:StatusType,airlineID:str) -> None:
        self.id = id 
        self.status = status
        self.airlineID = airlineID

class DashboardAirplaneMessage():
    def __init__(
            self,
            type:DashboardAirplaneMessageType,
            airplaneInfo:AirplaneInfo=None,
            ) -> None:
        self.type:DashboardAirplaneMessageType = type 

        # This object will be active when type is INFO
        self.airplaneInfo:AirplaneInfo = airplaneInfo 