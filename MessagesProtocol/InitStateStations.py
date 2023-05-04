class InitStateStations():
    def __init__(self) -> None:
        self.stations = []

class StationInfo():
    def __init__(self,id,merchandise_capacity,commercial_capacity) -> None:
        self.id = id 
        self.merchandise_capacity = merchandise_capacity
        self.commercial_capacity = commercial_capacity