#!/usr/bin/python
# coding: utf8

import pyudev

from pyudev import Context, Monitor

try:
    def device_event(observer, device):
        print 'event {0} on device {1}'.format(device.action, device)
except:
    print ("error")
	
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='')
monitor.start()