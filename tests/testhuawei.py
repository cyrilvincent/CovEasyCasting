print("Huawei Test")
print("===========")

mac = "C8:14:51:08:8F:3A"
print(f"Search services for {mac} ...")
import bluetooth
services = bluetooth.find_service(address=mac)
services = [s for s in services if s["protocol"]=="RFCOMM"]
print(services)
for s in services:
    print((s["name"],s["port"]))
service = [s for s in services if "BTSPPServer" in str(s["name"])][0]
print(service)
print(f"Connecting to {service}")
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((service["host"], service["port"]))
print("Receiving")
while(True):
    data = sock.recv(10)
    print(data)
sock.close()
print("Close")
