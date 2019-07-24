import serial

print("Read COM2")
sock = serial.Serial("COM2")
for i in range(10):
    s = sock.readline()
    print(s)
sock.close()

#echo hello > COM1
# or
# sock = serial.Serial("COM1")
# sock.write(b"hello COM1\n")
# sock.close()

