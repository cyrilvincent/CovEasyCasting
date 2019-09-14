#!/usr/bin/python3
from btpibox import *
import config

print("Test weight device")
print("==================")
print("Closing ports...")
SerialClient.closeAllSerials()
client = SerialClient(3, Device(config.weightId))
client.connect()
print("Listening...")
while True:
    data = client.sock.readline()
    print(data)
client.close()