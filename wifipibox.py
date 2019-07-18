import http.client
import time

from btpibox import *
from typing import List, Tuple
import socket

class WifiServer(BTServer):

    def __init__(self, devices:Tuple[Device], host, uri):
        super().__init__(devices)
        self.device.id = self.getIp()
        self.mainClient.id = host+uri
        self.host = host
        self.uri = uri

    def emit(self):
        print("Emiting")
        while True:
            try:
                json = self.makeJson()
                print("Sending "+json)
                conn = http.client.HTTPConnection(self.host)
                conn.request("POST",self.uri,json,{'Content-type': 'application/json'})
                conn.close()
                self.mainClient.status = 2
            except IOError as ex:
                self.mainClient.status = -2
            time.sleep(2)

    def createServer(self):
        print(f"Server {self.device} Ok")

    def listen(self):
        self.mainClient.status = 0
        self.emit()

    def getIp(self):
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)

    def __repr__(self):
        return "WifiServer "+self.host+self.uri+"<-"+str(self.device)+"<-"+str(self.clients)


if __name__ == '__main__':
    server = WifiServer((
        Device("C8:14:51:08:8F:3A", 5),
        Device("C8:14:51:08:8F:3A", 4),
        Device("C8:14:51:08:8F:00", 2),
    ),"http://www.null.com:80","/")
    print(server)
    print("Connecting to devices")
    server.connectClients()
    print(server)
    print("Dialog to devices")
    server.dialogClients()
    print(server)
    print("Create Wifi server")
    server.createServer()
    print(server)
    print("Listening")
    server.listen()
    print("Stop")




