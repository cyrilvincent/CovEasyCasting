import threading
import abc
import uuid
import json
import datetime
import config
import logging

from typing import List, Tuple

class Device:

    def __init__(self, id="00:00:00:00:00:00", port=0):
        self.id = id
        self.port = port

    def __repr__(self):
        return str(self.id)+"["+str(self.port)+"]"

class AbstractClient(threading.Thread, metaclass=abc.ABCMeta):

    def __init__(self, prefix:str, device:Device, cb = lambda device, data : 0, timeout:int = config.timeOutData):
        super().__init__()
        self.prefix = prefix
        self.device = device
        self.sock = None
        self._data = 0.0
        self.datetime = datetime.datetime.now()
        self.cb = cb
        self.status = -2 # -2 = Not connected, -3 = Disconnected, -4 = Down, -1 = Connected, 0 = Dialog
        self.timeout = timeout
        self.server = None
        self.stop = False

    @property
    def data(self):
        if self._data > 0:
            dt = datetime.datetime.now()
            s = (dt - self.datetime).total_seconds()
            if s > self.timeout:
                logging.debug("Timeout:"+str(self))
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

    def __repr__(self):
        return str(self.device)

    def __del__(self):
        try:
            self.sock.close()
        except:
            pass

class AbstractServer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def emit(self):...

    def makeJson(self):
        d = {}
        # d["phone"] = self._getData(self.clients[0])
        # d["temp"] = self._getData(self.clients[1])
        # d["pres"] = self._getData(self.clients[2])
        # d["weight"] = self._getData(self.clients[3])
        # d["mix"] = self._getData(self.clients[4])
        d["pho"] = int(self._getData(self.getByPrefix("pho")))
        d["tem"] = self._getData(self.getByPrefix("tem"))
        pre = self._getData(self.getByPrefix("pre"))
        d["pre"] = pre/100 if pre > 0 else pre
        d["wei"] = int(self._getData(self.getByPrefix("wei")))
        # d["mix"] = self.convertIntToBinary(self._getData(self.getByPrefix("mix")))
        d["mix"] = int(self._getData(self.getByPrefix("mix")))
        return json.dumps(d)

    def _getData(self,device):
        if device.status < 0:
            return device.status
        else:
            return device.data

    def getByPrefix(self, prefix):
        res = [c for c in self.clients if c.prefix == prefix]
        if len(res) == 0:
            logging.error(f"Prefix {prefix} not found")
            return self.clients[["pho","tem","wei","pre","mix"].index(prefix)]
        else:
            return res[0]

    def convertIntToBinary(self, nb:int)->int:
        res = -1
        if nb >= 0 and nb < 32:
            try:
                res = int(bin(int(nb) + 32)[2:])
            except TypeError:
                pass
        return res

    @abc.abstractmethod
    def connectClients(self):...

    @abc.abstractmethod
    def dialogClients(self):...

    def getMac(self):
        mac = uuid.getnode()
        mac = ':'.join(("%012X" % mac)[i:i + 2] for i in range(0, 12, 2))
        return mac

    @abc.abstractmethod
    def createServer(self, nbClient):...

    @abc.abstractmethod
    def listen(self):...
