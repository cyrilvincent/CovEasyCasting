port = 50
print("Mock BT Test "+str(port))
print("===============")
# netstat to see all binding port

import uuid
mac = uuid.getnode()
mac = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
print("Starting BT Server "+mac+" "+str(port)+"...")

import bluetooth
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.bind(("",port))
sock.listen(1)
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
bluetooth.advertise_service(sock, "MockBTServer50",uuid,[uuid, bluetooth.SERIAL_PORT_CLASS],[bluetooth.SERIAL_PORT_PROFILE])
# si bug https://www.raspberrypi.org/forums/viewtopic.php?t=132470

print("Waiting for connection...")
clientSock, clientInfo = sock.accept()
print("Accepted connection from "+clientInfo)
import time
try:
    i = 1
    while i<3600:
        clientSock.send(i)
        i += 1
        time.sleep(1)
except IOError as ex:
    print("Error: "+str(ex))

clientSock.close()
sock.close()

