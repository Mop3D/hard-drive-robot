#!/usr/bin/python
# coding: utf8

"""
HDRobo-Desk.py

date: 19.01.2020
author: oliver Klepach, Martin Weichselbaumer
"""

# https://www.tornadoweb.org/en/stable/guide/structure.html
from tornado import websocket, web, ioloop
import tornado.autoreload
#import json
#import os

# needed to import modules from the api folder
import sys
sys.path.append('./api')

# set the web static folder
static_path_dir = 'ClientApp/build/static'
settings = {
    'debug': True,
    'autoreload': True,
    'static_path': './ClientApp/build/static'
}

# common
# must set before the api handlers
from Common import BaseHandler

# web Index and API
from WEB_IndexAndAPIHandler import IndexHandler, IndexFirstHandler, ApiHandler
# web Socket
from WEB_SocketHandler import SocketHandler, SocketHandlerWrapper

# signal SocketHandlerWrapper
from RobotWorker import RobotWorker



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
    