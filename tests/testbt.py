#!/usr/bin/python3
print("BlueTooth Test")
print("==============")

import bluetooth
# print("Discover BT ...")
# devices = bluetooth.discover_devices(lookup_names=True, duration=5)
# print(f"Found {len(devices)} device(s)")
# print(devices)
#
# for device in devices:
#     print(f"Search services for {device} ...")
#     services = bluetooth.find_service(address=device[0])
#     print(services)
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect(("00:0E:EA:CF:47:5A", 1))
print("Receiving")
while(True):
    data = sock.recv(10)
    print(data)
sock.close()

