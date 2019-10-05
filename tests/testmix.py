#!/usr/bin/python3
from btpibox import *
import config
import time

print("Test mix device")
print("===============")
#print("Closing ports...")
#SerialClient.closeAllSerials()
client = SerialClient("mix", Device(config.mixId))
client.connect()
# data = client.sock.readline()
# print(data)
# data = client.sock.readline()
# print(data)
for i in range(6):
    print("Sending "+str(i)+"...")
    client.sock.write((str(i)+"\n").encode())
    print("Listening...")
    data = client.sock.readline()
    print(data)
    time.sleep(1)
client.sock.close()