#!/usr/bin/python
# coding: utf8

"""
WEB_SocketHandler.py

date: 19.01.2020
author: oliver Klepach, Martin Weichselbaumer
"""

from tornado import websocket, web, ioloop
import signal

cl = []

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
        
        #robotWork.ConnectedInfo()
        
    def on_close(self):
        print ("open closed")
        if self in cl:
            cl.remove(self)
        #if gpioExists:
        #    ElevatorMotor1.setSendMessage(None)
        #    ConnectorMotor1.setSendMessage(None)

    @staticmethod
    def SendMessage(command, data):
        print "SendMessage", command, data
        retJson = { "command": command, "data": data }
        for webSocket in cl:
            webSocket.write_message(retJson)

#def signalHandler(signum, frame):
#    SocketHandler.SendMessage("signalhandler", {})
#    print ("send signal")
#    signal.setitimer(signal.ITIMER_REAL, 5)

#signal.signal(signal.SIGALRM, signalHandler)
##signal.setitimer(signal.ITIMER_REAL, 5)

