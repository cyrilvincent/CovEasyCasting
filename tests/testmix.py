#!/usr/bin/python3
from btpibox import *
import config
import time

print("Test mix device")
print("===============")
print("Closing ports...")
SerialClient.closeAllSerials()
client = SerialClient(3, Device(config.mixId))
client.connect()
for i in range(6):
    print("Sending "+str(i)+"...")
    client.sock.write((str(i)+"\n").encode())
    #time.sleep(0.5)
    #client.sock.close()
    #client.sock.open()
    print("Listening...")
    data = client.sock.readline()
    print(data)
    time.sleep(1)
client.sock.close()