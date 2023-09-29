#import usb.core
#dev = usb.core.find()
#print(dev)

from Monsoon import HVPM

monsoon = HVPM.Monsoon()
monsoon.setup_usb()
monsoon.setVout(4.1)
