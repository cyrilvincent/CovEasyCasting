from btpibox import *
from filepibox import *
from typing import Tuple
import config

class ConsoleServer(BTServer):

    def __init__(self, devices:Tuple[Device]):
        super().__init__(devices)

    def emit(self):
        print("Emiting")
        while True:
            json = self.makeJson()
            print(json)
            self.status = 2
            time.sleep(1)

    def createServer(self):
        pass

    def listen(self):
        self.status = 0
        self.emit()

    def __repr__(self):
        return "ConsoleServer "+str(self.clients[0])+"<-Console<-"+str(self.clients[1:])


if __name__ == '__main__':
    server = ConsoleServer((
        BTClient(0, Device(config.phoneId, config.phonePort)),
        FileClient(1, Device(config.tempId, config.tempPort)),
        BTClient(2, Device(config.preasureId, config.preasurePort)),
        SerialClient(3, Device(config.weightId)),
        SerialClient(4, Device(config.mixId), timeout=3600),
    ))
    server.clients[0].cb = server.phoneEvent
    print(server)
    print("Dialog to devices")
    server.dialogClients()
    print(server)
    print("Listening")
    server.listen()
    print("Stop")




