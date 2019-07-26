import csv
import time
from genericpibox import *

class FileClient(AbstractClient):

    def __init__(self, id:int, device:Device, cb = lambda device, data : 0, timeout:int = config.timeOutData):
        super().__init__(id,device,cb,timeout)
        self.values = None

    def connect(self):
        print(f"Connecting to {self.device}")
        try:
            f = open(self.device.id)
            self.values = list(csv.DictReader(f))
            f.close()
            print(f"Connected to {self.device}")
            self.status = -1
        except IOError:
            self.status = -4
            print(f"{self.device} is Down")

    def run(self) -> None:
        if self.status < -1:
            self.connect()
        self.status = 0
        while(not self.isStop):
            for row in self.values:
                self.data = float(row["value"])
                print(str(self.device)+"->"+str(self.data))
                time.sleep(1)

    def __repr__(self):
        return "FileClient"+str(self.id)+str(self.device)

class FileMixClient(FileClient):

    def __init__(self, id:int, device:Device, cb = lambda device, data : 0, timeout:int = config.timeOutData):
        super().__init__(id,device,cb,timeout)
        self.values = None

    def run(self) -> None:
        if self.status < -1:
            self.connect()
        self.status = 0
        while(not self.isStop):
            print(str(self.device)+"->"+str(self.data))
            time.sleep(1)

    def phoneEvent(self, device, data):
        try:
            data = int(data)
            print(str(data) + "->"+str(self.device))
            self.data = 0
            time.sleep(0.5)
            self.data = int([v["out"] for v in self.values if int(v["in"]) == data ][0])
        except:
            pass

    def __repr__(self):
        return "FileMixClient"+str(self.id)+str(self.device)



if __name__ == '__main__':
    c = FileClient(0, Device("data/temperature.csv"))
    c.connect()
    c.run()
    c.close()



