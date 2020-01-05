#!/usr/bin/python
# coding: utf8
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
static_path_dir = '/static'
settings = {
    'debug': True,
    'autoreload': True,
    'static_path': './static'
}
#    'static_path': '/home/pi/web/static'

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
from API_HDRack import MotorHandler
if gpioExists:
# load GpioMotor
    import GpioMotor
 
    #Elevator
    #Elevator Slot
    stepsPerSlot = 400
    #Elevator Motor
    stepsPerRound = 4096

    stepsPerKey = 100
    stepsToConnect = 1830

    ####test
    #GpioMotor.gpioResolution(3, 5, 7)
    #GpioMotor.gpioResolution(11, 13, 15)
    GpioMotor.gpioResolution(19, 21, 23)
    ####test

    #GpioMotor.gpioResolution(11, 13, 15)

    ElevatorMotor1 = GpioMotor.gpioMotor("Elevator", 16, 18)
    ElevatorMotor1.setSpeed(50)    
    #ElevatorMotor1.setEndstop(18)

    ConnectorMotor1 = GpioMotor.gpioMotor("Connector", 19, 21)
    ConnectorMotor1.setSpeed(50)    
    #ConnectorMotor1.setEndstop(26) 
    ConnectorMotor1.powerOff()

    #Gear Motor
    #    # motor1 11,16,18,22 Motor alleine
    #    # motor1 11, 13, 15, 16 Endstop 18 Robot
    #    # motor2 19, 21, 23, 24 Endstop 26 Robot
    #    ElevatorMotor1 = GpioMotor.gpioMotor("Elevator", 11, 13, 15, 16)
    #    ElevatorMotor1.setSpeed(50)    
    #    ElevatorMotor1.setEndstop(18)
    #    ConnectorMotor1 = GpioMotor.gpioMotor("Connector", 19, 21, 23, 24)
    #    ConnectorMotor1.setSpeed(50)    
    #    #ConnectorMotor1.setEndstop(26)
    #    ConnectorMotor1.powerOff()
# /load the robo components


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("templates/index.html")

class ApiHandler(web.RequestHandler):

    @web.asynchronous
    def get(self, *args):
        self.finish()
        retJson = { }
        return json.dumps(retJson)

        
        value = self.get_argument("value")
        data = {"id": id, "value" : value}
        data = json.dumps(data)
        for c in cl:
            c.write_message(data)

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
        if gpioExists:
            ElevatorMotor1.setSendMessage(SocketHandler.SendMessage)
            ConnectorMotor1.setSendMessage(SocketHandler.SendMessage)
        
        robotWork.ConnectedInfo()
        
    def on_close(self):
        print ("open closed")
        if self in cl:
            cl.remove(self)
        if gpioExists:
            ElevatorMotor1.setSendMessage(None)
            ConnectorMotor1.setSendMessage(None)

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

        self.devMon = DeviceConnect.Monitor(None, "ata", None, self.devicePath, self.connDisk, self);
        diskConnected = self.devMon.GetConnectedDisk()
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

# init the Robot Worker class
robotWork = RobotWorker(SocketHandler)
# init the socket handler class
socketHandler = SocketHandlerWrapper(SocketHandler)

app = web.Application(
    [
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
    (r'/api', ApiHandler),
    #(r'/motor/([0-9]+)', MotorHandler),
    (r'/motor/(.*)/(.*)', MotorHandler, dict(gpioExists=gpioExists, socketHandler=socketHandler)), #/motor/motorName/Command
    #(r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    #(r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
    (r'/static/(.*)', web.StaticFileHandler, {'path': static_path_dir})
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
