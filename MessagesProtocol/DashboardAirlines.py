from GlobalTypes.Types import DashboardAirlineUpdate, NegotiationStatus, SpotType

class AirlineInfo():
    def __init__(self,id,nSpotsCommercial,nSpotsMerchandise) -> None:
        self.id = id 
        self.nSpotsCommercial = nSpotsCommercial,
        self.nSpotsMerchandise = nSpotsMerchandise

class DashboardAirlines():
    def __init__(
            self,
            type:DashboardAirlineUpdate,
            negotiationText:str=None,
            airlineInfo:AirlineInfo=None,
            negotiationStatus:NegotiationStatus=None,
            ) -> None:
        self.type: DashboardAirlineUpdate = type 
        self.negotiationtext = negotiationText
        self.negotiationStatus = negotiationStatus
        self.airlineInfo:AirlineInfo = airlineInfo 