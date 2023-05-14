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
                await self.handlerRequest(receiveMsg=receiveMsg)

            # Receives information that the airplane departed to another airport
            elif performative == "cancel":
                await self.handlerCancel(receiveMsg=receiveMsg)
            
            # Receives information that there are no available parking gates or runways
            elif performative == "refuse":
                await self.handlerRefuse(receiveMsg=receiveMsg)

            # Receives information that there are available parking gates or runways
            # for a specified request (airplaneID is identified in the message)
            elif performative == "confirm":
                await self.handlerConfirm(receiveMsg=receiveMsg)

            # Receives information from the airplane about their status
            elif performative == 'inform':
                await self.handlerInform(receiveMsg=receiveMsg)

            # Receives the information that an airline has purchased new parking spots at the stations. 
            # Therefore, if any airplane from this airline is in the air and in the waiting queue, 
            # it will have the chance to land since there is space available for it!
            elif performative == 'inform-if':
                await self.handlerQueryIf(receiveMsg=receiveMsg)
                       

    async def processMostPriorityRequest(self,runway=None,requests=None):
        # process the most priority request
        request = self.getRequestWithMorePriority(requests)
        if request is not None:
            request.haveRunway = True

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
                    runwayInfo=runway
                )
                sendMsg.body = jsonpickle.encode(runwayAvailabilityInfo)
                await self.send(sendMsg)

                # Update Dashboard
                permissionText="permission accepted for " + str(request.id) + " -> Airplane can take-off in runway " + runway.id

                msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                msg.set_metadata("performative", "inform")
                bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                    type=DashboardControlTowerMessageType.PERMISSION_ACCEPTED,
                    permissionText=permissionText
                )
                msg.body = jsonpickle.encode(bodyMessage)
                await self.send(msg)

                # send message to airplane with runway to take-off
                request.runway = runway
                sendMsg = Message(to=request.id + "@" + Conf().get_openfire_server())
                sendMsg.set_metadata("performative", "agree")
                sendMsg.body = jsonpickle.encode(request)
                await self.send(sendMsg)

                # remove request from airplane
                del self.agent.requestsInProcess[request.id]

    async def processMostPriorityRequestLock(self,requests=None):

        request = self.getRequestWithMorePriority(requests)
        del self.agent.lockRequests[request.id]
        
        if request is not None:
            self.agent.requestsInProcess[request.id] = request
   
            if request.typeRequest == RequestType.LAND:
                sendMsg = Message(to="station@" + Conf().get_openfire_server())
                sendMsg.set_metadata("performative", "query-if")
                sendMsg.body = jsonpickle.encode(request)
                await self.send(sendMsg)

            elif request.typeRequest == RequestType.TAKEOFF:
                msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                msg.set_metadata("performative", "inform")
                bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                    type=DashboardControlTowerMessageType.AIRPLANE_REQUEST,
                    requestType=RequestType.TAKEOFF, 
                    requestText=str(request.id) + " from " + str(request.airlineID) + " request to take-off at " + str(request.requestTime.strftime("%H:%M:%S")) + " with priority " +  self.priorityToString(request.priority)
                )
                msg.body = jsonpickle.encode(bodyMessage)
                await self.send(msg)

    async def handlerRequest(self,receiveMsg):
        sender_name = receiveMsg.sender
        requestFromAirplane:RequestFromAirplane = jsonpickle.decode(receiveMsg.body)

        ############### Init Update Dashboard Control Tower
        msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "inform")
        requestText = "" 
        
        if requestFromAirplane.typeRequest == RequestType.LAND:
            requestText=str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " ("+ self.spotTypeToString(requestFromAirplane.spotType)+" airplane) request to land at " + str(requestFromAirplane.requestTime.strftime("%H:%M:%S"))+ " with priority " + self.priorityToString(requestFromAirplane.priority)
        elif requestFromAirplane.typeRequest == RequestType.TAKEOFF:
            requestText=str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " request to take-off at " + str(requestFromAirplane.requestTime.strftime("%H:%M:%S")) + " with priority " +  self.priorityToString(requestFromAirplane.priority)

        bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
            type=DashboardControlTowerMessageType.AIRPLANE_REQUEST,
            requestType=requestFromAirplane.typeRequest,
            requestText=requestText
        )
        msg.body = jsonpickle.encode(bodyMessage)
        await self.send(msg)
        ############### Finish Update Dashboard Control Tower

        ############### Init Process Request
        if len(self.agent.lockRequests) == 0: # If there is no requests in lockRequests, the request can be processed (otherwise the information of station or runway can be outdated)
            # Airplane want to land
            if requestFromAirplane.typeRequest == RequestType.LAND:
                isFull = self.isQueueFull(self.agent.queueInTheAir)

                # Get informations of stations
                if not isFull:
                    self.agent.requestsInProcess[requestFromAirplane.id] = requestFromAirplane

                    sendMsg = Message(to="station@" + Conf().get_openfire_server())
                    sendMsg.set_metadata("performative", "query-if")
                    sendMsg.body = jsonpickle.encode(requestFromAirplane)
                    await self.send(sendMsg)

                else:
                    sendMsg = Message(to=sender_name)
                    sendMsg.set_metadata("performative", "refuse")
                    sendMsg.body = "Go to another airport, the queue is full"
                    await self.send(sendMsg)

            # Airplane want to take-off
            elif requestFromAirplane.typeRequest == RequestType.TAKEOFF:
                self.agent.requestsInProcess[requestFromAirplane.id] = requestFromAirplane
                sendMsg = Message(to="runway@" + Conf().get_openfire_server())
                sendMsg.set_metadata("performative", "query-if")
                sendMsg.body = jsonpickle.encode(requestFromAirplane)
                await self.send(sendMsg)

        else: # add request in lockRequests
            self.agent.lockRequests[requestFromAirplane.id] = requestFromAirplane
        ############## Finish Process Request

    async def handlerCancel(self,receiveMsg):
        requestFromAirplane:RequestFromAirplane = jsonpickle.decode(receiveMsg.body)

        if requestFromAirplane.id in self.agent.requestsInProcess:
            del self.agent.requestsInProcess[requestFromAirplane.id]

        ############### Init Update Dashboard Control Tower
        msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "inform")
        bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
            type=DashboardControlTowerMessageType.AIRPLANE_REQUEST,
            informStatus=StatusType.TO_ANOTHER_AIRPORT, 
            requestText=str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " is going to another airport" 
        )
        msg.body = jsonpickle.encode(bodyMessage)
        await self.send(msg)  
        ############### Finish Update Dashboard Control Tower

    async def handlerRefuse(self,receiveMsg):
        requestFromAirplane:RequestFromAirplane = jsonpickle.decode(receiveMsg.body)

        # add airplane in the queue with airplane is in the air
        if requestFromAirplane.typeRequest == RequestType.LAND:
            airlineID = requestFromAirplane.airlineID
            if airlineID not in self.agent.queueInTheAir:
                self.agent.queueInTheAir[airlineID] = [requestFromAirplane]
            else: self.agent.queueInTheAir[airlineID].append(requestFromAirplane)

        ###############  Send message to airplane know that have to wait
        sendMsg = Message(to=str(requestFromAirplane.id) + "@" + Conf().get_openfire_server())
        sendMsg.set_metadata("performative", "inform")
        sendMsg.body = jsonpickle.encode(requestFromAirplane)
        await self.send(sendMsg)
        ############### Finish 

        ############### Init Update Dashboard Control Tower with permission denied 
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
        ############### Finish Update Dashboard Control Tower
        
        ############### Init Update Dashboard queue section (both in the air and in the ground are updated, its more like "waiting airplanes")
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
        ############### Finish Update Dashboard Control tower queue section

        # process next priority request if the current request already have been reserved a runway that not used!
        if requestFromAirplane.haveRunway:
            requestFromAirplane.haveRunway = False
            requests = list(self.agent.requestsInProcess.values()).copy()
            
            requestsWithoutMostPriorityRequest = []
            for request in requests:
                if request.id is not requestFromAirplane.id:
                    requestsWithoutMostPriorityRequest.append(request)

            await self.processMostPriorityRequest(requestFromAirplane.runway,requests)

        # process next priority request from lockRequests if there is a locked request
        elif len(self.agent.lockRequests) > 0:
            requests = list(self.agent.lockRequests.values()).copy()
            await self.processMostPriorityRequestLock(requests)

    async def handlerConfirm(self,receiveMsg):
        sender_name = receiveMsg.sender
        receiveMsgDecoded:tuple = jsonpickle.decode(receiveMsg.body)
        airplaneID = receiveMsgDecoded[0]

        # If Station confirm, control tower should question runwayManager about runways
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
            
            # if airplane want to land, calculate staton closest to the runway, put the station in the message to the airplane know the station and reserve Station
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

            # reserve the runway
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

            ############ Init Update Dashboard Control Tower 
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
            ############ Finish Update Dashboard Control Tower 

            # remove request from airplane
            del self.agent.requestsInProcess[airplaneID]

            # process next priority request from lockRequests if there is a locked request
            if len(self.agent.lockRequests) > 0:
                requests = list(self.agent.lockRequests.values()).copy()
                await self.processMostPriorityRequestLock(requests)

    async def handlerInform(self,receiveMsg):
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
            requests = list(self.agent.requestsInProcess.values())
            await self.processMostPriorityRequest(runway=requestFromAirplane.runway,requests=requests)

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
            requests = list(self.agent.requestsInProcess.values())
            await self.processMostPriorityRequest(requestFromAirplane.runway, requests)

    async def handlerQueryIf(self,receiveMsg):
        newSpotsAvailable:NewSpotsAvailable = jsonpickle.decode(receiveMsg.body)
                
        # Get members of object
        numberOfSpotsAvailable:int = newSpotsAvailable.nSpots
        airlineID = newSpotsAvailable.airline
        spotTypeAvailable:SpotType = newSpotsAvailable.spotType

        ############ Init Update Dashboard Control Tower 
        text=airlineID + " bought " + str(numberOfSpotsAvailable) + " spots -> check if airplanes in the air from the airline can land"
        msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "inform")
        bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
            type=DashboardControlTowerMessageType.PERMISSION_ACCEPTED,
            permissionText=text
        )
        msg.body = jsonpickle.encode(bodyMessage)
        await self.send(msg)
        ############ Finish Update Dashboard Control Tower 

        
        # Execute actions only if there are airplanes from the airline in the queue
        if airlineID in self.agent.queueInTheAir:
            dup_list = self.agent.queueInTheAir[airlineID].copy()
            for i in range(0,numberOfSpotsAvailable):
                
                # Get more priority land request 
                request:RequestFromAirplane = self.getRequestWithMorePriority(dup_list,onlyLandRequests=True)
                
                # Repeat the process like queue is not full!
                # Get Stations available ...
                if request is not None:
                    self.agent.requestInProcess = True

                    sendMsg = Message(to="station@" + Conf().get_openfire_server())
                    sendMsg.set_metadata("performative", "query-if")
                    sendMsg.body = jsonpickle.encode(request)
                    await self.send(sendMsg)

                    dup_list.remove(request)