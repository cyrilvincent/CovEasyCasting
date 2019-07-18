import threading
import bluetooth
import uuid
import time

from typing import List, Tuple

class BTDevice:

    def __init__(self, mac="00:00:00:00:00:00", port=0):
        self.mac = mac
        self.port = port

    def __repr__(self):
        return f"{self.mac}[{self.port}]"

class BTClient(threading.Thread):

    def __init__(self, id:int, device:BTDevice, cb = lambda device, data : 0):
        super().__init__()
        self.id = id
        self.device = device
        self.sock:bluetooth.BluetoothSocket = None
        self.data = -1
        self.cb = cb
        self.status = 0 # 0 = Not connected, 1 = Connected, 2 = Dialog, -1 = Down, -2 = Disconnected

    def connect(self):
        print(f"Connecting to {self.device}")
        try:
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.sock.connect((self.device.mac, self.device.port))
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

    def stop(self):
        self.status = 1

    def close(self):
        try:
            self.status = 0
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
        return f"BTClient{self.id}({self.status}){self.device}"

class BTServer:

    def __init__(self, BTDevices:Tuple[BTDevice], port=72, service = "EasyCastingBox"):
        """
        :param BTDevices: item 1 = temperature, item 2 = preasure, item 3 = weight
        :param port: port of the server
        :param service: name of the service
        """
        self.device:BTDevice= BTDevice(self.getMac(), port)
        self.clients:List[BTClient] = [BTClient(i + 1, d) for i, d in enumerate(BTDevices)]
        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ff"
        self.service = service
        self.mainClient:BTClient = BTClient(0, BTDevice())

    def _receiveEvent(self, device:BTDevice, data):
        print(f"PiBox Received {device}->{data}")
        if self.mainClient.status > 0:
            try:
                json = self.makeJson()
                self.device.sock.send(json)
                print(f"Sending {json}")
            except IOError as ex:
                pass

    def emit(self):
        while True:
            try:
                json = self.makeJson()
                self.device.sock.send(json)
                print(f"Sending {json}")
                self.mainClient.status = 2
            except IOError as ex:
                self.mainClient.status = -2
            time.sleep(1)

    def makeJson(self):
        json = "{t:" + self._getData(self.clients[1]) + ","
        json += "p:" + self._getData(self.clients[2]) + ","
        json += "w:" + self._getData(self.clients[3]) + "}"
        return json

    def _getData(self,device):
        if device.status < 0:
            return device.status
        else:
            return device.data

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

    def getMac(self):
        mac = uuid.getnode()
        mac = ':'.join(("%012X" % mac)[i:i + 2] for i in range(0, 12, 2))
        return mac

    def createServer(self, nbClient = 1):
        print(f"Starting server {self.device}")
        self.device.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.device.sock.bind(("", self.device.port))
        self.device.sock.listen(nbClient)
        print(f"Server {self.device} Ok")
        bluetooth.advertise_service(self.device.sock, self.service , self.uuid, [self.uuid, bluetooth.SERIAL_PORT_CLASS],
                                    [bluetooth.SERIAL_PORT_PROFILE])
        print(f"Service {self.service} Ok")

    def listen(self):
        self.mainClient.status = 0
        print("Waiting for connection...")
        clientSock, clientInfo = self.device.sock.accept()
        self.mainClient.mac = clientInfo
        self.mainClient.status = 1
        print(f"Accepted connection from {self.mainClient}")
        json = self.makeJson()
        self.device.sock.send(json)
        print(f"Sending {json}")
        self.mainClient.status = 2
        self.emit()

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
        return f"BTServer {self.mainClient}<-{self.device}<-{self.clients}"


if __name__ == '__main__':
    server = BTServer((
        BTDevice("C8:14:51:08:8F:3A", 4),
        BTDevice("C8:14:51:08:8F:00", 1),
        BTDevice("C8:14:51:08:8F:00", 2),
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




