import csv
import time
from genericpibox import *
from typing import Tuple

class FileClient(AbstractClient):

    def __init__(self, id:int, device:Device, cb = lambda device, data : 0, timeout:int = config.timeOutData):
        super().__init__(id,device,cb,timeout)
        self.values = None

    def connect(self):
        print(f"Connecting to {self.device}")
        try:
            f = open(self.device.id)
            self.values = list(csv.DictReader(f))
            f.close()
            print(f"Connected to {self.device}")
            self.status = -1
        except IOError:
            self.status = -4
            print(f"{self.device} is Down")

    def run(self) -> None:
        if self.status < -1:
            self.connect()
        self.status = 0
        while(not self.isStop):
            for row in self.values:
                self.data = float(row["value"])
                print(str(self.device)+"->"+str(self.data))
                time.sleep(1)

    def __repr__(self):
        return "FileClient"+str(self.id)+str(self.device)

# class BTServer(AbstractServer, BTClient):
#
#     def __init__(self, clients:Tuple[AbstractClient], port=72, service = "EasyCastingBox"):
#         BTClient.__init__(self, 0, Device(self.getMac(), port))
#         self.clients = clients
#         self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ff"
#         self.service = service
#         self.sock:bluetooth.BluetoothSocket = None
#         SerialClient.closeAllSerials()
#
#     def emit(self):
#         while True:
#             try:
#                 json = self.makeJson()
#                 print(f"Sending {json}")
#                 self.sock.send(json)
#                 self.status = 0
#             except IOError as ex:
#                 self.status = -3
#                 time.sleep(10)
#                 self.connect()
#             time.sleep(1)
#
#     def connectClient(self, num):
#         self.clients[num].connect()
#
#     def connectClients(self):
#         for client in self.clients:
#             client.connect()
#
#     def dialogClient(self, num):
#         self.clients[num].start()
#
#     def dialogClients(self):
#         for client in self.clients:
#             client.start()
#
#     def stopClients(self):
#         for client in self.clients:
#             client.stop()
#
#     def stopClient(self, num):
#         self.clients[num].stop()
#
#     def stopForceClient(self):
#         self.stopClients()
#         for client in self.clients:
#             del client
#
#     def createServer(self, nbClient = 1):
#         print(f"Starting server {self.device}")
#         self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#         self.sock.bind(("", self.device.port))
#         self.sock.listen(nbClient)
#         print(f"Server {self.device} Ok")
#         bluetooth.advertise_service(self.sock, self.service , self.uuid, [self.uuid, bluetooth.SERIAL_PORT_CLASS],
#                                     [bluetooth.SERIAL_PORT_PROFILE])
#         print(f"Service {self.service} Ok")
#
#     def listen(self):
#         self.status = min(-2, self.status)
#         print("Waiting for connection...")
#         clientSock, clientInfo = self.sock.accept()
#         self.id = clientInfo
#         self.status = -1
#         print(f"Accepted connection from {self}")
#         json = self.makeJson()
#         self.sock.send(json)
#         print(f"Sending {json}")
#         self.status = 0
#         self.emit()
#
#     def stop(self):
#         self.stopClients()
#         try:
#             self.device.close()
#             self.sock.close()
#             self.status = -2
#         except:
#             pass
#
#     def phoneEvent(self, device, data):
#         try:
#             data = int(data)
#             sock:serial.Serial = self.clients[-1].sock
#             #sock.close()
#             #sock.open()
#             print(str(data) + "->"+str(self.clients[-1].device))
#             sock.write((str(data)+"\n").encode())
#             self.clients[-1].data = 0
#             #time.sleep(0.5)
#             #sock.close()
#             #sock.open()
#         except IOError:
#             self.clients[-1].status = -4
#             print(f"{self.clients[-1].device} is Down")
#
#     def __repr__(self):
#         return "BTServer "+str(self.clients[0].device)+"<-"+str(self.device)+"<-"+str(self.clients[1:])
#

if __name__ == '__main__':
    c = FileClient(0, Device("data/temperature.csv"))
    c.connect()
    c.run()
    c.close()



