import serial
import time

from genericpibox import *

class SerialClient(AbstractClient):

    def __init__(self, id:int, device:Device, cb = lambda device, data : 0):
        super().__init__(id,device,cb)

    def connect(self):
        print(f"Connecting to {self.device}")
        try:
            self.sock = serial.Serial(self.device.id)
            print(f"Connected to {self.device}")
            self.status = -1
        except IOError:
            self.status = -4
            print(f"{self.device} is Down")

    def run(self) -> None:
        while(True):
            if self.status < -1:
                self.connect()
            while(self.status >= -1):
                try:
                    data = self.sock.readline()
                    self.status = 0
                    print(str(self.device)+"->"+str(data))
                    self.data = float(data)
                    self.cb(self.device, self.data)
                except ValueError:
                    pass
                except IOError:
                    self.status = -3
            try:
                self.sock.close()
                self.status = min(-2, self.status)
            except:
                pass
            time.sleep(60)

    def close(self):
        try:
            self.sock.close()
            self.status = min(self.status, 0)
        except:
            pass

    def __repr__(self):
        return "SerialClient"+str(self.id)+"("+str(self.status)+")"+str(self.device)

if __name__ == '__main__':
    c = SerialClient(0, Device("COM2"))
    c.connect()
    c.run()
    c.close()




