#!/usr/bin/python
# coding: utf8

"""
RobotWorker.py

date: 19.01.2020
author: oliver Klepach, Martin Weichselbaumer
"""

# web Socket
from WEB_SocketHandler import SocketHandler, SocketHandlerWrapper

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
