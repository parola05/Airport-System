from spade.behaviour import CyclicBehaviour
import jsonpickle
from MessagesProtocol.DashboardAirlinesMessage import DashboardAirlinesMessage, NegotiationStatus
from GlobalTypes.Types import DashboardAirlineMessageType
import customtkinter

class ReceiveUpdatesBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("[DashboardAirline] Starting ReceiveUpdatesBehaviour")

    async def run(self):
        msg = await self.receive(timeout=100) 
        if msg:
            dashboardAirlines:DashboardAirlinesMessage = jsonpickle.decode(msg.body)

            # update textbox (spots negotiation tab)
            if dashboardAirlines.type == DashboardAirlineMessageType.NEGOTIATION:

                # SET tag for text color
                tag = ""
                if dashboardAirlines.negotiationStatus == NegotiationStatus.PROPOSE:
                    tag = "tag1"
                elif dashboardAirlines.negotiationStatus == NegotiationStatus.SUCCESS:
                    tag = "tag2"
                elif dashboardAirlines.negotiationStatus == NegotiationStatus.FAIL:
                    tag = "tag3"

                # add message in textbox
                self.agent.view.tab_2.textbox.insert("end", "> " + dashboardAirlines.negotiationtext + "\n",tag)
                
                # update line for next message
                self.agent.line += 1 

            # add airline in airlines list (airline tab)
            elif dashboardAirlines.type == DashboardAirlineMessageType.INFO:

                # add label entry for airline ID
                labelID = customtkinter.CTkLabel(master=self.agent.view.tab_1.airlinesTable, text=dashboardAirlines.airlineInfo.id)
                labelID.grid(row=self.agent.rowIndex, column=0, padx=10, pady=(0, 20))

                # add label entry for airline number of commercial spots bought (zero before the negotiation conclusion)
                nSpotsCommercialLabel = customtkinter.CTkLabel(master=self.agent.view.tab_1.airlinesTable, text=dashboardAirlines.airlineInfo.nSpotsCommercial)
                nSpotsCommercialLabel.grid(row=self.agent.rowIndex, column=1, padx=10, pady=(0, 20))

                # add label entry for airline number of merchandise spots bought (zero before the negotiation conclusion)
                nSpotsMerchandiseLabel = customtkinter.CTkLabel(master=self.agent.view.tab_1.airlinesTable, text=dashboardAirlines.airlineInfo.nSpotsMerchandise)
                nSpotsMerchandiseLabel.grid(row=self.agent.rowIndex, column=2, padx=10, pady=(0, 20))
                
                # update rowIndex for next label
                self.agent.rowIndex += 1

                # keep label of nSpots to eventually updates some value in this label
                self.agent.view.tab_1.labels[dashboardAirlines.airlineInfo.id] = {}
                self.agent.view.tab_1.labels[dashboardAirlines.airlineInfo.id]["nSpotsMerchandiseLabel"] = nSpotsMerchandiseLabel
                self.agent.view.tab_1.labels[dashboardAirlines.airlineInfo.id]["nSpotsCommercialLabel"] = nSpotsCommercialLabel

            # update airline label in the list (airline tab)
            elif dashboardAirlines.type == DashboardAirlineMessageType.UPDATE:
                self.agent.view.tab_1.labels[dashboardAirlines.airlineInfo.id]["nSpotsMerchandiseLabel"].configure(text=dashboardAirlines.airlineInfo.nSpotsMerchandise)
                self.agent.view.tab_1.labels[dashboardAirlines.airlineInfo.id]["nSpotsCommercialLabel"].configure(text=dashboardAirlines.airlineInfo.nSpotsCommercial)