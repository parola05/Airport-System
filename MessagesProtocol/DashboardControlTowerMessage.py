from GlobalTypes.Types import DashboardControlTowerMessageType, RequestType, StatusType

class DashboardControlTowerMessage():
    def __init__(
            self,
            type:DashboardControlTowerMessageType,
            requestText:str=None,
            requestType:RequestType=None,
            informStatus:StatusType=None,
            permissionText:str=None,
            newSpotsText:str=None,
            avgTimeInQueue:float=None
            ) -> None:
        
        self.type: DashboardControlTowerMessageType = type 

        # These variables will be active when type is UPDATE
        self.requestText = requestText
        self.requestType:RequestType = requestType
        self.informStatus:StatusType = informStatus
        self.permissionText:permissionText = permissionText
        self.newSpotsText:str = newSpotsText
        self.avgTimeInQueue:float = avgTimeInQueue