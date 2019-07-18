print("Huawei Test")
print("===========")

mac = "C8:14:51:08:8F:3A"
print(f"Search services for {mac} ...")
import bluetooth
services = bluetooth.find_service(address=mac)
print(services)
for s in services:
    print(s["name"])
service = services[-4] # [s for s in services if "SMS/MMS" in s["name"]]
print(service)
print(f"Connecting to {service['name']}")
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((service["host"], service["port"]))
# print("Sending AT")
# sock.send('AT\r')
# sock.send('AT+CMGF=1\r')
# sock.send('AT+CMGL="ALL"\r')
# print("Receiving")
# data = sock.recv(10)
# print(data)
# sock.close()
# print("Close")

# dest = "0622538762"
# text = "Python"
# sock.send('AT+CMGF=1\r')
# sock.send("AT+CMGS=\"%s\"\r" % dest)
# sock.send("%s%s" % (text,chr(0o32)))
# sock.close()




