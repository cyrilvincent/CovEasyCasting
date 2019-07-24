import unittest
import time
from btpibox import *

class PiBoxTest(unittest.TestCase):

    def testBTClient(self):
        c = BTClient(0, Device("C8:14:51:08:8F:3A", 4))
        c.connect()
        self.assertEqual(1, c.status)
        c.start()
        time.sleep(2)
        self.assertEqual(2, c.status)
        c.close()

    def testBTServerClients(self):
        server = BTServer((
            Device("C8:14:51:08:8F:3A", 4),
            Device("C8:14:51:08:8F:00", 1),
            Device("C8:14:51:08:8F:00", 2),
        ))
        server.connectClients()
        self.assertEqual(1, server.clients[0].status)
        self.assertEqual(1, server.clients[1].status)
        self.assertEqual(1, server.clients[2].status)
        server.dialogClients()
        time.sleep(2)
        self.assertEqual(2, server.clients[0].status)
        self.assertEqual(2, server.clients[1].status)
        self.assertEqual(2, server.clients[2].status)

    def testBTServerServer(self):
        server = BTServer(())
        server.createServer()

if __name__ == '__main__':
    unittest.main()




