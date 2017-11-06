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

	currentPosition = 0
	buttonA=21 #Pin 40

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
		print (" self = " + self.__class__.__name__)
		

	# init. a,b,c,d are the contoling gpio ports
	def __init__(self,a,b,c,d):
		# init step position
		self.currentPosition = 0
		self.motorChannel = [a,b,c,d]
		print self
		print a,b,c,d
		# define by GPIO numbers, not board numbers
		GPIO.setmode(GPIO.BCM)
		# define out pins
		GPIO.setup(self.motorChannel, GPIO.OUT)
		GPIO.output(self.motorChannel,(0,0,0,0))
		# define in Pins for ends stop button
		GPIO.setup(self.buttonA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		# assign the event
		#GPIO.add_event_detect(self.buttonA, GPIO.RISING, callback = self.calibrateButton_callback)

	def dispose(self):
		print ("GPIO.cleanup()")
		GPIO.output(self.motorChannel,(0,0,0,0))
		
		
	# set speed in percent
	def setSpeed(self, speed):
		self.sleeptime= self.minsleeptime*100/speed

	# do step forward
	def doStep(self, count):
		self.loopStop = False
		print self.currentPosition
		direction=1
		if count < 0:
			direction= (-1)
		print direction			
		
		for xi in range (abs(count)):
			self.currentPosition += direction
			GPIO.output(self.motorChannel, self.stepPattern[self.currentPosition%8])  
			self.currentPosition
			sleep (self.sleeptime)
			if self.loopStop:
				break;

	# do step forward
	def doStepForward(self, count):
		self.loopStop = False
		for xi in range (count):
			self.currentPosition += 1
			GPIO.output(self.motorChannel, self.stepPattern[self.currentPosition%8])  
			sleep (self.sleeptime)
			if self.loopStop:
				break;

			
	# do step backward
	def doStepBackward(self, count):
		self.loopStop = False
		gpioMotorLoopStop = ""
		for xi in range (count): 
			self.currentPosition -= 1
			GPIO.output(self.motorChannel, self.stepPattern[7-self.currentPosition%8])	 
			sleep (self.sleeptime)
			if self.loopStop:
				break;
		
	#callback button pressed
	def calibrateButton_callback(buttonAclass, Test1):
		print("GPIO.input() - Button pressed - stop loop")
		buttonAclass.loopStop = True
