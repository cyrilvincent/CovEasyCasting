#mode on windows
import serial

port="COM5"
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

