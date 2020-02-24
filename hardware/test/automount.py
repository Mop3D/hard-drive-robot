#!/usr/bin/python
# coding: utf8

import deviceConnect

import psutil

diskPath = "/dev/sda"
devMon = deviceConnect.Monitor('block', None, diskPath, None);
diskConnected = devMon.GetConnectedDisk()
print(diskConnected)
devMon.StartMonitoring()

if False:
	devCon = deviceConnect.DeviceCon();
	diskPath = "/dev/sda"
	devicesConnected = devCon.GetDevicelist(diskPath)
	print(devicesConnected)
	if devicesConnected:
		deviceConnected = devicesConnected[0]
		deviceInfo = devCon.GetDeviceInfo(deviceConnected)
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

