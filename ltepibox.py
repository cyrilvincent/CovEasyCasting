import threading
import bluetooth
import uuid
import time

from abstractpibox import *
from typing import List, Tuple

"""
Etudier bluez543
D:\CVC\Covestro\EasyCasting\bluez-5.43\test\example-gatt-*
Sur Raspbian : https://scribles.net/running-ble-gatt-server-example-on-raspbian-stretch/#Step01

"""
class LTEClient(AbstractClient):

    def __init__(self, id:int, device:Device, cb = lambda device, data : 0):
        super().__init__(id,device,cb)

    def connect(self):
        print(f"Connecting to {self.device}")
        try:
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.sock.connect((self.device.id, self.device.port))
            print(f"Connected to {self.device}")
            self.status = 1
        except IOError:
            self.status = -1
            print(f"{self.device} is Down")

    def run(self) -> None:
        if self.status == 1:
            self.status = 2
        while(self.status > 1):
            try:
                self.data = self.sock.recv(1024)
                print(f"{self.device}->{self.data}")
                self.cb(self.device, self.data)
            except IOError:
                self.status = -2
        try:
            self.status = 0
            self.sock.close()
        except:
            pass

    def close(self):
        try:
            self.status = 0
            self.sock.close()
        except:
            pass

    def __repr__(self):
        return "BTClient"+str(self.id)+"("+str(self.status)+")"+str(self.device)

class BTServer(AbstractServer):

    def __init__(self, devices:Tuple[Device], port=72, service = "EasyCastingBox"):
        """
        :param BTDevices: item 1 = temperature, item 2 = preasure, item 3 = weight
        :param port: port of the server
        :param service: name of the service
        """
        self.device:Device= Device(self.getMac(), port)
        self.clients:List[BTClient] = [BTClient(i + 1, d) for i, d in enumerate(devices)]
        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ff"
        self.service = service
        self.mainClient:BTClient = BTClient(0, Device())
        self.sock:bluetooth.BluetoothSocket = None

    def _receiveEvent(self, device:Device, data):
        print(f"PiBox Received {device}->{data}")
        if self.mainClient.status > 0:
            try:
                json = self.makeJson()
                self.sock.send(json)
                print(f"Sending {json}")
            except IOError as ex:
                pass

    def emit(self):
        while True:
            try:
                json = self.makeJson()
                self.sock.send(json)
                print(f"Sending {json}")
                self.mainClient.status = 2
            except IOError as ex:
                self.mainClient.status = -2
            time.sleep(1)

    def connectClient(self, num):
        self.clients[num].connect()

    def connectClients(self):
        for client in self.clients:
            client.connect()

    def dialogClient(self, num):
        self.clients[num].start()

    def dialogClients(self):
        for client in self.clients:
            client.start()

    def stopClients(self):
        for client in self.clients:
            client.stop()

    def stopClient(self, num):
        self.clients[num].stop()

    def stopForceClient(self):
        self.stopClients()
        for client in self.clients:
            del client

    def createServer(self, nbClient = 1):
        print(f"Starting server {self.device}")
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.bind(("", self.device.port))
        self.sock.listen(nbClient)
        print(f"Server {self.device} Ok")
        bluetooth.advertise_service(self.sock, self.service , self.uuid, [self.uuid, bluetooth.SERIAL_PORT_CLASS],
                                    [bluetooth.SERIAL_PORT_PROFILE])
        print(f"Service {self.service} Ok")

    def listen(self):
        self.mainClient.status = 0
        print("Waiting for connection...")
        clientSock, clientInfo = self.sock.accept()
        self.mainClient.mac = clientInfo
        self.mainClient.status = 1
        print(f"Accepted connection from {self.mainClient}")
        json = self.makeJson()
        self.sock.send(json)
        print(f"Sending {json}")
        self.mainClient.status = 2
        self.emit()

    def stop(self):
        self.stopClients()
        try:
            self.device.close()
            self.sock.close()
        except:
            pass

    def __repr__(self):
        return "BTServer "+str(self.mainClient)+"<-"+str(self.device)+"<-"+str(self.clients)


if __name__ == '__main__':
    server = BTServer((
        Device("C8:14:51:08:8F:3A", 4),
        Device("C8:14:51:08:8F:00", 1),
        Device("C8:14:51:08:8F:00", 2),
    ))
    print(server)
    print("Connecting to devices")
    server.connectClients()
    print(server)
    print("Dialog to devices")
    server.dialogClients()
    print(server)
    print("Create BT server")
    server.createServer()
    print(server)
    print("Listening")
    server.listen()
    print("Stop")




