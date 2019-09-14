#!/usr/bin/python3
print("Seeeduino tempbt Test")
print("=====================")

import bluetooth
def readline(self):
    s = ""
    while(True):
        data = self.recv(1).decode()
        s += data
        if data == '\r':
            data = self.recv(1).decode()
            s += data
            if data == '\n':
                break
    return s

def readline1024(self):
    s = ""
    while(True):
        data = self.recv(1024).decode()
        s += data
        if '\r\n' in data:
            break;
    return s

mac = "00:0E:EA:CF:58:B8"
print(f"Connecting to {mac}")
bluetooth.BluetoothSocket.readline = readline1024
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#sock.readline = readline
sock.connect((mac, 1))
print("Receiving")
while(True):
    #data = sock.recv(1024)
    data = sock.readline()
    print(float(data))
sock.close()
print("Close")

