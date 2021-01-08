#!/usr/bin/python
# coding: utf8

#https://www.programcreek.com/python/example/53878/psutil.disk_usage

import psutil
import platform
import datetime

def tell_system_status():

        os, name, version, _, _, _ = platform.uname()
        version = version.split('-')[0]
        cores = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory()[2]
        disk_percent = psutil.disk_usage('/')[3]
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        running_since = boot_time.strftime("%A %d. %B %Y")
        response = "I am currently running on %s version %s.  " % (os, version)
        response += "This system is named %s and has %s CPU cores.  " % (name, cores)
        response += "Current disk_percent is %s percent.  " % disk_percent
        response += "Current CPU utilization is %s percent.  " % cpu_percent
        response += "Current memory utilization is %s percent. " % memory_percent
        response += "it's running since %s." % running_since
        return response

def disksinfo():
	values = []
	disk_partitions = psutil.disk_partitions(all=False)
	for partition in disk_partitions:
		usage = psutil.disk_usage(partition.mountpoint)
		device = {'device': partition.device,
				  'mountpoint': partition.mountpoint,
				  'fstype': partition.fstype,
				  'opts': partition.opts,
				  'total': usage.total,
				  'used': usage.used,
				  'free': usage.free,
				  'percent': usage.percent
				  }
		values.append(device)
	values = sorted(values, key=lambda device: device['device'])
	return values

def sysInfoRaw():
    import time
    import psutil

    cpuPercent = psutil.cpu_percent(interval=1)
    memPercent = psutil.virtual_memory().percent
    sda2Percent = psutil.disk_usage('/').percent
    sda3Percent = psutil.disk_usage('/home').percent

    seconds = int(time.time()) - int(psutil.boot_time())
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    uptime =  [d, h, m, s]

    return [cpuPercent, memPercent, sda2Percent, sda3Percent, uptime] 
	
def get_disk_info():
	data = []
	try:
		disks = psutil.disk_partitions(all=True)
		for disk in disks:
			if not disk.device:
				continue
			if disk.opts.upper() in ('CDROM', 'REMOVABLE'):
				continue
			item = {}
			item['name'] = disk.device
			item['device'] = disk.device
			item['mountpoint'] = disk.mountpoint
			item['fstype'] = disk.fstype
			item['size'] = psutil.disk_usage(disk.mountpoint).total >> 10
			data.append(item)
		data.sort(key=lambda x: x['device'])
	except:
		data = []
		self.logger.error(traceback.format_exc())

	return data
	
	
returnValue = tell_system_status()
print (returnValue)

returnValue = disksinfo()
print ("")
print (returnValue)

returnValue = sysInfoRaw()
print ("")
print (returnValue)

returnValue = get_disk_info()
print ("")
print (returnValue)

