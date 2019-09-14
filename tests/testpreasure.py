#!/usr/bin/python3
from btpibox import *
import config

print("Test preasure device")
print("====================")
client = BTClient(2, Device(config.preasureId, name=config.preasureBTName))
client.connect()
print("Listening...")
while True:
    data = client.sock.recv(1024)
    print(data)
client.close()