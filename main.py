import time
from agent.noise_agent import NoiseAgent
from agent.supervisor_agent import SupervisorAgent
from environment.noise_environment import NoiseEnvironment
from models.policies import get_policies


def simulate_zone(agent, env, zone, cycles=5):
    print("="*25)
    print(f" Monitoring Zone: {zone}")
    print("="*25)

    for i in range(cycles):
        print(f"\n Cycle {i+1} ")

        # Generate environment input
        _, noise, hour = env.generate()

        # Run full agent cycle
        agent.run_cycle(zone, noise, hour)

        time.sleep(2)


def main():
    env = NoiseEnvironment()
    supervisor = SupervisorAgent()
    agent = NoiseAgent(get_policies(), supervisor)

    zones = ["Library", "Hostel", "Lecture Hall", "Co-working"]

    print(" Intelligent Noise Management System Starting...\n")

    for zone in zones:
        simulate_zone(agent, env, zone)

        user = input("\nPress Enter to continue or type 'q' to quit: ")
        if user.lower() == 'q':
            break


if __name__ == "__main__":
    main()