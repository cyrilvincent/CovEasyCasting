import threading
import bluetooth
import uuid
from typing import List, Tuple

class BTDevice:

    def __init__(self, mac="00:00:00:00:00:00", port=0, isConnected = False):
        self.mac = mac
        self.port = port
        self.isConnected = isConnected
        self.isDialog = False
        self.isDown = False

    def __repr__(self):
        return f"{self.mac}[{self.port}]"

class BTClient(threading.Thread):

    def __init__(self, device:BTDevice, cb):
        super().__init__()
        self.device = device
        self.sock:bluetooth.BluetoothSocket = None
        self.cb = cb
        self.data = 0

    def connect(self):
        print(f"Connecting to {self.device}")
        try:
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.sock.connect((self.device.mac, self.device.port))
            self.device.isDown = False
            print(f"Connected to {self.device}")
            self.device.isConnected = True
        except IOError:
            self.device.isDown = True
            print(f"{self.device} is Down")

    def run(self) -> None:
        self.device.isDialog = True
        while(self.device.isDialog):
            try:
                self.data = self.sock.recv(1024)
                print(f"{self.device}->{self.data}")
                self.cb(self.device, self.data)
            except IOError:
                self.device.isConnected = False
                self.device.isDialog = False
        try:
            self.sock.close()
        except:
            pass

    def stop(self):
        self.device.isDialog = False

    def close(self):
        try:
            self.device.isDialog = False
            self.device.isConnected = False
            self.sock.close()
        except:
            pass

    def __enter__(self):
        self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def __repr__(self):
        return f"BTClient {self.device}->{self.device.isConnected}"

class BTServer:

    def __init__(self, BTDevices:Tuple[BTDevice], port=72, service = "EasyCastingBox"):
        """
        :param BTDevices: item 1 = temperature, item 2 = preasure, item 3 = weight
        :param port: port of the server
        :param service: name of the service
        """
        self.device:BTDevice= BTDevice(self.getMac(), port)
        self.deviceClients:List[BTClient] = [BTClient(d, self.receiveEvent) for d in BTDevices]
        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ff"
        self.service = service
        self.mainClient:BTDevice = BTDevice()
        self.port = port

    def receiveEvent(self, device:BTDevice, data):
        print(f"PiBox Received {device}->{data}")
        if self.mainClient.isConnected:
            try:
                json = self.makeJson()
                self.device.sock.send(json)
                print(f"Sending {json}")
            except IOError as ex:
                print(f"IOError {ex}")
                self.listen()

    def makeJson(self):
        json = "{t:" + self.deviceClients[0].data + ","
        json += "p:" + self.deviceClients[1].data + ","
        json += "w:" + self.deviceClients[2].data + "}"
        return json

    def connectClient(self, num):
        self.deviceClients[num].connect()

    def connectClients(self):
        for client in self.deviceClients:
            client.connect()

    def dialogClient(self, num):
        self.deviceClients[num].start()

    def dialogClients(self):
        for client in self.deviceClients:
            client.start()

    def stopClients(self):
        for client in self.deviceClients:
            client.stop()

    def stopClient(self, num):
        self.deviceClients[num].stop()

    def stopForceClient(self):
        self.stopClients()
        for client in self.deviceClients:
            del client

    def getMac(self):
        mac = uuid.getnode()
        mac = ':'.join(("%012X" % mac)[i:i + 2] for i in range(0, 12, 2))
        return mac

    def createServer(self, nbClient = 1):
        print(f"Starting server {self.device}")
        self.device.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.device.sock.bind(("", self.port))
        self.device.sock.listen(nbClient)
        print(f"Server {self.device} Ok")
        bluetooth.advertise_service(self.device.sock, self.service , self.uuid, [self.uuid, bluetooth.SERIAL_PORT_CLASS],
                                    [bluetooth.SERIAL_PORT_PROFILE])
        print(f"Service {self.service} Ok")

    def listen(self):
        self.mainClient.isConnected = False
        print("Waiting for connection...")
        clientSock, clientInfo = self.device.sock.accept()
        self.mainClient.mac = clientInfo
        self.mainClient.isConnected = True
        self.mainClient.isDialog = True
        print(f"Accepted connection from {self.mainClient}")
        json = self.makeJson()
        self.device.sock.send(json)
        print(f"Sending {json}")

    def stop(self):
        self.stopClients()
        try:
            self.device.close()
        except:
            pass

    def __del__(self):
        self.stop()

    def __enter__(self):
        self.createServer()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __repr__(self):
        return f"BTServer {self.mainClient}<->{self.device}<-{self.deviceClients}"


if __name__ == '__main__':
    server = BTServer((
        BTDevice("C8:14:51:08:8F:3A", 1),
        BTDevice("C8:14:51:08:8F:3A", 1),
        BTDevice("C8:14:51:08:8F:3A", 1),
    ))
    print(server)
    server.connectClients()
    print(server)
    server.dialogClients()
    print(server)
    server.createServer()
    print(server)
    server.listen()
    # Gérer toutes les pannes en boucle infinies




