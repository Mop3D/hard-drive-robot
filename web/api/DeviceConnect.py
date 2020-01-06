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

	monitorParent = None
	devCon = None
	connDisk = None
	
	# init
	def __init__(self, subsystem, bussystem, devtype, devname, connDisk, MonitorParent):
		self.monitorParent = MonitorParent
		self.monitorParent.MessageFromObject("devicemon", "init devmon")
		self.connDisk = connDisk;
		print ("deviceConnect.Monitor: init monitoring on {0},{1},{2}...".format(subsystem, devtype, devname))
		self.devCon = DeviceCon()
		self.subsystem = subsystem
		self.bussystem = bussystem
		self.devtype = devtype
		self.devname = devname

	def GetConnectedDisk(self):
		devicesConnected = self.devCon.GetDevicelist(self.devname)
		print "deviceConnect.Monitor: GetConnectedDisk", devicesConnected
		if devicesConnected is not None and len(devicesConnected) > 0 and self.connDisk is not None:
			self.connDisk.SetDevice(devicesConnected[0], self.devCon.GetDeviceInfo(devicesConnected[0]))
		return devicesConnected

	def StartMonitoring(self):
		print "deviceConnect.Monitor: start monitoring {0}, {1}...".format(self.subsystem, self.devtype) 
		monitor = pyudev.Monitor.from_netlink(self.context)
			
		if self.subsystem is not None and self.devtype is not None:
			monitor.filter_by(subsystem=self.subsystem, device_type=self.devtype)
			print "deviceConnect.Monitor: monitoring - subsystem, device_type"
		elif self.subsystem is not None:
			print "deviceConnect.Monitor: monitoring - subsystem"
			monitor.filter_by(subsystem=self.subsystem)
		elif self.devtype is not None:
			print "deviceConnect.Monitor: monitoring - device_type"
			monitor.filter_by('', device_type=self.devtype)
			
		observer = pyudev.MonitorObserver(monitor, self.Log_Event)
		observer.start()

	# Start Monitoring poll
	def StartMonitoringPoll(self):
		print "deviceConnect.Monitor: StartMonitoringPoll"
		#for device in iter(monitor.poll, None):
		#	self.Log_Event(device.action, device)
		
		#	print ("action, device node", device.action, device.device_node)
		#	#continue
		#	if self.devname is not None and not device.device_node.encode("latin-1").startswith(self.devname):
		#		continue
		#	deviceInfo = self.devCon.GetDeviceInfo(device)
		#	print("  action", device.action)
		#	#print("   deviceInfo", deviceInfo)
		#	if device.action == 'add':
		#		time.sleep( 1 )
		#		self.devCon.MountPartitions(device)
		#	if device.action == 'remove':
		#		time.sleep( 1 )
		#		self.devCon.UnmountPartitionFromDevice(device)

	#not in use
	def Log_Event(self, action, device):
		print "deviceConnect.Monitor: event action={0}, device node={1}".format(device.action, device.device_node)
		if device.device_node is None:
			return
		if self.devname is not None and not device.device_node.encode("latin-1").startswith(self.devname):
			return
		# bus = ata
		deviceInfo = self.devCon.GetDeviceInfo(device)

		retJson = { "Action": action,
			"Device": {
				"Type": device.device_type,
				"Node": device.device_node,
				"Number": device.device_number
			}
		}
		self.monitorParent.MessageFromObject("devicemon", retJson)

		if device.action == 'add':
			time.sleep( 1 )
			if self.connDisk is not None:
				self.connDisk.SetDevice(device, self.devCon.GetDeviceInfo(device))
			self.devCon.MountPartitions(device)
		if device.action == 'remove':
			time.sleep( 1 )
			if self.connDisk is not None:
				self.connDisk.ClearDevice()
			self.devCon.UnmountPartitionFromDevice(device)

	def Dispose(self):
		observer.stop()
		print "deviceConnect.Monitor: Dispose"

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
		print "deviceConnect.DeviceCon: GetDevicelist {0},{1}".format(devname, devtype)
		for device in deviceList:
			print "deviceConnect.DeviceCon: deviceList device".format(device)
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
			print "deviceConnect.DeviceCon.ListDeviceAttribute: {0} = {1}".format(att, device[att])

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
			count = count +1

	# mount partition
	def Mount(self, source, mountPoint, fstype, options=''):
		if fstype == None or fstype == "":
			return
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
