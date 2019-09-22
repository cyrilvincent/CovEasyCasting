import serial
import time
import serial.tools.list_ports as ls
import sys

from genericpibox import *

class SerialClient(AbstractClient):

    nb = 0

    def __init__(self, prefix:str, device:Device, cb = lambda device, data : 0, timeout:int = config.timeOutData):
        super().__init__(prefix, device, cb, timeout)
        self.server = None
        SerialClient.nb += 1
        # if SerialClient.nb == 1:
        #     SerialClient.closeAllSerials()



    def connect(self):
        logging.info(f"Connecting to {self.device}")
        try:
            self.sock = serial.Serial(self.device.id)
            logging.info(f"Connected to {self.device}")
            self.status = -1
        except IOError:
            self.status = -4
            logging.warning(f"{self.device} is Down")

    def run(self) -> None:
        while not self.stop:
            if self.status < -1:
                self.connect()
            while self.status >= -1 and not self.stop:
                try:
                    data = self.sock.readline()
                    self.status = 0
                    logging.debug(str(self.device)+"->"+str(data))
                    self.data = float(self.parseData(data.decode()))
                    self.cb(self.device, self.data)
                except TypeError:
                    self.data = 0
                except ValueError:
                    pass
                except IOError:
                    self.status = -3
                except:
                    pass
            try:
                self.sock.close()
                self.status = min(-2, self.status)
            except:
                pass
            time.sleep(10)
        print(f"{self} stopped")
        try:
            self.sock.close()
        except:
            pass

    @staticmethod
    def closeAllSerials():
        l = [p.device for p in ls.comports()]
        for d in l:
            try:
                sock = serial.Serial(d)
                sock.close()
                logging.info(str(d)+" closed")
            except:
                pass

    def parseData(self, data:str):
        if "pho" in data:
            print(data)

        if len(data) > 4 and data[3] == ":":
            prefix = ""
            if data.startswith("pho:"):
                prefix = "pho"
            elif data.startswith("tem:"):
                prefix = "tem"
            elif data.startswith("pre:"):
                prefix = "pre"
            elif data.startswith("wei:"):
                prefix = "wei"
            elif data.startswith("mix:"):
                prefix = "mix"
            if prefix != "":
                data = data[4:]
            if prefix != self.prefix:
                logging.warning(f"Switch prefix {self.prefix}<->{prefix}")
                cb = self.cb
                c = self.server.getByPrefix(prefix)
                c.prefix = self.prefix
                self.prefix = prefix
                self.cb = c.cb
                c.cb = cb
        return data

if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=config.loggingLevel)
    c = SerialClient(0, Device("COM5"))
    c.connect()
    c.run()
    c.close()




