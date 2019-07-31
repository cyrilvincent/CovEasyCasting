from btpibox import *
import config

print("Test phone device")
print("=================")
client = BTClient(0, Device(config.phoneId, name = config.phoneBTName))
client.connect()
print("Listening...")
while True:
    data = client.sock.recv(1024)
    print(data)
client.close()