import tkinter
import time

import threading
class Client(threading.Thread):

    def __init__(self):
        super().__init__()
        self.data = ""
        self.sock = None

    def run(self) -> None:
        mac = "C8:14:51:08:8F:3A"
        port = 3
        self.data = "Connecting to "+mac+"["+str(port)+"]"
        import bluetooth
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((mac, port))
        self.data = "Connected"
        while True:
            self.data = self.sock.recv(1024)
        self.sock.close()

class Display(threading.Thread):

    def __init__(self, labelVariable, client):
        super().__init__()
        self.labelVariable = labelVariable
        self.client = client

    def run(self) -> None:
        while(True):
            self.labelVariable.set(str(self.client.data))
            print(str(self.client.data))
            time.sleep(1)

class simpleapp_tk(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        self.geometry("500x50")
        self.client = Client()
        self.client.start()
        self.display = Display(self.labelVariable, self.client)
        self.display.start()


    def initialize(self):

        self.grid()
        self.entryVariable = tkinter.StringVar()
        self.entry = tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set("")

        button = tkinter.Button(self,text="Send",
                                command=self.OnButtonClick)
        button.grid(column=1,row=0)

        self.labelVariable = tkinter.StringVar()
        label = tkinter.Label(self,textvariable=self.labelVariable,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=1,columnspan=2,sticky='EW')
        self.labelVariable.set(u"...")

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, tkinter.END)


    def OnButtonClick(self):
        data = self.entryVariable.get()
        self.client.sock.send(str(data+"\n").encode())
        self.entry.selection_range(0, tkinter.END)
        self.entry.focus_set()

    def OnPressEnter(self,event):
        self.OnButtonClick()

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('PiBox Client Test')
    app.mainloop()