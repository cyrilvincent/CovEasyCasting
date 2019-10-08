from wifipibox import *
from typing import Tuple
import flask
import flask_socketio as io
import config
import logging

class RestServer(WifiServer):

    def __init__(self, clients:Tuple[AbstractClient], app, port):
        super().__init__(clients,"localhost","/")
        self.device.id = self.getIp()
        self.device.port = port
        self.app = app

    def emit(self):
        logging.info("Emiting")
        self.status = 0
        while True:
            try:
                json = self.makeJson()
                io.emit("response",json,broadcast=True)
                self.status = 0
            except IOError as ex:
                self.status = -4
                time.sleep(10)
            time.sleep(config.sleep)

    def createServer(self):
        logging.info(f"Starting server {self.device}")
        app.run("0.0.0.0",5000,debug=False)
        self.status = -1

    def __repr__(self):
        return "RestServer Wifi<-"+str(self.device)+"<-"+str(self.clients)

app = flask.Flask(__name__)
socketio = io.SocketIO(app, async_mode=None)

server = RestServer(eval(config.hardwareConfig), socketio, 80)

print(server)
print("Dialog to devices")
server.dialogClients()
print(server)

@app.route("/")
def rest():
    json = server.makeJson()
    logging.info("Sending " + json)
    res = flask.Response(response=json,status=200,mimetype="application/json")
    return res

@app.route("/test")
def test():
    return flask.render_template('websocket.html')

@socketio.on('heartbeat', namespace='/pibox')
def hearbeat():
    for i in range(10):
        io.emit('response',"ok")
        time.sleep(config.sleep)

@socketio.on("start", namespace="/pibox")
def start():
    server.emit()

@socketio.on('disconnect', namespace='/pibox')
def disconnect():
    server.stop()
    pass

if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=config.loggingLevel)
    print("Create Rest & WebSocket Server")
    server.createServer()

    



