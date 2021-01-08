#!/usr/bin/python
# coding: utf8

"""
WEB_IndexAndAPIHandler.py

date: 19.01.2020
author: oliver Klepach, Martin Weichselbaumer
"""

from tornado import websocket, web, ioloop

# common
from Common import BaseHandler

#
# the page handlers
#
class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("../ClientApp/build/index.html")

class IndexFirstHandler(web.RequestHandler):
    def get(self):
        self.render("../first/templates/index.html")
#

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
