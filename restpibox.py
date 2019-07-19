from wifipibox import *
from typing import Tuple
import flask
import flask_socketio as io

class RestServer(WifiServer):

    def __init__(self, devices:Tuple[Device], app, port):
        super().__init__(devices,"localhost","/")
        self.device.id = self.getIp()
        self.device.port = port
        self.app = app

    def emit(self):
        print("Emiting")
        self.mainClient.status = 2
        while self.mainClient.status == 2:
            try:
                json = self.makeJson()
                io.emit("response",json)
            except IOError as ex:
                self.mainClient.status = -2
            time.sleep(2)

    def createServer(self):
        print(f"Starting server {self.device}")
        app.run("0.0.0.0",self.device.port,debug=False)

    def stop(self):
        self.mainClient.status = 0

    def __repr__(self):
        return "RestServer Wifi<-"+str(self.device)+"<-"+str(self.clients)

app = flask.Flask(__name__)
socketio = io.SocketIO(app, async_mode=None)

server = RestServer((
    Device("C8:14:51:08:8F:3A", 5),
    Device("C8:14:51:08:8F:3A", 4),
    Device("C8:14:51:08:8F:00", 2),
), socketio, 80)
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

@app.route("/test")
def test():
    return flask.render_template('websocket.html')

@socketio.on('my_event', namespace='/pibox')
def test_message(message):
    import time
    for i in range(100):
        io.emit('my_response',{'data': i})
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





