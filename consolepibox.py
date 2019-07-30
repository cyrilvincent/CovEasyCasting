from btpibox import *
from mockpibox import *
from typing import Tuple
import config
import logging

class ConsoleServer(BTServer):

    def __init__(self, devices:Tuple[Device]):
        super().__init__(devices)

    def emit(self):
        logging.info("Emiting")
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
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    server = ConsoleServer(eval(config.defaultConfig))
    server.clients[0].cb = server.phoneEvent
    print(server)
    print("Dialog to devices")
    server.dialogClients()
    print(server)
    print("Listening")
    server.listen()
    print("Stop")




