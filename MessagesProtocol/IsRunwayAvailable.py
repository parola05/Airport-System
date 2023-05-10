class IsRunwayAvailable():
    def __init__(self, isAvailable: bool, runwayInfo) -> None:
        '''
            isAvailable: ficou livre (true) ou ocupada (false)
            runwayInfo: informações sobre a pista em questão
        '''
        self.isAvailable: bool = isAvailable
        self.runway = runwayInfo # objeto Runway