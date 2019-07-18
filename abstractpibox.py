import threading
import abc
import uuid

from typing import List, Tuple

class Device:

    def __init__(self, id="00:00:00:00:00:00", port=0):
        self.id = id
        self.port = port

    def __repr__(self):
        return f"{self.id}[{self.port}]"

class AbstractClient(threading.Thread, metaclass=abc.ABCMeta):

    def __init__(self, id:int, device:Device, cb = lambda device, data : 0):
        super().__init__()
        self.id = id
        self.device = device
        self.sock = None
        self.data = 0.0
        self.cb = cb
        self.status = 0 # 0 = Not connected, 1 = Connected, 2 = Dialog, -1 = Down, -2 = Disconnected

    @abc.abstractmethod
    def connect(self):...

    @abc.abstractmethod
    def run(self) -> None:...

    def stop(self):
        self.status = 1

    @abc.abstractmethod
    def close(self):...

    def __enter__(self):
        self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

class AbstractServer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def emit(self):...

    def makeJson(self):
        json = "{t:" + str(self._getData(self.clients[0])) + ","
        json += "p:" + str(self._getData(self.clients[1])) + ","
        json += "w:" + str(self._getData(self.clients[2])) + "}"
        return json

    def _getData(self,device):
        if device.status < 0:
            return device.status
        else:
            return device.data

    @abc.abstractmethod
    def connectClient(self, num):...

    @abc.abstractmethod
    def connectClients(self):...

    @abc.abstractmethod
    def dialogClient(self, num):...

    @abc.abstractmethod
    def dialogClients(self):...

    @abc.abstractmethod
    def stopClients(self):...

    @abc.abstractmethod
    def stopClient(self, num):...

    @abc.abstractmethod
    def stopForceClient(self):...

    def getMac(self):
        mac = uuid.getnode()
        mac = ':'.join(("%012X" % mac)[i:i + 2] for i in range(0, 12, 2))
        return mac

    @abc.abstractmethod
    def createServer(self, nbClient = 1):...

    @abc.abstractmethod
    def listen(self):...

    @abc.abstractmethod
    def stop(self):...

    def __del__(self):
        self.stop()

    def __enter__(self):
        self.createServer()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

