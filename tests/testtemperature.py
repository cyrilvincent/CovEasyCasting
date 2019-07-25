from btpibox import *
import config

print("Test temperature device")
print("=======================")
client = BTClient(1, Device(config.tempMac, config.tempMac))
client.connect()
print("Listening...")
for _ in range(10):
    data = client.sock.recv(1024)
    print(data)
client.close()