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
                    tag = "tag2"
                elif dashboardControlTowerMessage.requestType == RequestType.TAKEOFF:
                    tag = "tag1"
                elif dashboardControlTowerMessage.informStatus == StatusType.TO_ANOTHER_AIRPORT:
                    tag = "tag3"
                elif dashboardControlTowerMessage.informStatus == StatusType.TAKING_OFF:
                    tag = "tag4"
                elif dashboardControlTowerMessage.informStatus == StatusType.LANDING:
                    tag = "tag5"
                    

                # add message in textbox
                self.agent.view.tab_1.textbox.insert(str(self.agent.tab_1_line) + ".0", "> " + dashboardControlTowerMessage.requestText + "\n",tag)
                
                # update line for next message
                self.agent.tab_1_line += 1 