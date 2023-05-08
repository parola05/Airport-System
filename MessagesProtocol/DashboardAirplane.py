from GlobalTypes.Types import DashboardAirplaneUpdate, StatusType

class AirplaneInfo():
    def __init__(self,id,status:StatusType,airlineID:str) -> None:
        self.id = id 
        self.status = status
        self.airlineID = airlineID

class DashboardAirplane():
    def __init__(
            self,
            type:DashboardAirplaneUpdate,
            airplaneInfo:AirplaneInfo=None,
            ) -> None:
        self.type: DashboardAirplaneUpdate = type 
        self.airplaneInfo:AirplaneInfo = airplaneInfo 