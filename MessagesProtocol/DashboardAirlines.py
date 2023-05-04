from GlobalTypes.Types import DashboardAirlineUpdate

class DashboardAirlines():
    def __init__(self,type:DashboardAirlineUpdate,negotiationText:str=None) -> None:
        self.type: DashboardAirlineUpdate = type 
        self.negotiationtext = negotiationText