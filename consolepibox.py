#!/usr/bin/python3
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
        while not self.stop:
            json = self.makeJson()
            print(json)
            time.sleep(config.sleep)

    def createServer(self):
        pass

    def listen(self):
        self.status = 0
        self.emit()

    def run(self) -> None:
        print("Dialog to devices")
        server.dialogClients()
        print(server)
        print("Listening")
        server.listen()

    def end(self):
        print("Stopping")
        for c in self.clients:
            c.stop = True
        time.sleep(1)
        self.stop = True
        time.sleep(10)

    def __repr__(self):
        return "ConsoleServer "+str(self.clients[0].device)+"<-Console<-"+str(self.clients[1:])


if __name__ == '__main__':
    print("Console Server PiBox")
    print("====================")
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    server = ConsoleServer(eval(config.hardwareConfig))
    server.clients[0].cb = server.phoneEvent
    if type(server.clients[-1]) is FileMixClient:
        server.clients[0].cb = server.clients[-1].phoneEvent
    print(server)
    server.start()
    print("Press Enter to stop")
    input()
    server.end()
    print("Stopped")
    time.sleep(2)
    import os
    os._exit(0)





