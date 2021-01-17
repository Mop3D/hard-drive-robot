#!/usr/bin/python
# coding: utf8

"""
ConnectedDisk.py

date: 17.01.2021
author: oliver Klepach, Martin Weichselbaumer
"""

class CDisk():
	devMonConnectedDisk = None

	# init
	#def __init__(self, communicationHandler):
	
	# set the hardware connected disk
	def SetConnectedDisk(self, devMonConnectedDisk):
		self.devMonConnectedDisk = devMonConnectedDisk
	
	# get the hardware connected disk info
	def GetDiskInfo(self):
		print ("   -> ConnectedDisk.GetDiskInfo")
		if self.devMonConnectedDisk == None:
			return {}
		return self.devMonConnectedDisk.GetJson()





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
