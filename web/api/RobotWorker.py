#!/usr/bin/python
# coding: utf8

"""
RobotWorker.py

date: 07.01.2021
author: oliver Klepach, Martin Weichselbaumer
"""

# web Socket
#from WEB_SocketHandler import SocketHandler, SocketHandlerWrapper

# DeviceConnect
import DeviceConnect
# connected Disk
import ConnectedDisk 

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
    commHandler = None
    
    # StatusInfo, StatusError, WriteJsonToSocket
    def StatusInfo(self, message):
        self.commHandler.StatusInfo("robotworker", message)
    def StatusError(self, message):
        self.commHandler.StatusError("robotworker", message)
    def WriteJsonToSocket(self, action, json):
        self.commHandler.WriteJsonToSocket("robotworker", action, json, True)

    # init
    def __init__(self, communicationHandler):
        self.commHandler = communicationHandler
        self.StatusInfo("init RobotWorker")

        #init Disk
        self.connDisk = ConnectedDisk.CDisk(self.commHandler)

        self.devMon = DeviceConnect.Monitor('block', None, self.devicePath, True, self.commHandler)
        # add connect/disconnect event
        self.devMon.CallOnConnect(self.connected_changed)
        self.devMon.CallOnDisconnect(self.connected_changed)

        #diskConnected = self.devMon.GetConnectedDisk()
        self.devMon.StartMonitoring()
    
    # connect/disconnect callback
    def connected_changed(self, action, diskid):
        print "**************************** event:", action, diskid


    # DiskInfoJson
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

    # ConnectedInfo
    def ConnectedInfo(self):
        retJson = self.DiskInfoJson()
        self.WriteJsonToSocket("connectinfo", retJson)
        
    # ConnectToSlot
    def ConnectToSlot(self, slotNo):
        self.connectedSlotNo = slotNo
        self.StatusInfo("   ConnectToSlot: {0}".format(slotNo))
        retJson = self.DiskInfoJson()
        self.WriteJsonToSocket("connecttoslot", retJson)
        
    # MessageFromObject
    def MessageFromObject(self, command, message):
        if command == "connecteddisk":
            messageJson = self.DiskInfoJson()
        if command == "disconnecteddisk":
            message = self.DiskInfoJson()
        
        self.StatusInfo("   -> MessageFromObject - {0}: {1}".format(command, message))
        self.WriteJsonToSocket(command, messageJson)
