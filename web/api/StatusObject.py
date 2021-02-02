#!/usr/bin/python
# coding: utf8

"""
StatusObject.py
stores the currect Status of the DiskDevice

date: 01.03.2020
author: oliver Klepach, Martin Weichselbaumer
"""

#
# StatusObjectBase
# provide the base communication from submodules
#
class StatusObjectBase():
    # the web Socket Object
    webSocketHandler = None
    # default module name
    StatusModulName = "StatusObject"

    # WriteStatus
    def WriteStatus(self, messageFrom, messageType, message, sendToSocket ):
        if (messageType == "Info"):
            print colors.fg.cyan + messageType + ":" + colors.reset, "'" + messageFrom + "'", message
        elif (messageType == "Error"):
            print colors.fg.red + messageType + ":" + colors.reset, "'" + messageFrom + "'", message
        else:
            print messageType + ":", messageFrom, message

        #if sendToSocket:
        #    self.WriteJsonToSocket(messageFrom, messageType, { "Message": message }, False)

	# WriteStatus - Info
    def StatusInfo(self, message):
        self.WriteStatus(self.StatusModulName, "Info", message, True)
	# WriteStatus - Info
    def StatusInfoFrom(self, messageFrom, message):
        self.WriteStatus(messageFrom, "Info", message, True)

	# WriteStatus - Error
    def StatusError(self, message):
        self.WriteStatus(self.StatusModulName, "Error", message, True)
	# WriteStatus - Error
    def StatusErrorFrom(self, messageFrom, message):
        self.WriteStatus(messageFrom, "Error", message, True)

	# WriteJson
    def WriteJson(self, action, json):
        self.WriteJsonToSocket(self.StatusModulName, action, json, True)
	# WriteJson
    def WriteJsonFrom(self, messageFrom, action, json):
        self.WriteJsonToSocket(messageFrom, action, json, True)

    def WriteJsonToSocket(self, messageFrom, action, json, printOut):
        retJson = []
        retJson.append( { "Action": action,
            "Object": messageFrom
        } )
        retJson.append(json)
        if printOut:
            self.WriteStatus(messageFrom, "Info", "Send Json {0}".format(retJson), False)

        if self.webSocketHandler is not None:
            self.webSocketHandler.SendMessage(messageFrom, retJson)

    # send the result as jsonRpc response
    def ResponseJsonRPC(self, jsonrpcId, resultValue, jsonrpcMethod = None):
        jsonrpcReturn = {
            "jsonrpc": "2.0"          
        }
        # send id if exists, otherwise -1
        if jsonrpcId == None:
            jsonrpcReturn["id"] = -1
        else:
            jsonrpcReturn["id"] = jsonrpcId

        # send method only the exists
        if jsonrpcMethod != None:
            jsonrpcReturn["method"] = jsonrpcMethod

        jsonrpcReturn["result"] = resultValue

        self.StatusInfo(jsonrpcReturn)

        if self.webSocketHandler is not None:
            print "self.webSocketHandler"
            self.webSocketHandler.SendMessage("jsonrpc", jsonrpcReturn)

        return


    # don't remove for the moment
    def WriteJsonToSocketA(self, messageFrom, action, json, printOut):
        print "WriteJsonToSocketA"


	# init
    def __init__(self, socketHandler):
        if socketHandler != None:
            self.webSocketHandler = socketHandler

        self.StatusInfo("StatusObject", "Init")

#
# StatusObject
# simple implementation
#
class StatusObject(StatusObjectBase):
    # init
    def __init__(self, socketHandler):
        # default module name
        self.StatusModulName = "StatusObject"
        self.StatusInfo("Init Object")

#
# colors for output
#
class colors:
    '''Colors class:
    reset all colors with colors.reset
    two subclasses fg for foreground and bg for background.
    use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.green
    also, the generic bold, disable, underline, reverse, strikethrough,
    and invisible work with the main class
    i.e. colors.bold
    '''
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'