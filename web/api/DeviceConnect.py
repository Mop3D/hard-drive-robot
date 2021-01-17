#!/usr/bin/python
# coding: utf8

"""
DeviceConnect.py

date: 07.01.2021
author: oliver Klepach, Martin Weichselbaumer
"""

import pyudev
#https://pyudev.readthedocs.io/en/latest/#documentation
#sudo apt-get install python-psutil
import psutil

import os 
import time
import subprocess 

import inspect

from events import Events

import socket

# StatusObject
from StatusObject import StatusObjectBase

class ConnectedDisk():
	context = pyudev.Context()
	devCon = None

	deviceConnected = None
	diskInfo = None

	diskid = None
	mountedPartitions = None

	# init
	def __init__(self, devCon, deviceConnected):
		self.devCon = devCon
		self.deviceConnected = deviceConnected
		self.GetConnectedDisk()

	def GetJson(self):
		if self.deviceConnected == None:
			return {}

		diskJson = {
			"diskid": self.diskid,
			"mounted": [ "part1"]
		}
		return diskJson

	def GetConnectedDisk(self):
		#print "GetConnectedDisk..."
		self.diskInfo = self.devCon.MountDiskPartitions(self.deviceConnected)
		self.mountedPartitions = self.diskInfo["partitions"]
		self.diskid = self.diskInfo["serial"]
		#print self.diskInfo

class MonitorDiskEvents(Events):
    __events__ = ('on_connect', 'on_disconnect')

class Monitor(StatusObjectBase):
	context = pyudev.Context()

	monitorOn = False
	devCon = None
	subsystem = None
	devtype = None
	devname = None
	# the current connected disk
	connectedDisk = None
	
	# init
	def __init__(self, subsystem, devtype, devname, monitorDevices):
        # set the communication status modul name
		self.StatusModulName = "DeviceMonitor"
		self.monitorOn = monitorDevices

		self.StatusInfo("init Device Monitor")
		#print ("init monitoring on {0},{1},{2}...".format(subsystem, devtype, devname))
		self.StatusInfo("init monitoring on {0},{1},{2}...".format(subsystem, devtype, devname))
		self.devCon = DeviceCon()
		self.subsystem = subsystem
		self.devtype = devtype
		self.devname = devname

		self.StatusInfo("Check connected device")
		devicesConnected = self.devCon.GetDevicelist(self.devname)
		if len(devicesConnected) == 0:
			self.StatusInfo("No disk connected")
			self.connectedDisk = None
		else:
			self.StatusInfo("Disk connected: " + str(devicesConnected[0]))
			self.connectedDisk = ConnectedDisk(self.devCon, devicesConnected[0])

		self.Events = MonitorDiskEvents()

	def CallOnConnect(self, objToCall):
		self.Events.on_connect += objToCall
	def CallOnDisconnect(self, objToCall):
		self.Events.on_disconnect += objToCall



	# GetConnectedDeviceList
	def GetConnectedDeviceList(self):
		devicesConnected = self.devCon.GetDevicelist(self.devname)
		return devicesConnected

	# Start Monitoring
	def StartMonitoring(self):
		monitor = pyudev.Monitor.from_netlink(self.context)
			
		if self.subsystem is not None and self.devtype is not None:
			monitor.filter_by(subsystem=self.subsystem, device_type=self.devtype)
		elif self.subsystem is not None:
			monitor.filter_by(subsystem=self.subsystem)
		elif self.devtype is not None:
			monitor.filter_by('', device_type=self.devtype)
			
		# call by webserver
		#if self.statusObj.webSocketHandler != None:
		if self.monitorOn:
			self.StatusInfo("start Monitor Observer (Event)")
			observer = pyudev.MonitorObserver(monitor, self.CallByEvent)
			observer.start()
		else:
			self.StatusInfo("start Monitor Listener (direct)")
			for device in iter(monitor.poll, None):
				self.CallByEvent(device.action, device)
			#print ("action, device node", device.action, device.device_node)
			##continue
			#if self.devname is not None and not device.device_node.encode("latin-1").startswith(self.devname):
			#	continue
			#deviceInfo = self.GetDeviceInfo(device)
			#print("  action", device.action)
			##print("   deviceInfo", deviceInfo)
			#if device.action == 'add':
			#	time.sleep( 1 )
			#	self.devCon.MountPartitions(device)
			#if device.action == 'remove':
			#	time.sleep( 1 )
			#	self.devCon.UnmountPartitionFromDevice(device)

	def CallByEvent(self, action, device):
		# only disk, no partition
		if device.device_type != "disk":
			return
		#print " *** event, device node, type", action, device.device_node, device.device_type
		self.StatusInfo(" *** event, device node, type {0},{1},{2}".format(action, device.device_node, device.device_type))
		if self.devname is not None and not device.device_node.encode("latin-1").startswith(self.devname):
			print "CallByEvent - nothing to do", self.devname, device.device_node.encode("latin-1")
			return

		deviceInfo = self.devCon.GetDeviceInfo(device)

		retJson = { "Device": {
				"Type": device.device_type,
				"Node": device.device_node,
				"Number": device.device_number
			}
		}
		#if self.statusObj.webSocketHandler is not None:
		#	self.statusObj.webSocketHandler.SendMessage("devicemon", retJson)
		if self.statusObj != None:
			self.statusObj.WriteJson("devicemon", action, retJson)

		self.StatusInfo("*** action {0},{1}".format(device.action, device))
		if device.action == 'add':
			time.sleep( 1 )
			#self.devCon.MountDiskPartitions(device)
			self.connectedDisk = ConnectedDisk(self.devCon, device)
			# call connect Event
			self.Events.on_connect('connected', self.connectedDisk.diskid)
			#self.StatusJson("connectDisk", { "diskid": self.connectedDisk.diskid, "mounted": [ "part1"] } )
			self.StatusJson("connectDisk", self.connectedDisk.GetJson() )

		if device.action == 'remove':
			time.sleep( 1 )
			self.Events.on_disconnect('disconnected', self.connectedDisk.diskid)
			self.devCon.UnmountDiskPartitions(device)
			self.StatusJson("disconnectDisk", { "diskid": self.connectedDisk.diskid } )
			self.connectedDisk = None

	def Dispose(self):
		observer.stop()
		self.StatusInfo("observer dispose")


