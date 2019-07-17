print("BlueTooth Test")
print("==============")

import bluetooth
print("Discover BT ...")
devices = bluetooth.discover_devices(lookup_names=True, duration=5)
print(f"Found {len(devices)} device(s)")
print(devices)

try:
    import bluetooth.ble as ble
    print("Discover BT LTE ...")
    service = ble.DiscoveryService()
    ltes = service.discover(2)
    print(f"Found {len(ltes)} LTE device(s)")
    print(ltes)
except:
    print("BT LTE Failed")

for device in devices:
    print(f"Search services for {device} ...")
    services = bluetooth.find_service(address=device[0])
    print(services)

