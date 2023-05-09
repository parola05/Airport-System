class SpotType:
    MERCHANDISE = 1
    COMMERCIAL = 2

class RequestType:
    LAND = 1
    TAKEOFF = 2

class StatusType:
    IN_STATION = 1
    FLYING = 2
    LANDING = 3
    WAITING_TAKEOFF = 4
    WAITING_LAND = 5
    TO_ANOTHER_AIRPORT = 6

class Priority:
    HIGH = 1
    MEDIUM = 2
    LOW = 3

class DashboardAirlineMessageType:
    NEGOTIATION = 1
    INFO = 2
    UPDATE = 3

class DashboardAirplaneMessageType:
    INFO = 1

class DashboardRunwayMessageType:
    INFO = 1

class DashboardControlTowerMessageType:
    AIRPLANE_REQUEST = 1

class DashboardStationMessageType:
    INFO = 1

class NegotiationStatus:
    PROPOSE = 1
    SUCCESS = 2
    FAIL = 3