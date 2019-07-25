from wifipibox import *
from typing import Tuple
import flask
import flask_socketio as io
import config

class RestServer(WifiServer):

    def __init__(self, clients:Tuple[AbstractClient], app, port):
        super().__init__(clients,"localhost","/")
        self.device.id = self.getIp()
        self.device.port = port
        self.app = app

    def emit(self):
        print("Emiting")
        self.status = 0
        while self.status == 0:
            try:
                json = self.makeJson()
                io.emit("response",json,broadcast=True)
                self.status = 0
            except IOError as ex:
                self.status = -4
            time.sleep(1)

    def createServer(self):
        print(f"Starting server {self.device}")
        app.run("0.0.0.0",self.device.port,debug=False)
        self.status = -1

    def stop(self):
        self.status = -2

    def __repr__(self):
        return "RestServer Wifi<-"+str(self.device)+"<-"+str(self.clients)

app = flask.Flask(__name__)
socketio = io.SocketIO(app, async_mode=None)

server = RestServer((
        BTClient(0, Device(config.phoneMac, name=config.phoneBTName)),
        BTClient(1, Device("C8:14:51:08:8F:00", 1)),
        BTClient(2, Device(config.preasureMac, name=config.preasureBTName)),
        SerialClient(3, Device(config.weightSerial)),
        BTClient(4, Device("C8:14:51:08:8F:00", 5)),
    ), socketio, 80)
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

@app.route("/test")
def test():
    return flask.render_template('websocket.html')

@socketio.on('heartbeat', namespace='/pibox')
def hearbeat():
    for i in range(10):
        io.emit('response',"ok")
        time.sleep(1)

@socketio.on("start", namespace="/pibox")
def start():
    server.emit()

@socketio.on('disconnect', namespace='/pibox')
def disconnect():
    server.stop()

if __name__ == '__main__':
    print("Create Rest & WebSocket Server")
    server.createServer()





