print("Pibox Scan")
print("==========")

import bluetooth
print("Discover BT ...")
devices = bluetooth.discover_devices(lookup_names=True, duration=5)
print(f"Found {len(devices)} device(s)")
print(devices)

for device in devices:
    print(f"Search services for {device} ...")
    services = bluetooth.find_service(address=device[0])
    print(services)

mac = "C8:14:51:08:8F:3A"
print(f"Find service for {mac}")
services = bluetooth.find_service(address=mac)
print(services)
for s in services:
    print(s["name"])
service = services[0]
print(service)
print(f"Connecting to {service['name']}")
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((service["host"], service["port"]))
print(f"Receiving...")
data = sock.recv(1024)
print(f"Receive {data}")

mac = "C8:14:51:08:8F:3A"
print(f"Find service for {mac}")
services = bluetooth.find_service(address=mac)
print(services)
for s in services:
    print(s["name"])
service = services[0]
print(service)
print(f"Connecting to {service['name']}")
sock2 = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock2.connect((service["host"], service["port"]))
print(f"Receiving...")
data = sock.recv(1024)
print(f"Receive {data}")

print("Closing")
sock.close()
sock2.close()

