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

    def isQueueFull(self,queueInTheAir: Dict):
        amountWaiting = 0
        for airplanesFromAirline in queueInTheAir.values():
            amountWaiting += len(airplanesFromAirline)
        return amountWaiting >= self.agent.queueInTheAirMaxSize
    
    def getRequestWithMorePriority(self,requests:List[RequestFromAirplane]):
        highPriorityAirplanes = list(filter(lambda request: request.priority == Priority.HIGH and request.typeRequest == RequestType.LAND, requests))
        if len(highPriorityAirplanes) > 0:
            olderRequest = min(highPriorityAirplanes, key=lambda request: request.requestTime)
            return olderRequest
        else:
            mediumPriorityAirplanes = list(filter(lambda request: request.priority == Priority.MEDIUM and request.typeRequest == RequestType.LAND, requests))
            if len(mediumPriorityAirplanes) > 0:
                olderRequest = min(mediumPriorityAirplanes, key=lambda request: request.requestTime)
                return olderRequest
            else:
                lowPriorityAirplanes = list(filter(lambda request: request.priority == Priority.LOW and request.typeRequest == RequestType.LAND, requests))
                if len(lowPriorityAirplanes) > 0:
                    olderRequest = min(lowPriorityAirplanes, key=lambda request: request.requestTime)
                    return olderRequest
                else: return None

    async def run(self):

        receiveMsg = await self.receive()

        if receiveMsg:
            sender_name = receiveMsg.sender
            performative = receiveMsg.get_metadata('performative')

            # Recebe um pedido do avião para aterrar ou decolar
            if performative == 'request':
                requestFromAirplane:RequestFromAirplane = jsonpickle.decode(receiveMsg.body)

                # Recebe um pedido do avião para aterrar
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
                        requestText=str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " request to land at " + str(requestFromAirplane.requestTime.strftime("%H:%M:%S"))+ " with priority " + self.priorityToString(requestFromAirplane.priority)
                    )
                    msg.body = jsonpickle.encode(bodyMessage)
                    await self.send(msg)

                # Recebe um pedido do avião para levantar voo
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

            # Recebe informação de que o avião partiu para outro aeroporto
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
            
            # Recebe a informação de que não existem gares ou pistas disponíveis
            elif performative == "refuse":
                requestFromAirplane:RequestFromAirplane = jsonpickle.decode(receiveMsg.body)

                airlineID = requestFromAirplane.airlineID
                if airlineID not in self.agent.queueInTheAir:
                    self.agent.queueInTheAir[airlineID] = [requestFromAirplane]
                else: self.agent.queueInTheAir[airlineID].append(requestFromAirplane)

                sendMsg = Message(to=str(requestFromAirplane.id) + "@" + Conf().get_openfire_server())
                sendMsg.set_metadata("performative", "inform")
                sendMsg.body = jsonpickle.encode(requestFromAirplane)
                await self.send(sendMsg)

                ############ Update Dashboard Tab Request ############
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
                
                ############ Update Dashboard Tab Queue ############
                msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                msg.set_metadata("performative", "inform")
                if requestFromAirplane.typeRequest == RequestType.LAND:
                    requestText=str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " is waiting to land.." 
                else:
                    requestText=str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " is waiting to take off.." 
                bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                    type=DashboardControlTowerMessageType.AIRPLANE_IN_QUEUE,
                    requestType=requestFromAirplane.typeRequest,
                    requestText=requestText
                )
                msg.body = jsonpickle.encode(bodyMessage)
                await self.send(msg)

            # Recebe a informação de que existem gares ou pistas disponíveis
            elif performative == "confirm":
                receiveMsgDecoded:tuple = jsonpickle.decode(receiveMsg.body)
                airplaneID = receiveMsgDecoded[0]

                if "station@" in str(sender_name):
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

            # Receives information from the airplane after being allowed to land or take off
            elif performative == 'inform':
                requestFromAirplane:RequestFromAirplane = jsonpickle.decode(receiveMsg.body)
                
                ########### UPDATE DASHBOARD ###########
                msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                msg.set_metadata("performative", "inform")

                # both runway and station already reserved in "confirm" performative
                if requestFromAirplane.status == StatusType.LANDING:
                    informStatus = StatusType.LANDING
                    requestText = str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " confirm that receive the permission and is landing in runway " + str(requestFromAirplane.runway.id)

                # runway become free when airplane park, but the station stays occuped
                elif requestFromAirplane.status == StatusType.IN_STATION:
                    informStatus = StatusType.IN_STATION
                    requestText = str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " confim that is parked in station " + str(requestFromAirplane.station.id)

                    sendMsg = Message(to="runway@" + Conf().get_openfire_server())
                    sendMsg.set_metadata("performative", "inform-ref")
                    runwayAvailabilityInfo = IsRunwayAvailable(
                        isAvailable=True,
                        runwayInfo=requestFromAirplane.runway
                    )
                    sendMsg.body = jsonpickle.encode(runwayAvailabilityInfo)
                    await self.send(sendMsg)

                    msg = Message(to="dashboardControlTower@" + Conf().get_openfire_server())
                    msg.set_metadata("performative", "inform")
                
                # runway already reserved in "confirm" performative, however the station must be free
                elif requestFromAirplane.status == StatusType.TAKING_OFF:
                    informStatus = StatusType.TAKING_OFF
                    requestText = str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " confirm that receive the permission and is taking off in runway " + str(requestFromAirplane.runway.id)
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

                # runway must be free
                elif requestFromAirplane.status == StatusType.FLYING:
                    informStatus = StatusType.FLYING
                    requestText = str(requestFromAirplane.id) + " from " + str(requestFromAirplane.airlineID) + " is flying"
                    
                    sendMsg = Message(to="runway@" + Conf().get_openfire_server())
                    sendMsg.set_metadata("performative", "inform-ref")
                    runwayAvailabilityInfo = IsRunwayAvailable(
                                                isAvailable=True,
                                                runwayInfo=requestFromAirplane.runway
                                             )
                    sendMsg.body = jsonpickle.encode(runwayAvailabilityInfo)
                    await self.send(sendMsg)

                bodyMessage:DashboardControlTowerMessage = DashboardControlTowerMessage(
                    type=DashboardControlTowerMessageType.AIRPLANE_REQUEST,
                    informStatus=informStatus,
                    requestText=requestText
                )

                msg.body = jsonpickle.encode(bodyMessage)
                await self.send(msg)

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
                        request:RequestFromAirplane = self.getRequestWithMorePriority(dup_list)
                        
                        # Repeat the process like queue is not full!
                        # Get Stations available ...
                        if request is not None:
                            print("get request!")
                            sendMsg = Message(to="station@" + Conf().get_openfire_server())
                            sendMsg.set_metadata("performative", "query-if")
                            sendMsg.body = jsonpickle.encode(request)
                            await self.send(sendMsg)

                            dup_list.remove(request)