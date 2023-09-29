import time
import argparse
import random
from experiment import tap, MonsoonEnergyMeter, DummyEnergyMeter, Writer, clear_browser, open_browser, screen_brightness, unlock, get_device_model

parser = argparse.ArgumentParser(description='WASM Energy Experiment')
parser.add_argument('-m', '--meter', type=str, help='Energy metering approach: monsoon, batterystats, dummy', default="monsoon")
parser.add_argument('-f', '--filename', type=str, help='Filename of results', default="measurements.txt")
parser.add_argument('-c', '--count', type=int, help='Number of executions', default=1)
args = parser.parse_args()

browsers = ['chrome', 'firefox']
types = ['js', 'c']
algorithms = [
    'ackermann', 'bubblesort', 'countingsort', 'fibonacci',
    'gnomesort', 'happynumbers', 'heapsort', 'insertionsort',
    'humblenumbers', 'kmeanspp', 'matrixmultiplication',
    'mergesort', 'nqueens', 'pancakesort', 'perfectnumbers',
    'quicksort', 'seqnonsquares', 'shellsort', 'towersofhanoi'
]
device_model = get_device_model()

writer = Writer(args.filename)

meter = DummyEnergyMeter()
if args.meter == "monsoon":
    meter = MonsoonEnergyMeter()
meter.setup()


def get_url(type='js', algorithm='bubblesort'):
    return "https://wasm-energy-experiment.netlify.app/{}/{}/energy.html".format(type, algorithm)


def get_settings():
    s = []

    for browser in browsers:
        for type in types:
            for algorithm in algorithms:
                s.append((browser, type, algorithm, get_url(type, algorithm)))

    return s


def get_randomized_settings():
    s = get_settings()
    random.shuffle(s)
    return s


def execution(browser, type, algorithm, url):

    print("START: {}, {}, {}".format(browser, type, algorithm))

    # prepare device
    clear_browser(browser)
    time.sleep(1)
    open_browser(browser, url)
    time.sleep(10)
   
    # start algorithm
    meter.start()
    tap(500, 300)
    time.sleep(5)
    meter.stop()
    result = meter.measurements()
    print("   algo energy: {}".format(result['energy']))

    # write results    
    writer.write([browser, type, algorithm, device_model, str(result['energy'])])


unlock()
unlock()
screen_brightness(0.3)


for i in range(args.count):
    settings = get_randomized_settings()
    for setting in settings:
        execution(*setting)
