#from .StationManager.StationManager import StationManagerAgent
#from .RunwayManager.RunwayManager import RunwayManagerAgent

class Agents():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        '''
            init all agents of the system
        '''
        #self.stationManager = StationManagerAgent()
        self.stationManager = None
        #self.runwayManager = RunwayManagerAgent()
        self.runwayManager = None
        self.airplaines = []
        # TODO: init rest of agents
        # self.airplaines = []
        # self.airlines = []
        # self.controlTower = ControlTower()