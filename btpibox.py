import threading
import bluetooth
import uuid
import time

from genericpibox import *
from serialpibox import *
from typing import List, Tuple

class BTClient(SerialClient):

    def __init__(self, id:int, device:Device, cb = lambda device, data : 0):
        super().__init__(id,device,cb)

    def connect(self):
        print(f"Connecting to {self.device}")
        try:
            if self.device.port == 0:
                self.findPort()
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.sock.connect((self.device.id, self.device.port))
            print(f"Connected to {self.device}")
            self.status = -1
        except IOError:
            self.status = -4
            print(f"{self.device} is Down")

    def findPort(self):
        try:
            services = bluetooth.find_service(address=self.device.id)
            service = [s for s in services if self.device.name in str(s["name"])][0]
            self.device.port = int(service["port"])
        except:
            self.status = -4


    def run(self) -> None:
        while(True):
            if self.status < -1:
                self.connect()
            while(self.status >= -1):
                try:
                    data = self.sock.recv(1024)
                    self.status = 0
                    print(str(self.device)+"->"+str(data))
                    self.data = float(data)
                    self.cb(self.device, self.data)
                except ValueError:
                    pass
                except IOError:
                    self.status = -3
            try:
                self.sock.close()
                self.status = min(-2, self.status)
            except:
                pass
            time.sleep(10)

    def __repr__(self):
        return "BTClient"+str(self.id)+"("+str(self.status)+")"+str(self.device)

class BTServer(AbstractServer, BTClient):

    def __init__(self, devices:Tuple[Device], port=72, service = "EasyCastingBox"):
        BTClient.__init__(self, 0, Device(self.getMac(), port))
        self.clients:List[BTClient] = [BTClient(i, d) for i, d in enumerate(devices)]
        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ff"
        self.service = service
        self.sock:bluetooth.BluetoothSocket = None

    def emit(self):
        while True:
            try:
                json = self.makeJson()
                print(f"Sending {json}")
                self.sock.send(json)
                self.status = 0
            except IOError as ex:
                self.status = -3
                time.sleep(10)
                self.connect()
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
        self.status = min(-2, self.status)
        print("Waiting for connection...")
        clientSock, clientInfo = self.sock.accept()
        self.id = clientInfo
        self.status = -1
        print(f"Accepted connection from {self}")
        json = self.makeJson()
        self.sock.send(json)
        print(f"Sending {json}")
        self.status = 0
        self.emit()

    def stop(self):
        self.stopClients()
        try:
            self.device.close()
            self.sock.close()
            self.status = -2
        except:
            pass

    def __repr__(self):
        return "BTServer "+str(self.clients[0].device)+"<-"+str(self.device)+"<-"+str(self.clients[1:])


if __name__ == '__main__':
    server = BTServer((
        Device("C8:14:51:08:8F:3A", 5),
        Device("C8:14:51:08:8F:3A", 5),
        Device("C8:14:51:08:8F:3A", 4),
        Device("C8:14:51:08:8F:00", 2),
        Device("C8:14:51:08:8F:3A", 5),
    ))
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




