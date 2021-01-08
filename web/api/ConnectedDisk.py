#!/usr/bin/python
# coding: utf8

"""
ConnectedDisk.py

date: 01.03.2020
author: oliver Klepach, Martin Weichselbaumer
"""

class CDisk():
    commHandler = None

    def StatusInfo(self, message):
        self.commHandler.StatusInfo("connecteddisk", message)
    def StatusError(self, message):
        self.commHandler.StatusError("connecteddisk", message)

	# init
    def __init__(self, communicationHandler):
        self.commHandler = communicationHandler
        self.StatusInfo("init")

	def GetDeviceInfo(self, property):
		print ("   -> ConnectedDisk.Disk.DeviceInfo: deviceInfo {0}, {1}".format(property, self.diskDevice))
		if self.diskInfo == None:
			return ""
		if self.diskInfo[property] != None:
			return self.diskInfo[property]	
		return ""


class CDiskA():
	diskParent = None

	diskDevice = None
	diskInfo = None
	
	# init
	def __init__(self, DiskParent):
		self.diskParent = DiskParent
		print "   -> ConnectedDisk.Disk: init"

	def GetDeviceInfo(self, property):
		print ("   -> ConnectedDisk.Disk.DeviceInfo: deviceInfo {0}, {1}".format(property, self.diskDevice))
		if self.diskInfo == None:
			return ""
		if self.diskInfo[property] != None:
			return self.diskInfo[property]	
		return ""

	def SetDevice(self, DiskDevice, DiskInfo):
		print ("   -> ConnectedDisk.Disk.SetDevice: deviceInfo {0}".format(DiskDevice))
		self.diskDevice = DiskDevice
		self.diskInfo = DiskInfo
		self.diskParent.MessageFromObject("connecteddisk", "")

	def ClearDevice(self):
		print "   -> ConnectedDisk.Disk.ClearDevice"
		self.diskDevice = None
		self.diskParent.MessageFromObject("disconnecteddisk", "")

	def Dispose(self):
		print "deviceConnect.Monitor: Dispose"
