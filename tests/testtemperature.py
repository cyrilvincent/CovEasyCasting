#!/usr/bin/python3
from btpibox import *
import config

print("Test temperature device")
print("=======================")
client = BTClient(1, Device(config.tempId, config.tempId))
client.connect()
print("Listening...")
while True:
    data = client.sock.recv(1024)
    print(data)
client.close()