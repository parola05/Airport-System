from spade.behaviour import CyclicBehaviour
import jsonpickle
from MessagesProtocol.DashboardControlTowerMessage import DashboardControlTowerMessage
from GlobalTypes.Types import DashboardControlTowerMessageType, RequestType, StatusType
import customtkinter

class ReceiveUpdatesBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("[DashboardControlTower] Starting ReceiveUpdatesBehaviour")

    async def run(self):
        msg = await self.receive(timeout=100) 
        if msg:
            dashboardControlTowerMessage:DashboardControlTowerMessage = jsonpickle.decode(msg.body)

            # update textbox in "Airplanes Requests tab"
            if dashboardControlTowerMessage.type == DashboardControlTowerMessageType.AIRPLANE_REQUEST:

                # SET tag for text color
                tag = ""
                if dashboardControlTowerMessage.requestType == RequestType.LAND:
                    tag = "tag6"
                elif dashboardControlTowerMessage.requestType == RequestType.TAKEOFF:
                    tag = "tag6"
                elif dashboardControlTowerMessage.informStatus == StatusType.TO_ANOTHER_AIRPORT:
                    tag = "tag4"
                elif dashboardControlTowerMessage.informStatus == StatusType.TAKING_OFF or dashboardControlTowerMessage.informStatus == StatusType.FLYING:
                    tag = "tag1"
                elif dashboardControlTowerMessage.informStatus == StatusType.LANDING or dashboardControlTowerMessage.informStatus == StatusType.IN_STATION:
                    tag = "tag1"
                    
                self.agent.view.tab_1.textbox.insert("end", "> " + dashboardControlTowerMessage.requestText + "\n",tag)
                self.agent.tab_1_line += 1

            elif dashboardControlTowerMessage.type == DashboardControlTowerMessageType.AIRPLANE_IN_QUEUE:
                if dashboardControlTowerMessage.requestType == RequestType.LAND:
                    tag = "tag2"
                elif dashboardControlTowerMessage.requestType == RequestType.TAKEOFF:
                    tag = "tag1"
                
                self.agent.view.tab_2.textbox.insert("end", "> " + dashboardControlTowerMessage.requestText + "\n",tag)
                self.agent.tab_2_line += 1

            elif dashboardControlTowerMessage.type == DashboardControlTowerMessageType.PERMISSION_DENIED:
                tag = "tag3"
                self.agent.view.tab_1.textbox.insert("end", "> " + dashboardControlTowerMessage.permissionText + "\n",tag)
                self.agent.tab_1_line += 1

            elif dashboardControlTowerMessage.type == DashboardControlTowerMessageType.PERMISSION_ACCEPTED:
                tag = "tag2"
                self.agent.view.tab_1.textbox.insert("end", "> " + dashboardControlTowerMessage.permissionText + "\n",tag)
                self.agent.tab_1_line += 1