
import random
class NoiseEnvironment:
    def __init__(self):
        self.zones=["Library","Hostel","Lecture Hall","Co-working"]
    def generate(self):
        return random.choice(self.zones), random.randint(20,90), random.randint(0,23)
