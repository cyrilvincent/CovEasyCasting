#!/usr/bin/python3
import serial

port="/dev/ttyUSB0"
print("Read "+port)
sock = serial.Serial(port)
while(True):
    s = sock.readline()
    print(s)
sock.close()

#echo hello > COM2
# or
# sock = serial.Serial("COM1")
# sock.write(b"hello COM1\n")
# sock.close()

