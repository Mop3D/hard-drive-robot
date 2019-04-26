#!/usr/bin/python
# coding: utf8

import pyudev
import inspect

context = pyudev.Context()
	
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
	
for device in context.list_devices(subsystem='block', DEVTYPE='partition'):
    print(device.get('ID_FS_LABEL', 'unlabeled partition'))
#for device in context.list_devices(subsystem='block', DEVTYPE='disk'):
#	deviceOut(device)
