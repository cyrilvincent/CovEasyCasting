port = 72
print(f"Mock BT Test {port}")
print("===============")
# netstat to see all binding port

import uuid
mac = uuid.getnode()
mac = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
print(f"Starting BT Server {mac}[{port}]...")

import bluetooth
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.bind(("",port))
sock.listen(1)
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ef"
bluetooth.advertise_service(sock, "MockBTServer72",uuid,[uuid, bluetooth.SERIAL_PORT_CLASS],[bluetooth.SERIAL_PORT_PROFILE])

print("Waiting for connection...")
clientSock, clientInfo = sock.accept()
print(f"Accepted connection from {clientInfo}")
import time
try:
    i = 1
    while i<3600:
        clientSock.send(i)
        i += 1
        time.sleep(1)
except IOError as ex:
    print(f"Error: {ex}")

clientSock.close()
sock.close()

