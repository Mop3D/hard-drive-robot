#!/usr/bin/python
# coding: utf8
from time import sleep
import RPi.GPIO as GPIO

class gpioMotor(object):
	"""Motor - GPIO out"""
	# half step
	stepPattern= [
	[1,0,0,0],
	[1,1,0,0],
	[0,1,0,0],
	[0,1,1,0],
	[0,0,1,0],
	[0,0,1,1],
	[0,0,0,1],
	[1,0,0,1]]

	# full step
	stepPattern2= [
	[1,1,0,0],
	[0,1,1,0],
	[0,0,1,1],
	[1,0,0,1]]

	currentPosition = 0
	endstop = False
	endstopbutton = 0

	loopStop = False

	minsleeptime = 0.0006
	speed = 100 # in percent (110% möglich)
	sleeptime= minsleeptime*100/speed

	# info
	def info(self):
		print ('\n--- motor info --- ')
		print (" channels = " + str(self.motorChannel))
		print (" sleeptime = " + str(self.sleeptime))
		print (" currentPosition = " + str(self.currentPosition))
		

	# init. a,b,c,d are the contoling gpio ports
	def __init__(self,a,b,c,d):
		# init step position
		self.currentPosition = 0
		self.motorChannel = [a,b,c,d]
		self.endStop=False
		
		# define by GPIO numbers, not board numbers
		GPIO.setmode(GPIO.BCM)
		# define out pins
		GPIO.setup(self.motorChannel, GPIO.OUT)
		GPIO.output(self.motorChannel,(0,0,0,0))
		# define in Pins for ends stop button
		# assign the event
		#GPIO.add_event_detect(self.buttonA, GPIO.RISING, callback = self.calibrateButton_callback)

	def dispose(self):
		GPIO.output(self.motorChannel,(0,0,0,0))
		
		
	# set speed in percent
	def setSpeed(self, speed):
		self.sleeptime= self.minsleeptime*100/speed

	# set endstop gpio port
	def setEndstop(self, endstopport):
		self.endstopbutton = endstopport
		GPIO.setup(self.endstopbutton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.add_event_detect(self.endstopbutton, GPIO.FALLING, callback=self.endstopCallback)  

	# do step forward
	def doStep(self, count):
		self.loopStop = False

		direction=1
		if count < 0:
			direction= (-1)

		for xi in range (abs(count)):
			self.currentPosition += direction
			GPIO.output(self.motorChannel, self.stepPattern[self.currentPosition%8])  
			sleep (self.sleeptime)
			if self.loopStop:
				break;
				
	#callback button pressed
	def calibrate(self):
		while GPIO.input(self.endstopbutton)!=1:
			self.doStep( 100)
			self.currentPosition=0

	#callback button pressed
	def endstopCallback(self,port ):
		# print("GPIO.input() - Button pressed - stop loop")
		# print "port"
		#print port
		# print "self"
		# print self
		self.loopStop = True
		self.endStop = True
