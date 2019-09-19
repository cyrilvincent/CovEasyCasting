#!/usr/bin/python3
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
from typing import Tuple

class BTClient(SerialClient):

    def __init__(self, id:int, device:Device, cb = lambda device, data : 0, timeout:int = config.timeOutData):
        super().__init__(id,device,cb,timeout)

    def connect(self):
        if self.device.id != config.phoneId:
            logging.info(f"Connecting to {self.device}")
            try:
                if isinstance(self.device.port, str):
                    self.findPort()
                bluetooth.BluetoothSocket.readline = BTClient.readline1024
                self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                self.sock.connect((self.device.id, self.device.port))
                logging.info(f"Connected to {self.device}")
                self.status = -1
            except IOError:
                self.status = -4
                logging.error(str(self.device) + "is Down")
            except TypeError:
                pass
        else:
            self.status = -1

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
                    if self.sock != None:
                        #data = self.sock.recv(1024)
                        data = self.sock.readline()
                        self.status = 0
                        logging.debug(str(self.device)+"->"+str(data).strip())
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

    def readline1024(self):
        s = ""
        while (True):
            data = self.recv(1024).decode()
            s += data
            if '\r\n' in data:
                break;
        return s

    def readline1(self):
        s = ""
        while (data != '\n'):
            data = self.recv(1).decode()
            s += data
        return s

class BTServer(AbstractServer, BTClient):

    def __init__(self, clients:Tuple[AbstractClient], port=0, service = config.serviceName, uuid = config.serviceUUID):
        BTClient.__init__(self, 0, Device(self.getMac(), port))
        self.clients = clients
        self.uuid = uuid
        self.service = service
        self.sock:bluetooth.BluetoothSocket = None

    def emit(self):
        while self.status > -2:
            try:
                json = self.makeJson()
                print(f"Sending {json}")
                self.clients[0].sock.send(str(json+"\n").encode())
                self.status = 0
            except IOError as ex:
                self.status = -3
                print("Client disconnected")
            time.sleep(1)

    def listen(self):
        while True:
            self.clients[0].status = min(-2, self.status)
            print("Waiting for connection...")
            self.clients[0].sock, clientInfo = self.sock.accept()
            self.status = -1
            print(f"Accepted connection from {clientInfo}")
            self.emit()

    def connectClients(self):
        for client in self.clients:
            client.connect()

    def dialogClients(self):
        for client in self.clients:
            client.start()

    def createServer(self):
        logging.info(f"Starting server {self.device}")
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.bind(("", config.btServerPort))
        self.device.port = self.sock.getsockname()[1]
        self.sock.listen(1)
        self.status = -1
        print(f"Server {self.device} started")
        bluetooth.advertise_service(self.sock, self.service , self.uuid, [self.uuid, bluetooth.SERIAL_PORT_CLASS], [bluetooth.SERIAL_PORT_PROFILE])
        logging.info(f"Service {self.service} Ok")

    def phoneEvent(self, device, data):
        try:
            data = int(data)
            sock = self.clients[-1].sock
            sock.send((str(data)+"\n").encode())
            logging.warning(str(data) + "->" + str(self.clients[-1].device))
        #self.clients[-1].data = 0
        except IOError:
            self.clients[-1].status = -4
            logging.warning(f"{self.clients[-1].device} is Down")
        except AttributeError:
            self.clients[-1].status = -4
            logging.warning(f"{self.clients[-1].device} is Unavailable")

    def __repr__(self):
        return "BTServer "+str(self.clients[0].device)+"<-"+str(self.device)+"<-"+str(self.clients[1:])

    def __del__(self):
        try:
            self.sock.close()
            for c in self.clients:
                del c
        except:
            pass

if __name__ == '__main__':
    print("BT Server PiBox")
    print("===============")
    logging.basicConfig(format='%(message)s', level=config.loggingLevel)
    server = BTServer(
        eval(config.hardwareConfig),
        config.btServerPort
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




