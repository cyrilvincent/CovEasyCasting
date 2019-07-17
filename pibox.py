import threading
import bluetooth
import uuid
import time
from typing import List, Tuple

class BTDevice:

    def __init__(self, mac="", port=0, isConnected = False):
        self.mac = mac
        self.port = port
        self.isConnected = isConnected

    def __repr__(self):
        return f"{self.mac}[{self.port}]"

class BTClient(threading.Thread):

    def __init__(self, device:BTDevice, cb):
        self.device = device
        self.stop = False
        self.sock:bluetooth.BluetoothSocket = None
        self.cb = cb
        self.data = 0

    def connect(self):
        print(f"Connecting to {self.device}")
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((self.device.mac, self.device.port))
        print(f"Connected to {self.device}")
        self.device.isConnected = True

    def run(self) -> None:
        while(not self.stop):
            try:
                self.data = self.sock.recv(1024)
                print(f"{self.device}->{self.data}")
                self.cb(self.device, self.data)
            except IOError:
                self.device.isConnected = False
                self.stop = True
        try:
            self.sock.close()
        except:
            pass

    def stop(self):
        self.stop = True

    def close(self):
        try:
            self.sock.close()
            self.stop = False
            self.device.isConnected = False
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
        self.devices = BTDevices
        self.device = BTDevice(self.getMac(), port)
        self.deviceClients:List[BTClient] = []
        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ff"
        self.sock = None
        self.service = service
        self.mainClient:BTDevice = BTDevice()

    def receiveEvent(self, device:BTDevice, data):
        print(f"PiBox Received {device}->{data}")
        if self.mainClient.isClientConnected:
            try:
                json = self.makeJson()
                self.sock.send(json)
                print(f"Sending {json}")
                self.nbIOError = 0
            except IOError as ex:
                print(f"IOError {ex}")
                self.listen()

    def makeJson(self):
        json = "{t:" + self.deviceClients[0].data + ","
        json += "p:" + self.deviceClients[1].data + ","
        json += "w:" + self.deviceClients[2].data + "}"
        return json

    def startClients(self):
        for device in self.devices:
            client = BTClient(device)
            client.connect()
            self.deviceClients.append(client)

    def stopClients(self):
        for client in self.deviceClients:
            client.stop()

    def stopForceClient(self):
        self.stopClients()
        for client in self.deviceClients:
            del client

    def getMac(self):
        mac = uuid.getnode()
        mac = ':'.join(("%012X" % mac)[i:i + 2] for i in range(0, 12, 2))
        return mac

    def createServer(self):
        print(f"Starting server {self.device}")
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.bind(("", self.port))
        self.sock.listen(1) # One connection at a time
        print("Server {self.device} Ok")
        bluetooth.advertise_service(self.sock, self.service , self.uuid, [self.uuid, bluetooth.SERIAL_PORT_CLASS],
                                    [bluetooth.SERIAL_PORT_PROFILE])
        print(f"Service {self.service} Ok")

    def listen(self):
        self.isClientConnected = False
        print("Waiting for connection...")
        clientSock, clientInfo = self.sock.accept()
        print(f"Accepted connection from {clientInfo}")
        self.mainClient = BTDevice(clientInfo, 0, True)

    def stop(self):
        self.stopClients()
        try:
            self.sock.close()
        except:
            pass

    def __del__(self):
        self.stop()

    def __enter__(self):
        self.createServer()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __repr__(self):
        return f"BTServer {self.mainClient}<->{self.device}<-{self.devices}"


if __name__ == '__main__':
    server = BTServer((
        BTDevice("C8:14:51:08:8F:3A", 1),
        BTDevice("C8:14:51:08:8F:3A", 1),
        BTDevice("C8:14:51:08:8F:3A", 1),
    ))
    print(server)
    server.startClients()
    print(server)
    server.createServer()
    print(server)
    server.listen()
    # Gérer toutes les pannes en boucle infinies




