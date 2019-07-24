import serial
sock = serial.Serial("COM1")
sock.close()
sock = serial.Serial("COM2")
sock.close()
