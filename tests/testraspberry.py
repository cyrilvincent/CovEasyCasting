print("Raspberry Test")
print("==============")

mac = "DC:A6:32:23:9A:7E"
print(f"Search services for {mac} ...")
import bluetooth
# services = bluetooth.find_service(address=mac)
# services = [s for s in services if s["protocol"]=="RFCOMM"]
# print(services)
# for s in services:
#     print((s["name"],s["port"]))
# service = [s for s in services if "BTSPPServer" in str(s["name"])][0]
# print(service)
# print(f"Connecting to {service}")
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((mac, 1))
print("Receiving")
while(True):
    data = sock.recv(10)
    print(data)
sock.close()
print("Close")
