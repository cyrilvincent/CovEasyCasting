print("BlueTooth Test")
print("==============")

import bluetooth
print("Discover BT ...")
devices = bluetooth.discover_devices(lookup_names=True, duration=5)
print(f"Found {len(devices)} device(s)")
print(devices)

for device in devices:
    print(f"Search services for {device} ...")
    services = bluetooth.find_service(address=device[0])
    print(services)

