from GlobalTypes.Types import DashboardAirlineUpdate

class AirlineInfo():
    def __init__(self,id) -> None:
        self.id = id 

class DashboardAirlines():
    def __init__(self,type:DashboardAirlineUpdate,negotiationText:str=None,airlineInfo:AirlineInfo=None) -> None:
        self.type: DashboardAirlineUpdate = type 
        self.negotiationtext = negotiationText
        self.airlineInfo:AirlineInfo = airlineInfo 