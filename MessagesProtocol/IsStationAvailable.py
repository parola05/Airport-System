from GlobalTypes.Types import SpotType

class IsStationAvailable():
    def __init__(self, isAvailable: bool, stationInfo, spotType:SpotType) -> None:
        '''
            isAvailable: ficou livre (true) ou ocupado (false)
            stationInfo: informações sobre a gare em questão
            spotType: tipo de spot que ficou livre ou ocupado
        '''
        self.isAvailable: bool = isAvailable
        self.station = stationInfo # objeto Station
        self.spotType:SpotType = spotType