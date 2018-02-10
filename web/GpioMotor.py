#!/usr/bin/python
# coding: utf8
from time import sleep
import RPi.GPIO as GPIO

class gpioMotor(object):
	"""Motor - GPIO out"""
	stepPattern= [
	[1,0,0,0],
	[1,1,0,0],
	[0,1,0,0],
	[0,1,1,0],
	[0,0,1,0],
	[0,0,1,1],
	[0,0,0,1],
	[1,0,0,1]]

	name = 'motor'
	currentPosition = 0
	endStop = False
	endstopbutton = 0

	minsleeptime = 0.0006
	speed = 30 # in percent (110% möglich)
	sleeptime= minsleeptime*100/speed

	# info
	def info(self):
		print ('\n--- motor info --- ')
		print (" channels = " + str(self.motorChannel))
		print (" sleeptime = " + str(self.sleeptime))
		print (" currentPosition = " + str(self.currentPosition))
		print (" self = " + self.__class__.__name__)
		info = { "name": self.name, "channels": self.motorChannel, "sleeptime": self.sleeptime, "currentPosition": self.currentPosition }
		return info

	# init. name of the motor, a,b,c,d are the contoling gpio ports
	def __init__(self, name, a, b, c, d):
		self.name = name
		# init step position
		self.currentPosition = 0
		self.motorChannel = [a,b,c,d]
		self.endStop=False
		
		# Bananapi settings
		# define by GPIO Board, not numbers / Bananpi
		GPIO.setmode(GPIO.BOARD)
		# define out pins
		for mChannel in self.motorChannel:
			GPIO.setup(mChannel, GPIO.OUT)

		self.gpioOutput(self.motorChannel, (0, 0, 0, 0))
		#GPIO.output(self.motorChannel,(0,0,0,0))
		# define in Pins for ends stop button
		#GPIO.setup(self.buttonA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		# assign the event
		#GPIO.add_event_detect(self.buttonA, GPIO.RISING, callback = self.calibrateButton_callback)

	def powerOff(self):
		print ("GPIO.powerOff()")
		self.gpioOutput(self.motorChannel, (0, 0, 0, 0))
		#GPIO.output(self.motorChannel,(0,0,0,0))

	def dispose(self):
		print ("GPIO.cleanup()")
		self.gpioOutput(self.motorChannel, (0, 0, 0, 0))
		#GPIO.output(self.motorChannel,(0,0,0,0))

	# set speed in percent
	def setSpeed(self, speed):
		self.sleeptime= self.minsleeptime*100/speed

	# set endstop gpio port
	def setEndstop(self, endstopport):
		self.endstopbutton = endstopport
		GPIO.setup(self.endstopbutton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		# call when Button Released
		#GPIO.add_event_detect(self.endstopbutton, GPIO.FALLING, callback=self.endstopCallback)  
		# call when Button Pressed
		GPIO.add_event_detect(self.endstopbutton, GPIO.RISING, callback=self.endstopCallback)  
		
	# do step
	def doStep(self, count):
		#self.endStop = False

		direction=1
		if count < 0:
			direction= (-1)

		#print ("direction button", direction, GPIO.input(self.endstopbutton))
		if GPIO.input(self.endstopbutton)==1 and direction>0:
			return self.info()
			
		
		for xi in range (abs(count)):
			self.currentPosition += direction
			self.gpioOutput(self.motorChannel, self.stepPattern[self.currentPosition%8])
			if GPIO.input(self.endstopbutton)==1 and direction>0:
				break;
			sleep (self.sleeptime)

		self.powerOff()
		return self.info()
		
	#do while endstop button pressed
	def doCalibrate(self):
		#while GPIO.input(self.endstopbutton)!=1 and self.currentPosition > -10000:
		#	self.doStep(1000)
		self.doStep(10000)
		self.currentPosition=0
		return self.info()

	#emulate gpio.output with arrays
	def gpioOutput(self, channelArray, valueArray):
		for channelCount in range(len(channelArray)):
			GPIO.output(channelArray[channelCount], valueArray[channelCount])

	#callback button pressed
	def endstopCallback(self,port):
		#print("     -----> GPIO.input() - Button pressed - stop loop")
		self.endStop = True
		self.currentPosition = 0
