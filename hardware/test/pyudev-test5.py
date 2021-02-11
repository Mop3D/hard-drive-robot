#!/usr/bin/python
# coding: utf8

#import sys
#sys.path.append('../disk')

import DeviceConnect

import psutil

diskPath = "/dev/sda"
devMon = DeviceConnect.Monitor('block', None, diskPath, None)
#diskConnected = devMon.connectedDisk
if devMon.connectedDisk:
	print len(devMon.connectedDisk.mountedPartitions)
	print "diskid", devMon.connectedDisk.diskid
	if len(devMon.connectedDisk.mountedPartitions) != 0:
		print "part1 Sharename", devMon.connectedDisk.mountedPartitions[0]

def something_changed(action, diskid):
    print "**************************** event:", action, diskid

devMon.CallOnConnect(something_changed)
devMon.CallOnDisconnect(something_changed)
#devMon.OnEvents.on_connect += something_changed

devMon.StartMonitoring()

if False:
	devCon = DeviceConnect.DeviceCon()
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
			devCon.MountPartitions(partitionFromDisk)
			#for p in psutil.disk_partitions():
			#    if p.device in partitionFromDisk.device_node:
			#        print("  {}: {}".format(p.device, p.mountpoint))

