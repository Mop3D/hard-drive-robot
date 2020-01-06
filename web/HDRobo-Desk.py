#!/usr/bin/python
# coding: utf8

"""
HDRobo-Desk.py
"""

# https://www.tornadoweb.org/en/stable/guide/structure.html
from tornado import websocket, web, ioloop
import tornado.autoreload
import json
import os
import signal
import sys
# needed to import modules from the api folder
sys.path.append('./api')

cl = []

# set the web static folder
static_path_dir = 'ClientApp/build/static'
settings = {
    'debug': True,
    'autoreload': True,
    'static_path': './ClientApp/build/static'
}

# DeviceConnect
import DeviceConnect
# connected Disk
import ConnectedDisk

# check if gpio exists
gpioExists = True
try:
    import RPi.GPIO as GPIO
except ImportError:
    gpioExists = False


# load the robo components
from API_HDRack import MotorHandler, HDRackWorker
if gpioExists:
    print ("init motors")
# load GpioMotor
    #import GpioMotor
 
    #Elevator
    #Elevator Slot
    #stepsPerSlot = 400
    #Elevator Motor
    #stepsPerRound = 4096

    #stepsPerKey = 100
    #stepsToConnect = 1830

    #ElevatorMotor1 = GpioMotor.gpioMotor("Elevator", 21, 23, 19)
    ##ElevatorMotor1.setEndstop(18)
    #ElevatorMotor1.powerOff()

    #ConnectorMotor1 = GpioMotor.gpioMotor("Connector", 3, 5, 7)
    ##ConnectorMotor1.setEndstop(26) 
    #ConnectorMotor1.powerOff()
# /load the robo components

#
# the page handlers
#
class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("ClientApp/build/index.html")

class IndexFirstHandler(web.RequestHandler):
    def get(self):
        self.render("first/templates/index.html")
#


#
# must set before the api handlers
# CORS for development 
class BaseHandler(web.RequestHandler):

    def set_default_headers(self):
        self.set_header("access-control-allow-origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, PUT, DELETE, OPTIONS')
        # HEADERS!
        self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type") 

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

#
# the api handler
#
class ApiHandler(BaseHandler):

    @web.asynchronous
    def get(self, *args):
        retJson = { "return": "ping"}
        self.write(retJson)
        self.finish()

        #value = self.get_argument("value")
        #data = {"id": id, "value" : value}
        #data = json.dumps(data)
        #for c in cl:
        #    c.write_message(data)

    @web.asynchronous
    def post(self):
        pass







#
# Socket Handler wrapper class
#        
class SocketHandlerWrapper():
    # init
    def __init__(self, SocketHandler):
        self.webSocketHandler = SocketHandler
    def SendMessage(self, command, data):
        self.webSocketHandler.SendMessage(command, data)
#
# Socket Handler class
#        
class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print ("open socket")
        if self not in cl:
            cl.append(self)
        #if gpioExists:
        #    ElevatorMotor1.setSendMessage(SocketHandler.SendMessage)
        #    ConnectorMotor1.setSendMessage(SocketHandler.SendMessage)
        
        robotWork.ConnectedInfo()
        
    def on_close(self):
        print ("open closed")
        if self in cl:
            cl.remove(self)
        #if gpioExists:
        #    ElevatorMotor1.setSendMessage(None)
        #    ConnectorMotor1.setSendMessage(None)

    @staticmethod
    def SendMessage(command, data):
        print ("SendMessage", command, data)
        retJson = { "command": command, "data": data }
        for webSocket in cl:
            webSocket.write_message(retJson)


#
# Robot worker class
#        
class RobotWorker():
    #connected Slot Number
    connectedSlotNo = -1
    
    # listen to device 
    devicePath = "/dev/sda"
    #connected Disk
    connDisk = None
    # device handler
    devMon = None
    #websocker handler
    webSocketHandler = None
    
    # init
    def __init__(self, SocketHandler):
        self.webSocketHandler = SocketHandler
        self.MessageFromObject("robotworker", "init RobotWorker")

        #init Disk
        self.connDisk = ConnectedDisk.CDisk(self)

        self.devMon = DeviceConnect.Monitor(None, "ata", None, self.devicePath, self.connDisk, self)
        #diskConnected = self.devMon.GetConnectedDisk()
        self.devMon.StartMonitoring()

    def DiskInfoJson(self):
        retJson = {
            "SlotNo": self.connectedSlotNo,
            "Device": { }
        }
        if self.connDisk != None:
            retJson["Device"]["Type"] = self.connDisk.GetDeviceInfo("type")
            retJson["Device"]["Node"] = self.connDisk.GetDeviceInfo("name")
            retJson["Device"]["Serial"] = self.connDisk.GetDeviceInfo("serial")
            retJson["Device"]["Bus"] = self.connDisk.GetDeviceInfo("bus")
        return retJson

    def ConnectedInfo(self):
        retJson = self.DiskInfoJson()
        self.MessageFromObject("connectinfo", retJson)
        
    def ConnectToSlot(self, slotNo):
        self.connectedSlotNo = slotNo
        print ("   ConnectToSlot: {0}".format(slotNo))
        retJson = self.DiskInfoJson()
        self.MessageFromObject("connecttoslot", retJson)
        
    def MessageFromObject(self, command, message):
        if command == "connecteddisk":
            message = self.DiskInfoJson()
        if command == "disconnecteddisk":
            message = self.DiskInfoJson()
        
        print ("   -> MessageFromObject - {0}: {1}".format(command, message))
        if SocketHandler != None:
            self.webSocketHandler.SendMessage(command, message)

            
def signalHandler(signum, frame):
    SocketHandler.SendMessage("signalhandler", {})
    print ("send signal")
    signal.setitimer(signal.ITIMER_REAL, 5)

signal.signal(signal.SIGALRM, signalHandler)
#signal.setitimer(signal.ITIMER_REAL, 5)

# init the HDRack Worker class
hdrackWork = HDRackWorker(SocketHandler)
# init the Robot Worker class
robotWork = RobotWorker(SocketHandler)
# init the socket handler class
socketHandler = SocketHandlerWrapper(SocketHandler)

app = web.Application(
    [
    (r'/', IndexHandler),
    (r'/first', IndexFirstHandler),
    (r'/ws', SocketHandler),
    (r'/api/(.*)', ApiHandler),
    #(r'/motor/([0-9]+)', MotorHandler),
    (r'/motor/(.*)/(.*)', MotorHandler, dict(hdrackWork=hdrackWork)), #/motor/motorName/Command
    #(r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    #(r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
    (r'/static/(.*)', web.StaticFileHandler, {'path': static_path_dir}),
   (r'/firststatic/(.*)', web.StaticFileHandler, {'path': "./first/firststatic"})
    ],
    **settings
)

if __name__ == '__main__':
    print ("start app on 8888")
    app.listen(8888)
    #auto reload after file change
    #TODO remove in prod
    #tornado.autoreload.start()
    #for dir, _, files in os.walk('static'):
    #     print (dir)
    #     [tornado.autoreload.watch(dir + '/' + f) for f in files if not f.startswith('.')]
    #
    ioloop.IOLoop.instance().start()
    