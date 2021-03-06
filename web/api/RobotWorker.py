#!/usr/bin/python
# coding: utf8

"""
RobotWorker.py

date: 02.02.2021
author: oliver Klepach, Martin Weichselbaumer
"""

# web Socket
#from WEB_SocketHandler import SocketHandler, SocketHandlerWrapper

# StatusObject
from StatusObject import StatusObjectBase

# DeviceConnect
import DeviceConnect
# connected Disk
import ConnectedDisk 

#
# Robot worker class
#        
class RobotWorker(StatusObjectBase):
    #connected Slot Number
    connectedSlotNo = -1
    
    # listen to device 
    devicePath = "/dev/sda"
    #connected Disk
    connDisk = None
    # device handler
    devMon = None
    
    # init
    def __init__(self, socketHandler):
        if socketHandler != None:
            self.webSocketHandler = socketHandler
        # set the communication status modul name
        self.StatusModulName = "RobotWorker"
        self.StatusInfo("init RobotWorker")

        #init Disk
        self.connDisk = ConnectedDisk.CDisk()

        self.devMon = DeviceConnect.Monitor('block', None, self.devicePath, True)
        # add connect/disconnect event
        self.devMon.CallOnConnect(self.Connected_changed)
        self.devMon.CallOnDisconnect(self.Connected_changed)
        # Set the current connected disk
        self.connDisk.SetConnectedDisk(self.devMon.connectedDisk)

        #diskConnected = self.devMon.GetConnectedDisk()
        self.devMon.StartMonitoring()
    
    # connect/disconnect callback
    def Connected_changed(self, action, diskid):
        print "**************************** event:", action, diskid
        if action == "connected":
        # Set the current connected disk
            self.connDisk.SetConnectedDisk(self.devMon.connectedDisk)
            self.ResponseJsonRPC(None, self.ConnectedDiskInfo(), "OnConnect")
        else:
        # disconnect
            json = {
                "diskid": diskid
            }
            self.ResponseJsonRPC(None, json, "OnDisconnect")
            self.connDisk.SetConnectedDisk(None)
    
    # send OnConnect
    def Trigger_OnConnect(self):
        if self.connDisk != None:
            json = self.ConnectedDiskInfo()
        else:
            json = {}
        self.ResponseJsonRPC(None, json, "OnConnect")
    # send OnDisconnect
    def Trigger_OnDisconnect(self):
        if self.connDisk != None:
            json = {
                "diskid": self.connDisk.GetDiskId()
            }
        else:
            json = {}
        self.ResponseJsonRPC(None, json, "OnDisconnect")


    # DiskInfoJson
    #def DiskInfoJson(self):
    #    retJson = {
    #        "SlotNo": self.connectedSlotNo,
    #        "Device": { }
    #    }
    #    if self.connDisk != None:
    #        retJson["Device"]["Type"] = self.connDisk.GetDeviceInfo("type")
    #        retJson["Device"]["Node"] = self.connDisk.GetDeviceInfo("name")
    #        retJson["Device"]["Serial"] = self.connDisk.GetDeviceInfo("serial")
    #        retJson["Device"]["Bus"] = self.connDisk.GetDeviceInfo("bus")
    #    return retJson

    # Hardware Connected Disk Info
    def ConnectedDiskInfo(self):
        retJson = self.connDisk.GetDiskInfo()
        self.WriteJson("connectinfo", retJson)
        return retJson 
        
    # ConnectToSlot
    def ConnectToSlot(self, slotNo):
        self.connectedSlotNo = slotNo
        self.StatusInfo("   ConnectToSlot: {0}".format(slotNo))
        retJson = self.DiskInfoJson()
        self.WriteJson("connecttoslot", retJson)
        
    # MessageFromObject
    def MessageFromObject(self, command, message):
        if command == "connecteddisk":
            messageJson = self.DiskInfoJson()
        if command == "disconnecteddisk":
            message = self.DiskInfoJson()
        
        self.StatusInfo("   -> MessageFromObject - {0}: {1}".format(command, message))
        self.WriteJson(command, messageJson)
