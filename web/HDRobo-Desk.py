#!/usr/bin/python
# coding: utf8

"""
HDRobo-Desk.py

date: 26.01.2020
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
from Common import hdRoboCfg

# web Index and API
from WEB_IndexAndAPIHandler import IndexHandler, IndexFirstHandler, ApiHandler
# web Socket
from WEB_SocketHandler import SocketHandler, SocketHandlerWrapper

# signal SocketHandlerWrapper
from RobotWorker import RobotWorker

# load the robo components
from API_HDRack import MotorHandler, HDRackWorker
            
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
    webPort = hdRoboCfg["WebServer"]["Port"]
    print ("start app on Port", webPort)
    app.listen(int(webPort))
    #auto reload after file change
    #TODO remove in prod
    #tornado.autoreload.start()
    #for dir, _, files in os.walk('static'):
    #     print (dir)
    #     [tornado.autoreload.watch(dir + '/' + f) for f in files if not f.startswith('.')]
    #
    ioloop.IOLoop.instance().start()
    