port = 0
print("Mock BT Server Test "+str(port))
print("=====================")
#https://docs.microsoft.com/en-us/windows/win32/bluetooth/bluetooth-and-bind

import uuid
mac = uuid.getnode()
mac = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
print("Starting BT Server "+mac+" "+str(port)+" ...")

import bluetooth
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.bind(("",port))
port = sock.getsockname()[1]
print("Started BT Server "+mac+" "+str(port)+" ...")
sock.listen(1)
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
bluetooth.advertise_service(sock, "pibox",uuid,[uuid, bluetooth.SERIAL_PORT_CLASS],[bluetooth.SERIAL_PORT_PROFILE])

print("Waiting for connection...")
clientSock, clientInfo = sock.accept()
print("Accepted connection from "+str(clientInfo))
import time
try:
    i = 1
    while i<3600:
        clientSock.send((str(i)+"\n").encode())
        i += 1
        time.sleep(1)
except IOError as ex:
    print("Error: "+str(ex))

clientSock.close()
sock.close()