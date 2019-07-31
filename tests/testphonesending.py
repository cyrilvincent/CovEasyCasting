port = 3
print("Test Phone sending")
print("==================")

import uuid
mac = uuid.getnode()
mac = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
print("Starting BT Server "+mac+" "+str(port)+"...")

import bluetooth
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.bind(("",port))
sock.listen(1)
uuid = "94329d29-7d6d-437d-973b-fba39e49d4ee"
bluetooth.advertise_service(sock, "PhoneSending",uuid,[uuid, bluetooth.SERIAL_PORT_CLASS],[bluetooth.SERIAL_PORT_PROFILE])

print("Waiting for connection...")
clientSock, clientInfo = sock.accept()
print("Accepted connection from "+str(clientInfo))
while True:
    i = int(input("Input int value: "))
    clientSock.send((str(i) + "\n").encode())
    print("Sended "+str(i))
clientSock.close()
sock.close()