class DeviceCon(StatusObjectBase):
	context = pyudev.Context()

	# init
	def __init__(self):
		self.StatusModulName = "DeviceCon"
		self.StatusInfo("init Device Context")

	# get device list
	def GetDevicelist(self, devname = "", devtype=""):
		devices=[]
		if devname != "" and devtype != "":
			deviceList = self.context.list_devices(subsystem='block', DEVNAME=devname, DEVTYPE=devtype)
		elif devname != "":
			deviceList = self.context.list_devices(subsystem='block', DEVNAME=devname)
		elif devtype != "":
			deviceList = self.context.list_devices(subsystem='block', DEVTYPE=devtype)
		else:
			deviceList = self.context.list_devices(subsystem='block')
		
		for device in deviceList:
			# Filter out cd drives, loop devices.
			if device.get('ID_TYPE', '') == 'cd':
				continue
			if device.get('UDISKS_PRESENTATION_NOPOLICY', '0') == '1':
				continue
			devices.append(device)
		return devices

	def GetDeviceInfo(self, device):
		def get_value(device, key):
			value = ""
			if key in device:
				value = device[key] #.replace('_',' ')
			return value
		deviceInfo = {
			"name": get_value(device, "DEVNAME"),
			"path": get_value(device, "DEVPATH"),
			"type": get_value(device, "DEVTYPE"),
			"bus": get_value(device, "ID_BUS"),
			"links": get_value(device, "DEVLINKS"),
			"model": get_value(device, "ID_MODEL"),
			"modelId": get_value(device, "ID_MODEL_ID"),
			"pathId": get_value(device, "ID_PATH"),
			"pathTag": get_value(device, "ID_PATH_TAG"),
			"revision": get_value(device, "ID_REVISION"),
			"serial": get_value(device, "ID_SERIAL"),
			"serialShort": get_value(device, "ID_SERIAL_SHORT"),
			"pathTag": get_value(device, "ID_PATH_TAG"),
			"vendor": get_value(device, "ID_VENDOR"),
			"vendorId": get_value(device, "ID_VENDOR_ID")
		}
		if get_value(device, "DEVTYPE") == "disk":
			deviceInfo["partTableType"] = get_value(device, "ID_PART_TABLE_TYPE")
			deviceInfo["partTableUUID"] = get_value(device, "ID_PART_TABLE_UUID")
			deviceInfo["ataRPM"]= get_value(device, "ID_ATA_ROTATION_RATE_RPM")
			
		if get_value(device, "DEVTYPE") == "partition":
			deviceInfo["fsLabel"] = get_value(device, "ID_FS_LABEL")
			deviceInfo["fsType"] = get_value(device, "ID_FS_TYPE")
			deviceInfo["fsUsage"] = get_value(device, "ID_FS_USAGE")
			deviceInfo["fsUUID"] = get_value(device, "ID_FS_UUID")
			deviceInfo["fsVersion"] = get_value(device, "ID_FS_VERSION")
		
		return deviceInfo

	# mount all partitions, (not used)	
	def MountDiskPartitions(self, diskDevice):
		self.StatusInfo("-----> MountDiskPartitions {0}".format(diskDevice.device_node))
		devInfo = self.GetDeviceInfo(diskDevice)
		devInfo["partitions"] = []
		partitions = self.GetPartitionsFromDisk(diskDevice)
		for partition in partitions:
			# partition info
			partInfo = self.GetDeviceInfo(partition)
			# device name
			deviceName = str(partInfo["name"])
			# part number
			lastDeviceChar = deviceName[-1:]
			# mount point and share name
			mountPoint = "/mnt/partition{0}".format(lastDeviceChar)
			shareName = "Part{0}".format(lastDeviceChar)
			#print "    --> Partition", partInfo["name"], partInfo["fsType"], partInfo["fsLabel"], mountPoint, shareName
			self.StatusInfo("    --> Partition {0},{1},{2},{3},{4}".format(partInfo["name"], partInfo["fsType"], partInfo["fsLabel"], mountPoint, shareName))
			# check and create mount folder
			if not os.path.exists(mountPoint):
				os.makedirs(mountPoint)
			# check mounted partitions
			if not self.CheckMountPartition(partition, mountPoint):
				#print "  {0} on {1} mount...".format(deviceName, mountPoint, partInfo["fsType"])
				self.StatusInfo("  {0} on {1} mount...".format(deviceName, mountPoint, partInfo["fsType"]))
				self.Mount(deviceName, mountPoint, partInfo["fsType"], "rw")
				self.SetSambaShare(shareName, mountPoint)
			else:
				#print "  {0} on {1} allready mounted".format(deviceName, mountPoint)
				self.StatusInfo("  {0} on {1} allready mounted".format(deviceName, mountPoint))
			partData = {
				"partInfo": partInfo,
				"mountPoint": mountPoint,
				"shareName": "//" + socket.gethostname() + "/" + shareName
			}
			devInfo["partitions"].append( partData  )
		return devInfo

	# mount all partitions from device
	def UnmountDiskPartitions(self, diskDevice):
		#print "-----< UnmountDiskPartitions", diskDevice.device_node
		self.StatusInfo("-----< UnmountDiskPartitions {0}".format(diskDevice.device_node))
		devInfo = self.GetDeviceInfo(diskDevice)
		for partition in psutil.disk_partitions():
			# only partition from the devices
			#print "    --< Part", partition.device, diskDevice.device_node, partition.mountpoint

			if partition.device.startswith(diskDevice.device_node):
				# part number
				lastDeviceChar = partition.device[-1:]
				# share name
				shareName = "Part{0}".format(lastDeviceChar)
				#print "    --< Partition", partition.device, partition.mountpoint, shareName
				self.StatusInfo("    --< Partition {0},{1},{2}...".format(partition.device, partition.mountpoint, shareName))
				self.DelSambaShare(shareName)
				self.KillFUser(partition.mountpoint)
				self.Umount(partition.device)


	# list device attibutes
	def ListDeviceAttribute(self, device):
		for att in device:
			#print ("{0} = {1}", att, device[att])
			self.StatusInfo("ListDeviceAttribute {0} = {1}".format(att, device[att]))

	# get Partitions 
	def GetPartitionsFromDisk(self, parentDevice):
		partitions = [device for device in self.context.list_devices(subsystem='block', DEVTYPE='partition', parent=parentDevice)]
		return partitions

	# check is device mounted
	def CheckMountPartition(self, partitionDevice, mountPoint):
		for partitions in psutil.disk_partitions():
			if partitions.device in partitionDevice.device_node:
				return True
				#print("  {}: {}".format(partitions.device, partitions.mountpoint))
		return False

	# mount all partitions, (not used)	
	#def MountPartition(self, parentDevice):
	#	devInfo = self.GetDeviceInfo(parentDevice)
	#	# check type
	#	if devInfo["type"] != "partition":
	#		return
	#	deviceName = str(devInfo["name"])
	#	lastDeviceChar = deviceName[-1:]
	#	mountPoint = "/mnt/partition{0}".format(lastDeviceChar)
	#	shareName = "Part{0}".format(lastDeviceChar)
	#	if not os.path.exists(mountPoint):
	#		os.makedirs(mountPoint)
	#	if not self.CheckMountPartition(parentDevice, mountPoint):
	#		self.Mount(devInfo["name"], mountPoint, devInfo["fsType"], "rw")
	#		self.SetSambaShare(shareName, mountPoint)
	#	else:
	#		 print "  - partition {0} on {1} mounted".format(devInfo["name"], mountPoint)

	# mount all partitions	
	#def MountPartitions(self, parentDevice):
	#	return
	#	partitions = self.GetPartitionsFromDisk(parentDevice)
	#	count = 0
	#	for partition in partitions:
	#		partInfo = self.GetDeviceInfo(partition)
	#		mountPoint = "/mnt/partition{0}".format(count)
	#		if not os.path.exists(mountPoint):
	#			print " - create " + mountPoint
	#			os.makedirs(mountPoint)
	#		if not self.CheckMountPartition(partition, mountPoint):
	#			print "xxx mount"
	#			#self.Mount(partInfo["name"], mountPoint, partInfo["fsType"], "rw")
	#		else:
	#			 print "  - partition {0} on {1} mounted".format(partInfo["name"], mountPoint)
	#		count = count + 1

	# mount partition
	def Mount(self, source, mountPoint, fstype, options=''):
		try:
			command = "mount -t {2} {0} {1} -o {3}".format(source, mountPoint, fstype, options)  
			#print " ... mount", command
			self.StatusInfo(" ... mount {0}".format(command))
			if fstype != None and fstype != "" :
				self.ShCommand(command)
		except Exception as e:
			#print('Failed mount: ' + str(e))
			self.StatusInfo("Failed mount: {0}".format(str(e)))

	# mount partitions from mountPoint
	#def UnmountPartitionMountPoint(self, mountPoint):
	#	for p in psutil.disk_partitions():
	#		if p.mountpoint == mountPoint:
	#			self.Umount(p.device)
	#			#print("  {}: {}".format(p.device, p.mountpoint))	
			
	# mount all partitions from device
	def UnmountPartitionFromDevice(self, device):
		devInfo = self.GetDeviceInfo(device)
		if devInfo["type"] != "partition":
			return
		deviceName = str(devInfo["name"])
		lastDeviceChar = deviceName[-1:]
		mountPoint = "/mnt/partition{0}".format(lastDeviceChar)
		shareName = "Part{0}".format(lastDeviceChar)

		#print "  unmount device ", device.device_node
		self.StatusInfo("  unmount device {0}".format(subsystemdevice.device_node))
		self.DelSambaShare(shareName)
		self.KillFUser(mountPoint)
		self.Umount(device.device_node)

	# mount all partitions from device
	#def UnmountPartitionFromDevice(self, device):
	#	#print "  unmount from Pa ", device.device_node
	#	for p in psutil.disk_partitions():
	#		devInfo = self.GetDeviceInfo(p)
	#		deviceName = str(devInfo["name"])

	#		print("..............", p)
	#		print("...............", devInfo )
	#		print("................", deviceName)

	#		lastDeviceChar = deviceName[-1:]
	#		mountPoint = "/mnt/partition{0}".format(lastDeviceChar)
	#		shareName = "Part{0}".format(lastDeviceChar)
	#		if p.device == device.device_node:
	#			#print ("    found", p.device, device.device_node)
	#			self.DelSambaShare(shareName)
	#			self.KillFUser(mountPoint)
	#			self.Umount(p.device)
	#		else:
	#			pDevice = self.GetDevicelist(p.device)
	#			#print ("p.device, pDevice", p.device, pDevice[0].device_node)
	#			if pDevice and pDevice[0].parent.device_node == device.device_node:
	#				self.DelSambaShare(shareName)
	#				self.KillFUser(mountPoint)
	#				self.Umount(p.device)

	# kill fuser on partition
	def KillFUser(self, mountPoint):
		command = "fuser -km {0}".format(mountPoint)  
		try:
			self.ShCommand(command)
		except Exception as e:
			self.StatusError("Failed kill fUser {0}".format(str(e)))

	# umount partition
	def Umount(self, mountDev):
		command = "umount {0}".format(mountDev)  
		self.ShCommand(command)

	# add smaba share	
	def SetSambaShare(self, shareName, folder):
		try:
			command = "net usershare add {0} {1} '{1}' everyone:F guest_ok=y".format(shareName, folder)  
			self.ShCommand(command)
		except Exception as e:
			self.StatusError("Failed set share {0}".format(str(e)))
	# remove smaba share	
	def DelSambaShare(self, shareName):
		try:
			command = "net usershare delete {0}".format(shareName)  
			self.ShCommand(command)
		except Exception as e:
			self.StatusError("Failed delete share {0}".format(str(e)))

	# call sh command
	def ShCommand(self, command):
		self.StatusInfo("command {0}".format(command))
		return subprocess.check_output(command.split(" ")) 
