import unittest
from btpibox import *
from serialpibox import *
import config
import os


class PiBoxTest(unittest.TestCase):

    def testTemperature(self):
        client = BTClient(1, Device(config.tempMac, config.tempMac))
        client.connect()
        self.assertEqual(-1, client.status)
        client.start()
        time.sleep(2)
        self.assertTrue(client.data > 0)
        client.close()

    def testPreasure(self):
        client = BTClient(2, Device(config.preasureMac, name=config.preasureBTName))
        client.connect()
        self.assertEqual(-1, client.status)
        client.start()
        time.sleep(2)
        self.assertTrue(client.data > 0)
        client.close()

    def testWeight(self):
        SerialClient.closeAllSerials()
        client = SerialClient(3, Device(config.weightSerial))
        client.connect()
        self.assertEqual(-1, client.status)
        client.start()
        time.sleep(3)
        self.assertTrue(client.data >= 0)
        client.close()

    def testWeightMock(self):
        SerialClient.closeAllSerials()
        client = SerialClient(3, Device(config.weightSerial))
        client.connect()
        self.assertEqual(-1, client.status)
        client.start()
        time.sleep(0.5)
        os.system("echo 1 > COM2")
        time.sleep(1)
        self.assertTrue(client.data >= 0)
        client.close()

    def testMix(self):
        client = SerialClient(3, Device(config.mixSerial))
        client.connect()
        client.sock.write("0\n".encode())
        client.sock.timeout = 0
        data = client.sock.read()
        self.assertTrue(data >= 0)
        client.close()

    def testPhone(self):
        client = BTClient(0, Device(config.phoneMac, name=config.phoneBTName))
        client.connect()
        client.close()

    def testBTServerClients(self):
        server = BTServer((
            BTClient(0, Device(config.phoneMac, name=config.phoneBTName)),
            BTClient(1, Device(config.tempMac, config.tempPort)),
            BTClient(2, Device(config.preasureMac, name=config.preasureBTName)),
            SerialClient(3, Device(config.weightSerial)),
            SerialClient(4, Device(config.mixSerial), timeout=3600),
        ))
        server.connectClients()
        self.assertEqual(-1, server.clients[0].status)
        self.assertEqual(-1, server.clients[1].status)
        self.assertEqual(-1, server.clients[2].status)
        self.assertEqual(-1, server.clients[3].status)
        self.assertEqual(-1, server.clients[4].status)
        server.dialogClients()
        time.sleep(2)
        self.assertEqual(0, server.clients[1].status)
        self.assertEqual(0, server.clients[2].status)
        self.assertEqual(0, server.clients[3].status)

if __name__ == '__main__':
    unittest.main()




