from GlobalTypes.Types import DashboardStationMessageType

class DashboardStationMessage():
    def __init__(self,type:DashboardStationMessageType,stationToUpdate=None) -> None:
        self.type:DashboardStationMessageType = type 
        # This list will be active when type is INFO
        self.stations = []
        # This object will be active when type is UPDATE
        self.stationToUpdate:StationInfo = stationToUpdate

class StationInfo():
    def __init__(self,id,merchandise_capacity=None,commercial_capacity=None,merchandise_available=None,commercial_available=None) -> None:
        self.id = id 
        self.merchandise_capacity = merchandise_capacity
        self.commercial_capacity = commercial_capacity
        self.merchandise_available = merchandise_available 
        self.commercial_available = commercial_available