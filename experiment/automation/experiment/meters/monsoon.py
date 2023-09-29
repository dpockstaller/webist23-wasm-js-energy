from Monsoon import HVPM, sampleEngine
from Monsoon.sampleEngine import triggers
from threading import Thread
import numpy as np


class MonsoonEnergyMeter:
    def __init__(self):
        self.monsoon = HVPM.Monsoon()
        self.engine = None
        self.monsoon_reader = None
        self.samples = None

    def setup(self, voltage=4.2):
        self.monsoon.setup_usb()
        self.monsoon.setVout(voltage)
        self.engine = sampleEngine.SampleEngine(self.monsoon)
        self.engine.ConsoleOutput(False)
        self.engine.disableCSVOutput()

    def start(self):
        self.monsoon_reader = MonsoonReader(self.engine)
        self.monsoon_reader.start()

    def stop(self):
        self.monsoon_reader.stop()
        self.samples = self.engine.getSamples()

    def measurements(self):
        timestamps = self.samples[sampleEngine.channels.timeStamp]
        time_deltas = [j - i for i, j in zip(timestamps[:-1], timestamps[1:])]
        current = np.array(self.samples[sampleEngine.channels.MainCurrent]) / 1000  # mA to A conversion
        voltage = np.array(self.samples[sampleEngine.channels.MainVoltage])
        duration = timestamps[-1]
        energy_consumption = np.sum(np.array(current[:-1]) * np.array(time_deltas) * np.array(voltage[:-1]))

        #power = current * voltage  # Watts
        #energy_consumption = np.sum(power) * duration  # E[J] = P[W] × t[s]
        return {'duration': duration, 'energy': energy_consumption}


class MonsoonReader(Thread):
    def __init__(self, monsoon_engine):
        super(MonsoonReader, self).__init__()
        self.monsoon_engine = monsoon_engine

    def prepare(self):
        pass

    def run(self):
        self.monsoon_engine.startSampling(triggers.SAMPLECOUNT_INFINITE)

    def stop(self):
        self.monsoon_engine._SampleEngine__stopTriggerSet = True
        self.join()
