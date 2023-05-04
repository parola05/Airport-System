from spade.behaviour import CyclicBehaviour

class ReceiveProposalAnswerBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("Starting Receive Proposal Answer Behaviour . . .")

    async def run(self):
        msg = await self.receive(timeout=100) 

        if msg:
            performative = msg.get_metadata('performative')
            if performative == 'agree':
                #print(msg.body)
                pass
            elif performative == 'reject-proposal':
                #print(msg.body)
                pass
        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")