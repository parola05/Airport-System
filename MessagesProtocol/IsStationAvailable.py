from GlobalTypes.Types import SpotType

class IsStationAvailable():
    def __init__(self, isAvailable: bool, stationInfo, airline:str, spotType:SpotType) -> None:
        '''
            isAvailable: ficou livre (true) ou ocupado (false)
            stationInfo: informações sobre a gare em questão
            spotType: tipo de spot que ficou livre ou ocupado
        '''
        self.isAvailable: bool = isAvailable
        self.station = stationInfo # objeto Station
        self.airline = airline
        self.spotType:SpotType = spotType