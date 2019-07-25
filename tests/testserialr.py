#mode on windows
import serial

print("Read COM1")
sock = serial.Serial("COM1")
s = sock.readline()
print(s)
sock.close()

#echo hello > COM2
# or
# sock = serial.Serial("COM1")
# sock.write(b"hello COM1\n")
# sock.close()

