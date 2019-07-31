print("BlueTooth LE Test")
print("=================")

import bluetooth.ble as ble
print("Discover BT LTE ...")
service = ble.DiscoveryService()
ltes = service.discover(2)
print(f"Found {len(ltes)} LTE device(s)")
print(ltes)


