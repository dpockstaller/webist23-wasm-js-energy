import time


class DummyEnergyMeter:

    def __init__(self):
        self.start_metering = 0
        self.duration = 0

    def setup(self, voltage=0):
        pass

    def start(self):
        self.start_metering = time.time()

    def stop(self):
        self.duration = time.time() - self.start_metering
        self.start_metering = 0

    def measurements(self):
        return {'duration': self.duration, 'energy': 123.123}
