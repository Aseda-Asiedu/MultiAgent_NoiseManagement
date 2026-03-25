class SupervisorAgent:
    def handle_violation(self, percept):
        zone = percept["zone"]
        noise = percept["noise"]

        print("\n[SUPERVISOR AGENT RESPONSE]")
        print(f"High noise detected in {zone} ({noise}dB).")
        print("Action: Incident logged and authority notified.\n")