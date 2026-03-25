import asyncio
import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from models.policies import get_policies 
from environment.noise_environment import NoiseEnvironment

class NoiseAgent(Agent):
    class MonitorBehaviour(CyclicBehaviour):
        async def on_start(self):
            self.policies = get_policies()
            self.env = NoiseEnvironment()
            # Restore original Beliefs (Memory)
            self.beliefs = {"violations": {}, "warnings": {}}
            print("[SETUP] NoiseAgent (BDI Logic) initialized.")

        def perceive(self, zone, noise, hour):
            # Original perception logic
            return {
                "zone": zone,
                "noise": noise,
                "hour": hour,
                "time_period": "Night" if hour >= 21 or hour < 6 else "Day"
            }

        def decide(self, percept):
            # Original decision logic using policies
            policy = self.policies[percept["zone"]]
            noise = percept["noise"]
            if noise <= policy["acceptable"]: return "ACCEPTABLE"
            elif noise <= policy["caution"]: return "CAUTION"
            else: return "VIOLATION"

        def update_beliefs(self, zone, decision):
            # Original belief update logic
            if zone not in self.beliefs["violations"]:
                self.beliefs["violations"][zone] = 0
                self.beliefs["warnings"][zone] = 0
            if decision == "CAUTION": self.beliefs["warnings"][zone] += 1
            elif decision == "VIOLATION": self.beliefs["violations"][zone] += 1

        def plan(self, percept, decision):
            # Original planning logic based on beliefs
            zone = percept["zone"]
            if decision == "ACCEPTABLE": return "monitor"
            elif decision == "CAUTION":
                return "escalate_warning" if self.beliefs["warnings"].get(zone, 0) >= 2 else "warn"
            elif decision == "VIOLATION":
                return "critical_escalation" if self.beliefs["violations"].get(zone, 0) >= 2 else "strong_warning"

        async def run(self):
            # 1. PERCEPT
            z, n, h = self.env.generate()
            percept = self.perceive(z, n, h)
            
            # 2. DECISION & BELIEF UPDATE
            decision = self.decide(percept)
            self.update_beliefs(z, decision)
            
            # 3. PLAN
            selected_plan = self.plan(percept, decision)

            # 4. ACTION (The detailed original output format)
            print("\n" + "="*60)
            print(f"[PERCEPT] Zone: {z} | Noise: {n}dB | Time: {h}:00 ({percept['time_period']})")
            print(f"[DECISION] Classified as: {decision}")
            print(f"[PLAN] Selected plan: {selected_plan}")

            if selected_plan == "critical_escalation":
                print("[ACTION] Critical noise level. Notifying Supervisor Agent...")
                msg = Message(to="supervisor@localhost")
                msg.body = f"{z},{n},{h}"
                await self.send(msg)
            else:
                # Map plans to original action text
                actions = {
                    "monitor": "Environment within limits. Monitoring continues.",
                    "warn": "Suggest reducing noise levels.",
                    "strong_warning": "Issuing strong warning to occupants.",
                    "escalate_warning": "Repeated noise detected. Escalating warning level."
                }
                print(f"[ACTION] {actions.get(selected_plan)}")

            print(f"[BELIEF UPDATE] Violations in {z}: {self.beliefs['violations'][z]} | Warnings: {self.beliefs['warnings'][z]}")
            print("="*60)

            await asyncio.sleep(4)

    async def setup(self):
        self.add_behaviour(self.MonitorBehaviour())