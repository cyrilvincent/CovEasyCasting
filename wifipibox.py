import http.client
import time

from btpibox import *
from typing import List, Tuple
import socket

class WifiServer(BTServer):

    def __init__(self, devices:Tuple[Device], host, uri):
        super().__init__(devices,80)
        self.device.id = self.getIp()
        self.clients[0].id = host+uri
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
                self.status = 0
            except IOError as ex:
                self.status = -4
            time.sleep(1)

    def createServer(self):
        print(f"Server {self.device} Ok")

    def listen(self):
        self.emit()

    def getIp(self):
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)

    def __repr__(self):
        return "WifiServer "+str(self.clients[0])+"<-"+str(self.device)+"<-"+str(self.clients[1:])


if __name__ == '__main__':
    server = WifiServer((
        Device("C8:14:51:08:8F:3A", 5),
        Device("C8:14:51:08:8F:3A", 5),
        Device("C8:14:51:08:8F:3A", 4),
        Device("C8:14:51:08:8F:00", 2),
        Device("C8:14:51:08:8F:3A", 5),
    ),"http://www.null.com:80","/")
    print(server)
    print("Dialog to devices")
    server.dialogClients()
    print(server)
    print("Listening")
    server.listen()
    print("Stop")




