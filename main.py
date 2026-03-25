import asyncio
import spade
import sys
import os
import contextlib
from agents.noise_agent import NoiseAgent
from agents.supervisor_agent import SupervisorAgent

# Helper to suppress the low-level XML/XMPP handshake errors
@contextlib.contextmanager
def mute_outputs():
    with open(os.devnull, 'w') as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr

async def main():
    noise_jid = "noise@localhost"
    supervisor_jid = "supervisor@localhost"
    password = "password"

    noise_agent = NoiseAgent(noise_jid, password)
    supervisor_agent = SupervisorAgent(supervisor_jid, password)

    print("\n" + "="*30)
    print(" NOISE MANAGEMENT SYSTEM: STARTING ---")
    print("="*30)
    
    # We mute ONLY the startup phase where the XML errors happen
    with mute_outputs():
        await supervisor_agent.start(auto_register=True)
        await noise_agent.start(auto_register=True)

    print("\n[SUCCESS] Agents are connected and synchronized.")
    print("[INFO] Monitoring zones... Press Ctrl+C to exit.\n")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Shutting down agents...")
        await noise_agent.stop()
        await supervisor_agent.stop()
        print("[X] System offline.")

if __name__ == "__main__":
    # The embedded server starts here
    spade.run(main(), embedded_xmpp_server=True)