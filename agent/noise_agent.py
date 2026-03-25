import time

class NoiseAgent:
    def __init__(self, policies, supervisor):
        self.policies = policies
        self.supervisor = supervisor

        # Beliefs (memory)
        self.beliefs = {
            "violations": {},
            "warnings": {}
        }

    def perceive(self, zone, noise, hour):
        return {
            "zone": zone,
            "noise": noise,
            "hour": hour,
            "time_period": "Night" if hour >= 21 or hour < 6 else "Day"
        }

    def decide(self, percept):
        policy = self.policies[percept["zone"]]
        noise = percept["noise"]

        if noise <= policy["acceptable"]:
            return "ACCEPTABLE"

        elif noise <= policy["caution"]:
            return "CAUTION"

        else:
            return "VIOLATION"

    def update_beliefs(self, zone, decision):
        if zone not in self.beliefs["violations"]:
            self.beliefs["violations"][zone] = 0
            self.beliefs["warnings"][zone] = 0

        if decision == "CAUTION":
            self.beliefs["warnings"][zone] += 1

        elif decision == "VIOLATION":
            self.beliefs["violations"][zone] += 1

    def plan(self, percept, decision):
        zone = percept["zone"]

        if decision == "ACCEPTABLE":
            return "monitor"

        elif decision == "CAUTION":
            if self.beliefs["warnings"].get(zone, 0) >= 2:
                return "escalate_warning"
            return "warn"

        elif decision == "VIOLATION":
            if self.beliefs["violations"].get(zone, 0) >= 2:
                return "critical_escalation"
            return "strong_warning"

    def act(self, percept, decision, plan):
        zone = percept["zone"]
        noise = percept["noise"]
        hour = percept["hour"]
        period = percept["time_period"]

        print("\n" + "="*60)

        # PERCEPT
        print(f"[PERCEPT] Zone: {zone} | Noise: {noise}dB | Time: {hour}:00 ({period})")
        time.sleep(1)

        # DECISION
        print(f"[DECISION] Classified as: {decision}")
        time.sleep(1)

        # PLAN
        print(f"[PLAN] Selected plan: {plan}")
        time.sleep(1)

        # ACTION
        if plan == "monitor":
            print("[ACTION] Environment is within acceptable limits. Monitoring continues.")

        elif plan == "warn":
            print("[ACTION] Suggest reducing noise levels.")

        elif plan == "strong_warning":
            print("[ACTION] Issuing strong warning to occupants.")

        elif plan == "escalate_warning":
            print("[ACTION] Repeated noise detected. Escalating warning level.")

        elif plan == "critical_escalation":
            print("[ACTION] Critical noise level. Notifying Supervisor Agent...")
            self.supervisor.handle_violation(percept)

        time.sleep(1)

        # BELIEF UPDATE DISPLAY
        print(f"[BELIEF UPDATE] Violations in {zone}: {self.beliefs['violations'].get(zone,0)} | "
              f"Warnings: {self.beliefs['warnings'].get(zone,0)}")

        print("="*60)

    def run_cycle(self, zone, noise, hour):
        percept = self.perceive(zone, noise, hour)
        decision = self.decide(percept)
        self.update_beliefs(zone, decision)
        plan = self.plan(percept, decision)
        self.act(percept, decision, plan)