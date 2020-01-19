#!/usr/bin/python
# coding: utf8
import yaml
from tornado import websocket, web, ioloop


# HDRobo config
hdRoboCfg = None
# load HDRobo config
with open("../HDRobo.conf.yml", 'r') as ymlfile:
    hdRoboCfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
#for section in hdRoboCfg:
#    print(section)

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
