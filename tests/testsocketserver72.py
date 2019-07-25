port = 72
print("Mock BT by Socket Test "+str(port))
print("=========================")

import uuid
mac = uuid.getnode()
mac = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
print("Starting BT Server "+mac+" "+str(port)+"...")

import socket
print(socket.AF_BLUETOOTH)
sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
sock.bind(("",port))
sock.listen(1)

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

