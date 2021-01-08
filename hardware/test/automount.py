#!/usr/bin/python
# coding: utf8

import StatusObject

import DeviceConnect

import psutil

statusObj = StatusObject.StatusObject(None)


diskPath = "/dev/sda"
devMon = DeviceConnect.Monitor('block', None, diskPath, False, statusObj)
diskConnected = devMon.GetConnectedDisk()
statusObj.StatusInfo("automount", diskConnected)
devMon.StartMonitoring()

###################################################
# not used
###################################################
if False:
	devCon = DeviceConnect.DeviceCon()
	diskPath = "/dev/sda"
	devicesConnected = devCon.GetDevicelist(diskPath)
	print(devicesConnected)
	if devicesConnected:
		deviceConnected = devicesConnected[0]
		deviceInfo = devCon.GetDeviceInfo(deviceConnected)
		print " "
		print(deviceInfo)
		devCon.ListDeviceAttribute(deviceConnected)
		partitionsFromDisk = devCon.GetPartitionsFromDisk(deviceConnected)
		if partitionsFromDisk:
			print(partitionsFromDisk)
			partitionFromDisk = partitionsFromDisk[0]
			deviceInfo = devCon.GetDeviceInfo(partitionFromDisk)
			#print(deviceInfo)
			devCon.ListDeviceAttribute(partitionFromDisk)
			print "   MountPartitions"
			devCon.MountPartitions(partitionFromDisk)
			#for p in psutil.disk_partitions():
			#    if p.device in partitionFromDisk.device_node:
			#        print("  {}: {}".format(p.device, p.mountpoint))

