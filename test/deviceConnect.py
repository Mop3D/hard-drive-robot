#!/usr/bin/python
# coding: utf8

import pyudev
#https://pyudev.readthedocs.io/en/latest/#documentation
#sudo apt-get install python-psutil
import psutil

import os 
import time
import subprocess 

import inspect

class Monitor():
	context = pyudev.Context()

	webSocketHandler = None
	devCon = None
	subsystem = None
	devtype = None
	devname = None
	
	# init
	def __init__(self, subsystem, devtype, devname, SocketHandler):
		if SocketHandler != None:
			self.webSocketHandler = SocketHandler
			self.webSocketHandler.SendMessage("devicemon", "init devmon")
		print ("init monitoring on {0},{1},{2}...".format(subsystem, devtype, devname))
		self.devCon = DeviceCon()
		self.subsystem = subsystem
		self.devtype = devtype
		self.devname = devname
	
	def GetConnectedDisk(self):
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
			
		#observer = pyudev.MonitorObserver(monitor, self.Log_Event)
		#observer.start()

		for device in iter(monitor.poll, None):
			self.Log_Event(device.action, device)
			#print ("action, device node", device.action, device.device_node)
			##continue
			#if self.devname is not None and not device.device_node.encode("latin-1").startswith(self.devname):
			#	continue
			#deviceInfo = self.devCon.GetDeviceInfo(device)
			#print("  action", device.action)
			##print("   deviceInfo", deviceInfo)
			#if device.action == 'add':
			#	time.sleep( 1 )
			#	self.devCon.MountPartitions(device)
			#if device.action == 'remove':
			#	time.sleep( 1 )
			#	self.devCon.UnmountPartitionFromDevice(device)

	def Log_Event(self, action, device):
		print ("action, device node", action, device.device_node)
		if self.devname is not None and not device.device_node.encode("latin-1").startswith(self.devname):
			return
		deviceInfo = self.devCon.GetDeviceInfo(device)

		retJson = { "Action": action,
			"Device": {
				"Type": device.device_type,
				"Node": device.device_node,
				"Number": device.device_number
			}
		}
		if self.webSocketHandler is not None:
			self.webSocketHandler.SendMessage("devicemon", retJson)

		print("  action", device.action, device)
		if device.action == 'add':
			time.sleep( 1 )
			self.devCon.MountPartitions(device)
		if device.action == 'remove':
			time.sleep( 1 )
			self.devCon.UnmountPartitionFromDevice(device)

	def Dispose(self):
		observer.stop()
		print ("observer dispose()")
	

class DeviceCon():
	context = pyudev.Context()

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

	# list device attibutes
	def ListDeviceAttribute(self, device):
		for att in device:
			print ("{0} = {1}", att, device[att])

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
		
	# mount all partitions	
	def MountPartitions(self, parentDevice):
		partitions = self.GetPartitionsFromDisk(parentDevice)
		count = 0
		for partition in partitions:
			partInfo = self.GetDeviceInfo(partition)
			mountPoint = "/mnt/partition{0}".format(count)
			if not os.path.exists(mountPoint):
				 print "create " + mountPoint
				 os.makedirs(mountPoint)
			if not self.CheckMountPartition(partition, mountPoint):
				 self.Mount(partInfo["name"], mountPoint, partInfo["fsType"], "rw")
			else:
				 print "partition {0} on {1} mounted".format(partInfo["name"], mountPoint)

	# mount partition
	def Mount(self, source, mountPoint, fstype, options=''):
		command = "mount -t {2} {0} {1} -o {3}".format(source, mountPoint, fstype, options)  
		self.shCommand(command)

	# mount partitions from mountPoint
	def UnmountPartitionMountPoint(self, mountPoint):
		for p in psutil.disk_partitions():
			if p.mountpoint == mountPoint:
				self.Umount(p.device)
				#print("  {}: {}".format(p.device, p.mountpoint))	
			
	# mount all partitions from device
	def UnmountPartitionFromDevice(self, device):
		#print "  unmount from Pa ", device.device_node
		for p in psutil.disk_partitions():
			if p.device == device.device_node:
				#print ("    found", p.device, device.device_node)
				self.Umount(p.device)
			else:
				pDevice = self.GetDevicelist(p.device)
				#print ("p.device, pDevice", p.device, pDevice[0].device_node)
				if pDevice and pDevice[0].parent.device_node == device.device_node:
					self.Umount(p.device)

	# umount partition
	def Umount(self, mountDev):
		command = "umount {0}".format(mountDev)  
		self.shCommand(command)

	# call sh command
	def shCommand(self, command):
		print "command", command;
		return subprocess.check_output(command.split(" ")) 
