from wifipibox import *
from typing import Tuple

class RestServer(WifiServer):

    def __init__(self, devices:Tuple[Device], app, port):
        super().__init__(devices,"localhost","/")
        self.device.id = self.getIp()
        self.device.port = port
        self.app = app

    def emit(self):
        pass

    def createServer(self):
        print(f"Starting server {self.device}")
        app.run("0.0.0.0",self.device.port)

    def __repr__(self):
        return "RestServer Wifi<-"+str(self.device)+"<-"+str(self.clients)

import flask
app = flask.Flask(__name__)
server = RestServer((
    Device("C8:14:51:08:8F:3A", 4),
    Device("C8:14:51:08:8F:00", 1),
    Device("C8:14:51:08:8F:00", 2),
), app, 80)
print(server)
print("Connecting to devices")
server.connectClients()
print(server)
print("Dialog to devices")
server.dialogClients()
print(server)

@app.route("/")
def rest():
    json = server.makeJson()
    print("Sending " + json)
    res = flask.Response(response=json,status=200,mimetype="application/json")
    return res

if __name__ == '__main__':
    print("Create Rest server")
    server.createServer()





