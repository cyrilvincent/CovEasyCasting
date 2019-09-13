print("Start as admin")
print("Closing...")
import serial
import serial.tools.list_ports as ls
l = ls.comports()
for p in l:
    print("Closing "+p.device)
    sock = serial.Serial(p.device)
    sock.close()
print("OK")
