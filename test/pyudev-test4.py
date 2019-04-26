#!/usr/bin/python
# coding: utf8

import pyudev
#https://pyudev.readthedocs.io/en/latest/#documentation
#sudo apt-get install python-psutil
import psutil

import inspect

context = pyudev.Context()

#https://stackoverflow.com/questions/1667257/how-do-i-mount-a-filesystem-using-python
def mount(source, target, fstype, options=''):
  import subprocess 
  command = "mount -t {2} {0} {1} -o {3}".format(source, target, fstype, options)  

  print(command.split(" "))
  output = subprocess.check_output(command.split(" ")) 
  
  return
  
  import ctypes
  import os
  # parameters wrong in the example
  ret = ctypes.CDLL('libc.so.6', use_errno=True).mount(source, target, fs, options, None)
  if ret < 0:
    errno = ctypes.get_errno()
    raise RuntimeError("Error mounting {} ({}) on {} with options '{}': {}".
     format(source, target, fs, options, os.strerror(errno)))

def umount(target):
  import subprocess 
  command = "umount {0}".format(target)  

  print(command.split(" "))
  output = subprocess.check_output(command.split(" ")) 
  
  return

	 
def get_disk_info(device):
    def get_value(device, key):
        value = ""
        if key in device:
            value = device[key] #.replace('_',' ')
        return value
    diskInfo = {
		"name": get_value(device, "DEVNAME"),
		"path": get_value(device, "DEVPATH"),
		"type": get_value(device, "DEVTYPE"),
		"bus": get_value(device, "ID_BUS"),
		"links": get_value(device, "DEVLINKS"),
		"model": get_value(device, "ID_MODEL"),
		"modelId": get_value(device, "ID_MODEL_ID"),
		"partTableType": get_value(device, "ID_PART_TABLE_TYPE"),
		"partTableUUID": get_value(device, "ID_PART_TABLE_UUID"),
		"pathId": get_value(device, "ID_PATH"),
		"pathTag": get_value(device, "ID_PATH_TAG"),
		"revision": get_value(device, "ID_REVISION"),
		"serial": get_value(device, "ID_SERIAL"),
		"serialShort": get_value(device, "ID_SERIAL_SHORT"),
		"pathTag": get_value(device, "ID_PATH_TAG"),
		"vendor": get_value(device, "ID_VENDOR"),
		"vendorId": get_value(device, "ID_VENDOR_ID"),
        "ataRPM": get_value(device, "ID_ATA_ROTATION_RATE_RPM")
	}
    return diskInfo

def get_partitions_from_disk(device):
    partitions = [device for device in context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
    return partitions
	
	
	
def decode_device_info(device):
    ''' Accept a device. Return a dict of attributes of given device.
    Clean up all strings in the process and make pretty.
    '''
    if 'ID_PRODUCT' in device:
        product = device['ID_PRODUCT'].replace('_',' ')
    else:
        product = "not defined"

    if 'ID_VENDOR' in device:
        vendor = device['ID_VENDOR'].replace('_',' ')
    else:
        vendor = "not defined"
		
    if 'ID_MODEL' in device:
        model = device['ID_MODEL'].replace('_',' ')
    else:
        model = "not defined"
		
    if 'ID_SERIAL_SHORT' in device:
        serial = device['ID_SERIAL_SHORT']
    elif 'ID_SERIAL' in device:
        serial = device['ID_SERIAL']
    else:
        serial = "not defined"
    #print ("vendor {0}, model {1}, serial {2}", vendor, model, serial)
    return({'node': device.device_node, 'type':device.device_type, 'vendor':vendor, 'model':model, 'serial':serial, 'product': product})

def getDevicelist(udevContext, devname):
    devices=[]
    #for device in udevContext.list_devices(subsystem='block', DEVTYPE='disk'):
    for device in udevContext.list_devices(subsystem='block', DEVNAME=devname):
        # Filter out cd drives, loop devices.
        if device.get('ID_TYPE', '') == 'cd':
            continue
        if device.get('UDISKS_PRESENTATION_NOPOLICY', '0') == '1':
            continue
        devices.append(device)
    return devices
	
def deviceOut(device):
	if device.device_node == "/dev/sda":
		print('Device: {0} ({1})'.format(device.device_node, device.device_type))
		memberOut(device)
	
def memberOut(object):
	for memberItem in inspect.getmembers(object):
		if not memberItem[0].startswith('_') and not inspect.ismethod(memberItem[1]):
			#print(memberItem)
			if inspect.isclass(memberItem[1]):
				print ("isclass")
			elif memberItem[0]=="properties":
				print("      " + memberItem[0] + ": type is {0}".format(type(memberItem[1])))
				memberOut(memberItem[1])
			else:
				print("      " + memberItem[0] + ": type is {0}".format(type(memberItem[1])))

def deviceOutA(device):
    x = 0
    if device.device_type is None:
        x = x + 1
    elif device.device_type == 'xdisk' or device.device_type == 'xpartition':
        x = x + 1
    elif device.device_type == 'xscsi_host' or device.device_type == 'xwlan':
        x = x + 1
    elif device.device_type == 'xusb_interface' or device.device_type == 'xusb_device':
        x = x + 1
    else:
#print('       sys_path: {0}'.format(device.sys_path))
#print('       sys_name: {0}'.format(device.sys_name))
#print('       sys_number: {0}, {1}'.format(device.sys_number, int(device.sys_number)))
#print('   device_node: {0}'.format(device.device_node))
#print(device.get('ID_FS_LABEL', 'unlabeled partition'))
        print('Device: {0} ({1})'.format(device.device_node, device.device_type))
        print(device.__dict__)
        print('     member -- ')
        for memberItem in inspect.getmembers(device):
            if not memberItem[0].startswith('_') and not inspect.ismethod(memberItem[1]):
                print(memberItem)
                if inspect.isclass(memberItem[1]):
                    print ("isclass")
                else:
                    print("  type is {0}".format(type(memberItem[1])))
	
#for device in context.list_devices(subsystem='block', DEVTYPE='partition'):
    #print(device.get('ID_FS_LABEL', 'unlabeled partition'))
	
#for device in context.list_devices(subsystem='block', DEVTYPE='disk'):
#    decode_device_info(device)
diskPath = "/dev/sda"
devicesConnected=getDevicelist(context, diskPath)
if (devicesConnected):
    #print devicesConnected
    for deviceRef in devicesConnected:
        devInfo=decode_device_info(deviceRef)
        print devInfo

checkDevice = devicesConnected[0]
#checkDevice = devicesConnected[1]
#checkDevice = devicesConnected[3]

for att in checkDevice:
    print ("{0} = {1}", att, checkDevice[att])

diskInfo = get_disk_info(checkDevice)
partitions = get_partitions_from_disk(checkDevice)
checkPartition = partitions[0]
print ("")
print (checkPartition)
for att in checkPartition:
    print ("{0} = {1}", att, checkPartition[att])
print ("")
for p in psutil.disk_partitions():
    if p.device in checkPartition.device_node:
        print("  {}: {}".format(p.device, p.mountpoint))

print (checkPartition.device_node)


#checkPartition.device_node
#mount(checkPartition.device_node, '/mnt/pdisk', 'vfat', 'rw')
umount('/mnt/pdisk')