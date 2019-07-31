import serial
import time
import serial.tools.list_ports as ls
import logging

from genericpibox import *

class SerialClient(AbstractClient):

    nb = 0

    def __init__(self, id:int, device:Device, cb = lambda device, data : 0, timeout:int = config.timeOutData):
        super().__init__(id,device,cb,timeout)
        SerialClient.nb += 1
        if SerialClient.nb == 1:
            SerialClient.closeAllSerials()


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
        while True:
            if self.status < -1:
                self.connect()
            while(self.status >= -1):
                try:
                    data = self.sock.readline()
                    self.status = 0
                    logging.debug(str(self.device)+"->"+str(data))
                    self.data = float(data)
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

    @staticmethod
    def closeAllSerials():
        l = [p.device for p in ls.comports()]
        for d in l:
            try:
                logging.info("Closing "+str(d))
                sock = serial.Serial(d)
                sock.close()
            except:
                pass

if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=config.loggingLevel)
    c = SerialClient(0, Device("COM2"))
    c.connect()
    c.run()
    c.close()




