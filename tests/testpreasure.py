#!/usr/bin/python3
from btpibox import *
import config

print("Test preasure device")
print("====================")
client = SerialClient(2, Device("COM8"))
client.connect()
print("Listening...")
while True:
    data = client.sock.readline()
    print(data)
client.close()