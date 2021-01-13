#!/usr/bin/python
# coding: utf8

"""
WEB_IndexAndAPIHandler.py

date: 19.01.2020
author: oliver Klepach, Martin Weichselbaumer
"""

from tornado import websocket, web, ioloop
import json

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

#
# the JsonRpc handler
#
# https://de.wikipedia.org/wiki/JSON-RPC
# https://docs.pylonsproject.org/projects/webob/en/stable/jsonrpc-example.html
#
class JsonRpcHandler(BaseHandler):
    # check if body is json 
    def prepare(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None
    
    #curl -g --data-binary '{ "jsonrpc": "2.0", "method": "Service.Version", "id": 1, "params": null }' --header 'content-type: application/json;' http://hdrobo:8888/jsonrpc
    #curl -g --data-binary '{ "jsonrpc": "2.0", "method": "Service.InvalidCall", "id": 1, "params": { "volume": 0} }' --header 'content-type: application/json;' http://hdrobo:8888/jsonrpc
    
    @web.asynchronous
    def post(self):
        if not self.request.headers.get("Content-Type", "").startswith("application/json"):
            # TODO: Korrektes 500 Error Handling
            # https://developpaper.com/question/whats-the-difference-between-send-error-write-error-and-raise-httperror-in-tornado/
            print "no json Content-Type header:", self.request.headers.get("Content-Type", "")
            self.clear()
            self.set_status(500)
            self.finish("no json content-type header")
            return
        if not self.json_args:
            print "invalid json body"
            self.clear()
            self.set_status(500)
            self.finish("invalid json body")
            return

        json = self.json_args
        try:
            jsonrpcMethod = json['method']
            jsonrpcId = json['id']
            jsonrpcParams = json['params']
        except KeyError, e:
            raise ValueError(
                "JSON body missing parameter: %s" % e)
        if jsonrpcMethod.startswith('_'):
            raise exc.HTTPForbidden(
                "Bad method name %s: must not start with _" % jsonrpcMethod)
        
        #if not isinstance(jsonrpcParams, list):
        #    raise ValueError(
        #        "Bad params %r: must be a list" % jsonrpcParams)
        #try:
        #    jsonrpcMethod = getattr(self.obj, jsonrpcMethod)
        #except AttributeError:
        #    raise ValueError(
        #        "No such method %s" % jsonrpcMethod)
        #try:
        #    result = jsonrpcMethod(*jsonrpcParams)
        #except:
        #    text = traceback.format_exc()
        #    exc_value = sys.exc_info()[1]
        #    error_value = dict(
        #        name='JSONRPCError',
        #        code=100,
        #        message=str(exc_value),
        #        error=text)
        #    return Response(
        #        status=500,
        #        content_type='application/json',
        #        body=dumps(dict(result=None,
        #                        error=error_value,
        #                        id=id)))

        jsonrpcVersion = json['jsonrpc']
        
        print "Version", jsonrpcVersion
        print "Method", jsonrpcMethod
        print "Id", jsonrpcId
        print "Params", jsonrpcParams

        
        if jsonrpcMethod == "Service.Version":
            resultValue = "V0.9.3A"
        else:
            resultValue = "Method %s not implemented" % jsonrpcMethod

        jsonrpcReturn = {
            "jsonrpc": "2.0",          
            "id": jsonrpcId
        }
        jsonrpcReturn["result"] = resultValue 

        #print "JsonRpc post json body", self.json_args

        self.set_header("Content-Type", "application/json")
        self.write(jsonrpcReturn)
        #print "You wrote ", self.get_body_argument("message")
        #self.write("You wrote " + self.get_body_argument("message"))
        self.finish()
