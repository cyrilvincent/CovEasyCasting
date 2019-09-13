print("Pibox 3 Test")
print("============")

mac = "C8:14:51:08:8F:3A"
port = 3

print(f"Connecting to {mac}[{port}]...")
import bluetooth
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((mac, port))
while True:
    data = sock.recv(1024)
    print(f"Receive {data}")
sock.close()




