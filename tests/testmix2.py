from btpibox import *
import config
import time

print("Test mix device multithread")
print("===========================")
client = SerialClient(3, Device(config.mixSerial))
server = BTServer((client,))
client.start()
time.sleep(2)
server.phoneEvent(client.device, 1)
time.sleep(2)
client.stop()