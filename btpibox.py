import threading
import bluetooth
import uuid
import time
import json
import serial
import sys
import logging

from genericpibox import *
from serialpibox import *
from mockpibox import *
from typing import List, Tuple

class BTClient(SerialClient):

    def __init__(self, id:int, device:Device, cb = lambda device, data : 0, timeout:int = config.timeOutData):
        super().__init__(id,device,cb,timeout)

    def connect(self):
        logging.info(f"Connecting to {self.device}")
        try:
            if isinstance(self.device.port, str):
                self.findPort()
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.sock.connect((self.device.id, self.device.port))
            logging.info(f"Connected to {self.device}")
            self.status = -1
        except IOError:
            self.status = -4
            logging.error(str(self.device) + "is Down")
        except TypeError:
            pass

    def findPort(self):
        try:
            services = bluetooth.find_service(address=self.device.id)
            service = [s for s in services if self.device.port in str(s["name"])][0]
            logging.debug("Change port "+self.device.port+" to "+str(service["port"]))
            self.device.port = int(service["port"])
        except:
            logging.warning("Can't find "+self.device.port)
            self.status = -4

    def run(self) -> None:
        while(True):
            if self.status < -1:
                self.connect()
            while(self.status >= -1):
                try:
                    data = self.sock.recv(1024)
                    self.status = 0
                    logging.debug(str(self.device)+"->"+str(data))
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
        return "BTClient"+str(self.id)+str(self.device)

class BTServer(AbstractServer, BTClient):

    def __init__(self, clients:Tuple[AbstractClient], port=0, service = config.serviceName, uuid = config.serviceUUID):
        BTClient.__init__(self, 0, Device(self.getMac(), port))
        self.clients = clients
        self.uuid = uuid
        self.service = service
        self.sock:bluetooth.BluetoothSocket = None
        self.clientSock = None
        SerialClient.closeAllSerials()

    def emit(self):
        while True:
            try:
                json = self.makeJson()
                print(f"Sending {json}")
                self.clientSock.send(str(json+"\n").encode())
                self.status = 0
            except IOError as ex:
                self.status = -3
                print("Client disconnected")
                time.sleep(2)
                break;
            time.sleep(1)

    def listen(self):
        while True:
            self.status = min(-2, self.status)
            print("Waiting for connection...")
            self.clientSock, clientInfo = self.sock.accept()
            self.status = -1
            print(f"Accepted connection from {clientInfo}")
            json = self.makeJson()
            self.clientSock.send(str(json + "\n").encode())
            logging.debug(f"Sending {json}")
            self.status = 0
            self.emit()

    def connectClients(self):
        for client in self.clients:
            client.connect()

    def dialogClients(self):
        for client in self.clients:
            client.start()

    def createServer(self, nbClient = 1):
        logging.info(f"Starting server {self.device}")
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.bind(("", self.device.port))
        self.sock.listen(nbClient)
        logging.info(f"Server {self.device} Ok")
        bluetooth.advertise_service(self.sock, self.service , self.uuid, [self.uuid, bluetooth.SERIAL_PORT_CLASS],
                                    [bluetooth.SERIAL_PORT_PROFILE])
        logging.info(f"Service {self.service} Ok")

    def phoneEvent(self, device, data):
        try:
            data = int(data)
            sock:serial.Serial = self.clients[-1].sock
            #sock.close()
            #sock.open()
            logging.debug(str(data) + "->"+str(self.clients[-1].device))
            sock.write((str(data)+"\n").encode())
            self.clients[-1].data = 0
            #time.sleep(0.5)
            #sock.close()
            #sock.open()
        except IOError:
            self.clients[-1].status = -4
            logging.warning(f"{self.clients[-1].device} is Down")

    def __repr__(self):
        return "BTServer "+str(self.clients[0].device)+"<-"+str(self.device)+"<-"+str(self.clients[1:])

    def __del__(self):
        try:
            self.sock.close()
            self.clientSock.close()
            for c in self.clients:
                del c
        except:
            pass


if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=config.loggingLevel+1)
    server = BTServer(
        eval(config.mockExceptPhoneConfig),
        3
    )
    server.clients[0].cb = server.phoneEvent
    if type(server.clients[-1]) is FileMixClient:
        server.clients[0].cb = server.clients[-1].phoneEvent
    print(server)
    print("Dialog to devices")
    server.dialogClients()
    print(server)
    print("Create BT server")
    server.createServer()
    print(server)
    print("Listening")
    server.listen()




