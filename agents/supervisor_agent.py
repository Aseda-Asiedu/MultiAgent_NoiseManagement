import datetime
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

class SupervisorAgent(Agent):
    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                zone, noise, hour = msg.body.split(",")
                # Original Supervisor Response Format
                print("\n" + "*"*40)
                print("[SUPERVISOR AGENT RESPONSE]")
                print(f"High noise detected in {zone} ({noise}dB) at {hour}:00.")
                print("Action: Incident logged and authority notified.")
                print("*"*40 + "\n")

                # Persistent Logging
                with open("noise_violations.log", "a") as f:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{timestamp}] CRITICAL: {zone} - {noise}dB at {hour}:00\n")

    async def setup(self):
        self.add_behaviour(self.ReceiveBehaviour())