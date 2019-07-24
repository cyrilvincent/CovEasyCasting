print("PiBox Devices Test")
print("==================")

print("Testing Python libraries...")
import bluetooth
import config
from btpibox import *

# print("Connecting to temperature device...")
# device = Device(config.tempMac, config.tempPort)
# client = BTClient(1,device)
# client.connect()
# client.close()

# print("Connecting to preasure device...")
# device = Device(config.preasureMac, config.preasurePort)
# client = BTClient(2,device)
# client.connect()
# client.close()

print("Connecting to weight device...")
device = Device(config.weightMac, name = config.weightBTName)
client = BTClient(3,device)
client.connect()
client.close()

# print("Connecting to mix device...")
# device = Device(config.mixMac, config.mixPort)
# client = BTClient(4,device)
# client.connect()
# client.close()

print("Connecting to phone device...")
device = Device(config.phoneMac, name = config.phoneBTName)
client = BTClient(0,device)
client.connect()
client.close()

print("All devices are OK start consolepibox.py to test the Server")

