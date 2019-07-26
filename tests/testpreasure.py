from btpibox import *
import config

print("Test preasure device")
print("====================")
client = BTClient(2, Device(config.preasureId, name=config.preasureBTName))
client.connect()
print("Listening...")
for _ in range(10):
    data = client.sock.recv(1024)
    print(data)
client.close()