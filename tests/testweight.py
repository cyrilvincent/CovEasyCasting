from btpibox import *
import config

print("Test weight device")
print("==================")
print("Closing ports...")
SerialClient.closeAllSerials()
client = SerialClient(3, Device(config.weightId))
client.connect()
print("Listening...")
for _ in range(10):
    data = client.sock.readline()
    print(data)
client.close()