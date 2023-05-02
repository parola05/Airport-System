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
    # IN_RUNWAY = 5

class Priority:
    HIGH = 1
    MEDIUM = 2
    LOW = 3