import csv
import time
import logging
from genericpibox import *

class MockClient(AbstractClient):

    def __init__(self, prefix:str, device:Device, cb = lambda device, data : 0, timeout:int = 3600 * 24):
        super().__init__(prefix, device, cb, timeout)
        self.data = float(device.id)

    def connect(self):
        logging.info(f"Connected to {self.device}")
        self.status = -1

    def run(self) -> None:
        if self.status < -1:
            self.connect()
        self.status = 0
        while not self.stop:
            logging.debug(str(self.device)+"->"+str(self.data))
            time.sleep(1)

class FileClient(AbstractClient):

    def __init__(self, prefix:int, device:Device, cb = lambda device, data : 0, timeout:int = config.timeOutData):
        super().__init__(prefix, device, cb, timeout)
        self.values = None

    def connect(self):
        logging.info(f"Connecting to {self.device}")
        try:
            f = open(self.device.id)
            self.values = list(csv.DictReader(f))
            f.close()
            logging.info(f"Connected to {self.device}")
            self.status = -1
        except IOError:
            self.status = -4
            logging.error(f"{self.device} is Down")

    def run(self) -> None:
        if self.status < -1:
            self.connect()
        self.status = 0
        while not self.stop:
            for row in self.values:
                self.data = float(row["value"])
                logging.debug(str(self.device)+"->"+str(self.data))
                time.sleep(1)

class FileMixClient(FileClient):

    def __init__(self, prefix:int, device:Device, cb = lambda device, data : 0, timeout:int = config.timeOutData):
        super().__init__(prefix, device, cb, timeout)
        self.values = None

    def run(self) -> None:
        if self.status < -1:
            self.connect()
        self.status = 0
        while not self.stop:
            logging.debug(str(self.device)+"->"+str(self.data))
            time.sleep(1)

    def phoneEvent(self, device, data):
        try:
            data = int(data)
            logging.debug(str(data) + "->"+str(self.device))
            self.data = 0
            time.sleep(0.5)
            self.data = int([v["out"] for v in self.values if int(v["in"]) == data ][0])
        except:
            pass

if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=config.loggingLevel)
    c = MockClient(0, Device(2500))
    c = FileClient(0, Device("data/temperature.csv"))
    c.connect()
    c.run()
    c.close()



