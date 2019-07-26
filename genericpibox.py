import threading
import abc
import uuid
import json
import datetime
import config

from typing import List, Tuple


class Device:

    def __init__(self, id="00:00:00:00:00:00", port=0):
        self.id = id
        self.port = port

    def __repr__(self):
        return str(self.id)+"["+str(self.port)+"]"

class AbstractClient(threading.Thread, metaclass=abc.ABCMeta):

    def __init__(self, id:int, device:Device, cb = lambda device, data : 0, timeout:int = config.timeOutData):
        super().__init__()
        self.id = id
        self.device = device
        self.sock = None
        self._data = 0.0
        self.datetime = datetime.datetime.now()
        self.cb = cb
        self.status = -2 # -2 = Not connected, -3 = Disconnected, -4 = Down, -1 = Connected, 0 = Dialog
        self.timeout = timeout
        self.isStop = False

    @property
    def data(self):
        if self._data > 0:
            dt = datetime.datetime.now()
            s = (dt - self.datetime).total_seconds()
            if s > self.timeout:
                print("Timeout:"+str(self))
                self._data = 0
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.datetime = datetime.datetime.now()

    @abc.abstractmethod
    def connect(self):...

    @abc.abstractmethod
    def run(self) -> None:...

    def stop(self):
        self.stop = True
        self.status = -1

    def close(self):
        try:
            self.sock.close()
            self.status = min(self.status, 0)
        except:
            pass

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
        d = {}
        d["phone"] = self._getData(self.clients[0])
        d["temp"] = self._getData(self.clients[1])
        d["preasure"] = self._getData(self.clients[2])
        d["weight"] = self._getData(self.clients[3])
        d["mix"] = self._getData(self.clients[4])
        return json.dumps(d)

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

