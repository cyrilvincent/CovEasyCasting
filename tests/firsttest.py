#!/usr/bin/python3
print("PiBox Devices Test")
print("==================")

print("Testing Python libraries...")
import bluetooth
import config
import serial
from btpibox import *

print("Connecting to temperature device...")
device = Device(config.tempMac, config.tempPort)
client = BTClient(1,device)
client.connect()
client.close()

print("Connecting to preasure device...")
device = Device(config.preasureId, name = config.preasureBTName)
client = BTClient(2,device)
client.connect()
client.close()

print("Connecting to weight device...")
device = Device(config.weightId)
client = SerialClient(3,device)
client.connect()
client.close()

print("Connecting to mix device...")
device = Device(config.mixId)
client = BTClient(4,device)
client.connect()
client.close()

print("Connecting to phone device...")
device = Device(config.phoneId, name = config.phoneBTName)
client = BTClient(0,device)
client.connect()
client.close()

print("All connections to devices are OK start unittestspibox.py to test communications and consolepibox.py to test the Server")

