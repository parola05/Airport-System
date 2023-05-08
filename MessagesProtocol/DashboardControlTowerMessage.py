from GlobalTypes.Types import DashboardControlTowerMessageType, RequestType

class DashboardControlTowerMessage():
    def __init__(
            self,
            type:DashboardControlTowerMessageType,
            requestText:str=None,
            requestType:RequestType=None,
            ) -> None:
        
        self.type: DashboardControlTowerMessageType = type 

        # This variable will be active when type is UPDATE
        self.requestText = requestText
        # This variable will be active when type is UPDATE
        self.requestType:RequestType = requestType