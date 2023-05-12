from typing import Dict, List
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import platform, sys, jsonpickle

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from MessagesProtocol.RequestFromAirplane import RequestFromAirplane
from MessagesProtocol.DashboardControlTowerMessage import DashboardControlTowerMessage
from MessagesProtocol.IsRunwayAvailable import IsRunwayAvailable
from MessagesProtocol.IsStationAvailable import IsStationAvailable
from MessagesProtocol.NewSpotsAvailable import NewSpotsAvailable
from GlobalTypes.Types import Priority
from GlobalTypes.Types import RequestType, DashboardControlTowerMessageType, StatusType, SpotType, Priority
from Conf import Conf

class ReceiveBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("[Control Tower] starting ReceiveBehaviour")

    def priorityToString(self,priority:Priority=None):
        if priority == Priority.HIGH: return "HIGH"
        if priority == Priority.MEDIUM: return "MEDIUM"
        if priority == Priority.LOW: return "LOW"

    def spotTypeToString(self,spotType:SpotType=None):
        if spotType == SpotType.COMMERCIAL: return "Comercial"
        if spotType == SpotType.MERCHANDISE: return "Merchandise"

    def isQueueFull(self,queueInTheAir: Dict):
        amountWaiting = 0
        for airplanesFromAirline in queueInTheAir.values():
            amountWaiting += len(airplanesFromAirline)
        return amountWaiting >= self.agent.queueInTheAirMaxSize
    
    def getRequestWithMorePriority(self,requests:List[RequestFromAirplane],onlyLandRequests:bool=False):
        if onlyLandRequests == True:
            highPriorityAirplanes = list(filter(lambda request: request.priority == Priority.HIGH and request.typeRequest == RequestType.LAND, requests))
        else:     
            highPriorityAirplanes = list(filter(lambda request: request.priority == Priority.HIGH, requests))
        if len(highPriorityAirplanes) > 0:
            olderRequest = min(highPriorityAirplanes, key=lambda request: request.requestTime)
            return olderRequest
        else:
            if onlyLandRequests == True:
                mediumPriorityAirplanes = list(filter(lambda request: request.priority == Priority.MEDIUM and request.typeRequest == RequestType.LAND, requests))
            else:     
                mediumPriorityAirplanes = list(filter(lambda request: request.priority == Priority.MEDIUM, requests))
            if len(mediumPriorityAirplanes) > 0:
                olderRequest = min(mediumPriorityAirplanes, key=lambda request: request.requestTime)
                return olderRequest
            else:
                if onlyLandRequests == True:
                    lowPriorityAirplanes = list(filter(lambda request: request.priority == Priority.LOW and request.typeRequest == RequestType.LAND, requests))
                else:     
                    lowPriorityAirplanes = list(filter(lambda request: request.priority == Priority.LOW, requests))
                if len(lowPriorityAirplanes) > 0:
                    olderRequest = min(lowPriorityAirplanes, key=lambda request: request.requestTime)
                    return olderRequest
                else: return None

    async def run(self):
        receiveMsg = await self.receive()

        if receiveMsg:
            sender_name = receiveMsg.sender
            performative = receiveMsg.get_metadata('performative')

            # Receive a request from airplane to land or taking-off
            if performative == 'request':
                requestFromAirplane:RequestFromAirplane = jsonpickle.decode(receiveMsg.body)

                # Airplane wants to land
                if requestFromAirplane.typeRequest == RequestType.LAND:
                    isFull = self.isQueueFull(self.agent.queueInTheAir)

                    if not isFull:
                        self.agent.requestsInProcess[requestFromAirplane.id] = requestFromAirplane

                        sendMsg = Message(to="station@" + Conf().get_openfire_server())
                        sendMsg.set_metadata("performative", "query-if")
                        sendMsg.body = jsonpickle.encode(requestFromAirplane)
                        await self.send(sendMsg)

                    else:
                        print("queue full!")
                        sendMsg = Message(to=sender_name)
                        sendMsg.set_metadata("performative", "refuse")
                        sendMsg.body = "Go to another airport, the queue is full"
                        await self.send(sendMsg)

                    ############### Update Dashboard ###############
                    msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                    msg.set_metadata("performative", "inform")
                    bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                        type=DashboardControlTowerMessageType.AIRPLANE_REQUEST,
                        requestType=RequestType.LAND, 
                        requestText=str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " ("+ self.spotTypeToString(requestFromAirplane.spotType)+" airplane) request to land at " + str(requestFromAirplane.requestTime.strftime("%H:%M:%S"))+ " with priority " + self.priorityToString(requestFromAirplane.priority)
                    )
                    msg.body = jsonpickle.encode(bodyMessage)
                    await self.send(msg)

                # Airplane want to take-off
                elif requestFromAirplane.typeRequest == RequestType.TAKEOFF:
                    self.agent.requestsInProcess[requestFromAirplane.id] = requestFromAirplane
                    sendMsg = Message(to="runway@" + Conf().get_openfire_server())
                    sendMsg.set_metadata("performative", "query-if")
                    sendMsg.body = jsonpickle.encode(requestFromAirplane)
                    await self.send(sendMsg)
                    
                    ############### Update Dashboard ###############
                    msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                    msg.set_metadata("performative", "inform")
                    bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                        type=DashboardControlTowerMessageType.AIRPLANE_REQUEST,
                        requestType=RequestType.TAKEOFF, 
                        requestText=str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " request to take-off at " + str(requestFromAirplane.requestTime.strftime("%H:%M:%S")) + " with priority " +  self.priorityToString(requestFromAirplane.priority)
                    )
                    msg.body = jsonpickle.encode(bodyMessage)
                    await self.send(msg)

            # Receives information that the airplane departed to another airport
            elif performative == "cancel":
                requestFromAirplane:RequestFromAirplane = jsonpickle.decode(receiveMsg.body)
                if sender_name in self.agent.requestsInProcess:
                    del self.agent.requestsInProcess[requestFromAirplane.id]

                ############ Update Dashboard ############
                msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                msg.set_metadata("performative", "inform")
                bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                    type=DashboardControlTowerMessageType.AIRPLANE_REQUEST,
                    informStatus=StatusType.TO_ANOTHER_AIRPORT, 
                    requestText=str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " is going to another airport" 
                )
                msg.body = jsonpickle.encode(bodyMessage)
                await self.send(msg)  
            
            # Receives information that there are no available parking gates or runways
            elif performative == "refuse":
                requestFromAirplane:RequestFromAirplane = jsonpickle.decode(receiveMsg.body)

                # add airplane in the queue with airplane is in the air
                if requestFromAirplane.typeRequest == RequestType.LAND:
                    airlineID = requestFromAirplane.airlineID
                    if airlineID not in self.agent.queueInTheAir:
                        self.agent.queueInTheAir[airlineID] = [requestFromAirplane]
                    else: self.agent.queueInTheAir[airlineID].append(requestFromAirplane)

                # send message to airplane know that have to wait
                sendMsg = Message(to=str(requestFromAirplane.id) + "@" + Conf().get_openfire_server())
                sendMsg.set_metadata("performative", "inform")
                sendMsg.body = jsonpickle.encode(requestFromAirplane)
                await self.send(sendMsg)

                # Update Dashboard Tab Request with permission denied 
                msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                msg.set_metadata("performative", "inform")

                if requestFromAirplane.typeRequest == RequestType.LAND:
                    permissionText="permission denied for " + str(requestFromAirplane.id) + " -> Airplane should stay in air waiting for updates" 
                else:
                    permissionText="permission denied for " + str(requestFromAirplane.id) + " -> Airplane should stay in the station waiting for updates" 
               
                bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                    type=DashboardControlTowerMessageType.PERMISSION_DENIED,
                    permissionText=permissionText
                )
                msg.body = jsonpickle.encode(bodyMessage)
                await self.send(msg)
                
                # Update Dashboard Queue (both in the air and in the ground are updated, its more like "waiting airplanes")
                msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                msg.set_metadata("performative", "inform")
                if requestFromAirplane.typeRequest == RequestType.LAND:
                    requestText=str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " is waiting to land" 
                else:
                    requestText=str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " is waiting to take off" 
                bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                    type=DashboardControlTowerMessageType.AIRPLANE_IN_QUEUE,
                    requestType=requestFromAirplane.typeRequest,
                    requestText=requestText
                )
                msg.body = jsonpickle.encode(bodyMessage)
                await self.send(msg)

                # 

            # Receives information that there are available parking gates or runways
            # for a specified request (airplaneID is identified in the message)
            elif performative == "confirm":
                receiveMsgDecoded:tuple = jsonpickle.decode(receiveMsg.body)
                airplaneID = receiveMsgDecoded[0]

                if "station@" in str(sender_name):
                    print("station confirm")
                    self.stationsAvailable = receiveMsgDecoded[1]
                    sendMsg = Message(to="runway@" + Conf().get_openfire_server())
                    sendMsg.set_metadata("performative", "query-if")
                    sendMsg.body = jsonpickle.encode(self.agent.requestsInProcess[airplaneID])
                    await self.send(sendMsg)
                
                elif "runway@" in str(sender_name):
                    runwaysAvailable = receiveMsgDecoded[1]
                    # put a random runway in the message to the airplane know the runway to land (the request will be the message to send back to airplane)
                    self.agent.requestsInProcess[airplaneID].runway = runwaysAvailable[0]
                    
                    # If airplane want to land, calculate staton closest to the runway and put the station in the message to the airplane know the station
                    if self.agent.requestsInProcess[airplaneID].typeRequest == RequestType.LAND:
                        closestStation = self.agent.closestStationToRunway(runwaysAvailable[0].coord, self.stationsAvailable)
                        self.agent.requestsInProcess[airplaneID].station = closestStation
                        
                        # reserve the station spot (will be busy)
                        sendMsg = Message(to="station@" + Conf().get_openfire_server())
                        sendMsg.set_metadata("performative", "inform-ref")
                        stationAvailabilityInfo = IsStationAvailable(
                            isAvailable=False,
                            stationInfo=closestStation,
                            airline=self.agent.requestsInProcess[airplaneID].airlineID,
                            spotType=self.agent.requestsInProcess[airplaneID].spotType
                        )
                        sendMsg.body = jsonpickle.encode(stationAvailabilityInfo)
                        await self.send(sendMsg)

                    #  reserve the runway (will be busy)
                    sendMsg = Message(to="runway@" + Conf().get_openfire_server())
                    sendMsg.set_metadata("performative", "inform-ref")
                    runwayAvailabilityInfo = IsRunwayAvailable(
                        isAvailable=False,
                        runwayInfo=runwaysAvailable[0]
                    )
                    sendMsg.body = jsonpickle.encode(runwayAvailabilityInfo)
                    await self.send(sendMsg)
                    
                    # remove airplane from queue (if the airplane is in the queue)
                    self.agent.removeAirplaneFromQueue(airlineID=self.agent.requestsInProcess[airplaneID].airlineID,airplaneID=airplaneID)

                    # send message to airplane with runway and station to land
                    sendMsg = Message(to=airplaneID + "@" + Conf().get_openfire_server())
                    sendMsg.set_metadata("performative", "agree")
                    sendMsg.body = jsonpickle.encode(self.agent.requestsInProcess[airplaneID])
                    await self.send(sendMsg)

                    ############ Update Dashboard Tab Request ############
                    if (self.agent.requestsInProcess[airplaneID].typeRequest == RequestType.LAND):
                        permissionText="permission accepted for " + str(self.agent.requestsInProcess[airplaneID].id) + " -> Airplane can land in runway " + self.agent.requestsInProcess[airplaneID].runway.id + ". Spot available in " +  self.agent.requestsInProcess[airplaneID].station.id
                    elif (self.agent.requestsInProcess[airplaneID].typeRequest == RequestType.TAKEOFF):
                        permissionText="permission accepted for " + str(self.agent.requestsInProcess[airplaneID].id) + " -> Airplane can take-off in runway " + self.agent.requestsInProcess[airplaneID].runway.id 

                    msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                    msg.set_metadata("performative", "inform")
                    bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                        type=DashboardControlTowerMessageType.PERMISSION_ACCEPTED,
                        permissionText=permissionText
                    )
                    msg.body = jsonpickle.encode(bodyMessage)
                    await self.send(msg)

                    # remove request from airplane
                    del self.agent.requestsInProcess[airplaneID]

            # Receives information from the airplane about their status
            elif performative == 'inform':
                requestFromAirplane:RequestFromAirplane = jsonpickle.decode(receiveMsg.body)
                
                # both runway and station already reserved in "confirm" performative
                if requestFromAirplane.status == StatusType.LANDING:
                    # update dashboard that airplane is landing
                    informStatus = StatusType.LANDING
                    requestText = str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " confirm that receive the permission and is landing in runway " + str(requestFromAirplane.runway.id)
                    msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                    msg.set_metadata("performative", "inform")

                    bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                        type=DashboardControlTowerMessageType.AIRPLANE_REQUEST,
                        informStatus=informStatus,
                        requestText=requestText
                    )

                    msg.body = jsonpickle.encode(bodyMessage)
                    await self.send(msg)

                # runway become free when airplane change to landing-> In_Station, but the station stays occuped
                # runway available -> process most priority request 
                elif requestFromAirplane.status == StatusType.IN_STATION:
                    # send information for runway manager update availability of the runway
                    sendMsg = Message(to="runway@" + Conf().get_openfire_server())
                    sendMsg.set_metadata("performative", "inform-ref")
                    runwayAvailabilityInfo = IsRunwayAvailable(
                        isAvailable=True,
                        runwayInfo=requestFromAirplane.runway
                    )
                    sendMsg.body = jsonpickle.encode(runwayAvailabilityInfo)
                    await self.send(sendMsg)

                    # Update dashboard with the information that airplane is parked
                    informStatus = StatusType.IN_STATION
                    requestText = str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " confim that is parked in station " + str(requestFromAirplane.station.id)
                    msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                    msg.set_metadata("performative", "inform")
                    bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                        type=DashboardControlTowerMessageType.AIRPLANE_REQUEST,
                        informStatus=informStatus,
                        requestText=requestText
                    )
                    msg.body = jsonpickle.encode(bodyMessage)
                    await self.send(msg)

                    # process the most priority request
                    request = self.getRequestWithMorePriority(list(self.agent.requestsInProcess.values()))
                    if request is not None:

                        # If the request type is land, the request should be put in the normal pipeline of processing:
                        # This pipeline is initialized with "get stations available"
                        if request.typeRequest == RequestType.LAND:
                            sendMsg = Message(to="station@" + Conf().get_openfire_server())
                            sendMsg.set_metadata("performative", "query-if")
                            sendMsg.body = jsonpickle.encode(request)
                            await self.send(sendMsg)

                        # If the request type is take-off, we need to reserve the runway that became free,
                        # inform airplane that it can take-off and remove the request from airplane
                        elif request.typeRequest == RequestType.TAKEOFF:
                            # reserve the runway
                            sendMsg = Message(to="runway@" + Conf().get_openfire_server())
                            sendMsg.set_metadata("performative", "inform-ref")
                            runwayAvailabilityInfo = IsRunwayAvailable(
                                isAvailable=False,
                                runwayInfo=requestFromAirplane.runway
                            )
                            sendMsg.body = jsonpickle.encode(runwayAvailabilityInfo)
                            await self.send(sendMsg)

                            # Update Control Tower Dashboard
                            permissionText="permission accepted for " + str(request.id) + " -> Airplane can take-off in runway " + requestFromAirplane.runway.id

                            msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                            msg.set_metadata("performative", "inform")
                            bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                                type=DashboardControlTowerMessageType.PERMISSION_ACCEPTED,
                                permissionText=permissionText
                            )
                            msg.body = jsonpickle.encode(bodyMessage)
                            await self.send(msg)

                            # send message to airplane with runway to take-off
                            request.runway = requestFromAirplane.runway
                            sendMsg = Message(to=request.id + "@" + Conf().get_openfire_server())
                            sendMsg.set_metadata("performative", "agree")
                            sendMsg.body = jsonpickle.encode(request)
                            await self.send(sendMsg)

                            # remove request from airplane
                            del self.agent.requestsInProcess[request.id]
                
                # runway already reserved in "confirm" performative, however the station must be free
                # this the airplane send this state when In_Station -> Taking_Off
                # station available -> process most priority request from the airline that have the spot
                elif requestFromAirplane.status == StatusType.TAKING_OFF:

                    # send information for station manager to update availablity of spot
                    sendMsg = Message(to="station@" + Conf().get_openfire_server())
                    sendMsg.set_metadata("performative", "inform-ref")
                    stationAvailabilityInfo = IsStationAvailable(
                        isAvailable=True,
                        stationInfo=requestFromAirplane.station,
                        spotType=requestFromAirplane.spotType,
                        airline=requestFromAirplane.airlineID
                    )
                    sendMsg.body = jsonpickle.encode(stationAvailabilityInfo)
                    await self.send(sendMsg)

                    # Update dashboard that airplane is taking-off
                    informStatus = StatusType.TAKING_OFF
                    requestText = str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " confirm that receive the permission and is taking off in runway " + str(requestFromAirplane.runway.id)
                    msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                    msg.set_metadata("performative", "inform")

                    bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                        type=DashboardControlTowerMessageType.AIRPLANE_REQUEST,
                        informStatus=informStatus,
                        requestText=requestText
                    )

                    msg.body = jsonpickle.encode(bodyMessage)
                    await self.send(msg)

                # runway become free when airplane change to taking-off -> flying, but the station stays occuped
                # runway available -> process most priority request 
                elif requestFromAirplane.status == StatusType.FLYING:
                    sendMsg = Message(to="runway@" + Conf().get_openfire_server())
                    sendMsg.set_metadata("performative", "inform-ref")
                    runwayAvailabilityInfo = IsRunwayAvailable(
                        isAvailable=True,
                        runwayInfo=requestFromAirplane.runway
                    )
                    sendMsg.body = jsonpickle.encode(runwayAvailabilityInfo)
                    await self.send(sendMsg)

                    # Update dashboard with the information that airplane is flying
                    informStatus = StatusType.FLYING
                    requestText = str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " is flying"
                    msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                    msg.set_metadata("performative", "inform")
                    bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                        type=DashboardControlTowerMessageType.AIRPLANE_REQUEST,
                        informStatus=informStatus,
                        requestText=requestText
                    )
                    msg.body = jsonpickle.encode(bodyMessage)
                    await self.send(msg)

                    # process the most priority request
                    request = self.getRequestWithMorePriority(list(self.agent.requestsInProcess.values()))
                    if request is not None:

                        # If the request type is land, the request should be put in the normal pipeline of processing:
                        # This pipeline is initialized with "get stations available"
                        if request.typeRequest == RequestType.LAND:
                            sendMsg = Message(to="station@" + Conf().get_openfire_server())
                            sendMsg.set_metadata("performative", "query-if")
                            sendMsg.body = jsonpickle.encode(request)
                            await self.send(sendMsg)

                        # If the request type is take-off, we need to reserve the runway that become free,
                        # inform airplane that it can take-off and remove the request from airplane
                        elif request.typeRequest == RequestType.TAKEOFF:
                            # reserve the runway (will be busy)
                            sendMsg = Message(to="runway@" + Conf().get_openfire_server())
                            sendMsg.set_metadata("performative", "inform-ref")
                            runwayAvailabilityInfo = IsRunwayAvailable(
                                isAvailable=False,
                                runwayInfo=requestFromAirplane.runway
                            )
                            sendMsg.body = jsonpickle.encode(runwayAvailabilityInfo)
                            await self.send(sendMsg)

                            # Update Dashboard
                            permissionText="permission accepted for " + str(request.id) + " -> Airplane can take-off in runway " + requestFromAirplane.runway.id

                            msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                            msg.set_metadata("performative", "inform")
                            bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                                type=DashboardControlTowerMessageType.PERMISSION_ACCEPTED,
                                permissionText=permissionText
                            )
                            msg.body = jsonpickle.encode(bodyMessage)
                            await self.send(msg)

                            # send message to airplane with runway to take-off
                            request.runway = requestFromAirplane.runway
                            sendMsg = Message(to=request.id + "@" + Conf().get_openfire_server())
                            sendMsg.set_metadata("performative", "agree")
                            sendMsg.body = jsonpickle.encode(request)
                            await self.send(sendMsg)

                            # remove request from airplane
                            del self.agent.requestsInProcess[request.id]

            # Receives the information that an airline has purchased new parking spots at the stations. 
            # Therefore, if any airplane from this airline is in the air and in the waiting queue, 
            # it will have the chance to land since there is space available for it!
            elif performative == 'inform-if':
                newSpotsAvailable:NewSpotsAvailable = jsonpickle.decode(receiveMsg.body)
                
                # Get members of object
                numberOfSpotsAvailable:int = newSpotsAvailable.nSpots
                airlineID = newSpotsAvailable.airline
                spotTypeAvailable:SpotType = newSpotsAvailable.spotType
                
                # Execute actions only if there are airplanes from the airline in the queue
                if airlineID in self.agent.queueInTheAir:
                    dup_list = self.agent.queueInTheAir[airlineID].copy()
                    for i in range(0,numberOfSpotsAvailable):
                        
                        # Get more priority land request 
                        request:RequestFromAirplane = self.getRequestWithMorePriority(dup_list,onlyLandRequests=True)
                        
                        # Repeat the process like queue is not full!
                        # Get Stations available ...
                        if request is not None:
                            sendMsg = Message(to="station@" + Conf().get_openfire_server())
                            sendMsg.set_metadata("performative", "query-if")
                            sendMsg.body = jsonpickle.encode(request)
                            await self.send(sendMsg)

                            dup_list.remove(request)