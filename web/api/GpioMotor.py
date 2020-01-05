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
class gpioResolution(object):
	RESOLUTION = {'1/1': (0, 0, 0),
              '1/2': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}
	def __init__(self, a, b, c):
		self.resolutionPins = [a,b,c]
		# Bananapi settings
		# define by GPIO Board, not numbers / Bananpi
		GPIO.setmode(GPIO.BOARD)
		# define out pins
		for mChannel in self.resolutionPins:
			GPIO.setup(mChannel, GPIO.OUT)
		# set resolution
		for mChannel in self.resolutionPins:
		#	self.gpioOutput(self.resolutionPins, self.RESOLUTION['1/32'])
			self.gpioOutput(self.resolutionPins, self.RESOLUTION['1/1'])
			
	def dispose(self):
		print ("GPIO.cleanup()")
		self.gpioOutput(self.resolutionPins, (0, 0, 0))

	#emulate gpio.output with arrays
	def gpioOutput(self, channelArray, valueArray):
		for channelCount in range(len(channelArray)):
			GPIO.output(channelArray[channelCount], valueArray[channelCount])

class gpioMotor(object):
	"""Motor - GPIO out"""

	name = 'motor'
	currentPosition = 0
	endStop = False
	endstopbutton = 0

	waitDelay = .0208 / 32

	minsleeptime = 0.0006
	speed = 30 # in percent (110% möglich)
	sleeptime= minsleeptime*100/speed

	sendMessage = None
	
	# info
	def info(self):
		print ('\n--- motor info --- ')
		print (" channels = " + str(self.directionPin) + "/" + str(self.stepPin))
		print (" sleeptime = " + str(self.sleeptime))
		print (" currentPosition = " + str(self.currentPosition))
		print (" self = " + self.__class__.__name__)
		info = { "name": self.name, "channels": str(self.directionPin) + "/" + str(self.stepPin), "sleeptime": self.sleeptime, "currentPosition": self.currentPosition }
		if self.sendMessage:
			self.sendMessage("statusinfo", info)
		return info

	# init. name of the motor, directionPin, stepPin are the controling gpio ports
	def __init__(self, name, directionPin, stepPin):
		self.name = name
		# init step position
		self.directionPin = directionPin
		self.stepPin = stepPin
		self.endStop=False
		
		# define out pins
		GPIO.setup(directionPin, GPIO.OUT)
		GPIO.setup(stepPin, GPIO.OUT)

	def powerOff(self):
		print ("GPIO.powerOff()")
		GPIO.output(self.directionPin, GPIO.LOW)
		GPIO.output(self.stepPin, GPIO.LOW)

	def dispose(self):
		print ("GPIO.cleanup()")
		GPIO.output(self.directionPin, GPIO.LOW)
		GPIO.output(self.stepPin, GPIO.LOW)

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

	# set SendMessage method
	def setSendMessage(self, SendMessage):
		self.sendMessage = SendMessage

	# do step
	def doStep(self, count):
		#self.endStop = False

		direction=1
		if count < 0:
			direction= (-1)

		# TODO:
		#if GPIO.input(self.endstopbutton)==1 and direction>0:
		#	return self.info()
			
		if direction>0: # Clockwise Rotation
			GPIO.output(self.directionPin, GPIO.HIGH)
		else: # Counterclockwise Rotation
			GPIO.output(self.directionPin, GPIO.LOW)			
		
		for xi in range (abs(count)):
			self.currentPosition += direction
			GPIO.output(self.stepPin, GPIO.HIGH)
			sleep (self.waitDelay * 10)
			GPIO.output(self.stepPin, GPIO.LOW)
			sleep (self.waitDelay)
			# TODO:
			#if GPIO.input(self.endstopbutton)==1 and direction>0:
			#	break;

		self.powerOff()
		return self.info()
		
	#do while endstop button pressed
	def doCalibrate(self):
		#while GPIO.input(self.endstopbutton)!=1 and self.currentPosition > -10000:
		#	self.doStep(1000)
		self.doStep(1000)
		self.currentPosition=0
		return self.info()

	#do reset
	def doReset(self):
		self.currentPosition=0
		self.powerOff()
		return self.info()

	#emulate gpio.output with arrays
	def gpioOutput(self, channelArray, valueArray):
		for channelCount in range(len(channelArray)):
			GPIO.output(channelArray[channelCount], valueArray[channelCount])

	# set Power off
	def powerOff(self):
		print ("GPIO.powerOff()")
		#self.gpioOutput(self.motorChannel, (0, 0, 0, 0))
		#GPIO.output(self.motorChannel,(0,0,0,0))

	#callback button pressed
	def endstopCallback(self,port):
		#print("     -----> GPIO.input() - Button pressed - stop loop")
		self.endStop = True
		self.currentPosition = 0