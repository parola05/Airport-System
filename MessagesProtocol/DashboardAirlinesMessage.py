from GlobalTypes.Types import DashboardAirlineMessageType, NegotiationStatus

class AirlineInfo():
    def __init__(self,id,nSpotsCommercial,nSpotsMerchandise) -> None:
        self.id = id 
        self.nSpotsCommercial = nSpotsCommercial,
        self.nSpotsMerchandise = nSpotsMerchandise

class DashboardAirlinesMessage():
    def __init__(
            self,
            type:DashboardAirlineMessageType,
            negotiationText:str=None,
            airlineInfo:AirlineInfo=None,
            negotiationStatus:NegotiationStatus=None,
            ) -> None:
        self.type: DashboardAirlineMessageType = type 

        # This variable will be active when type is NEGOTIATION
        self.negotiationtext = negotiationText

        # This variable will be active when type is NEGOTIATION
        self.negotiationStatus = negotiationStatus

        # This variable will be active when type is INFO
        self.airlineInfo:AirlineInfo = airlineInfo 