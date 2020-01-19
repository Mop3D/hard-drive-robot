#!/usr/bin/python
# coding: utf8

"""
GpoiMotor.py

date: 19.01.2020
author: oliver Klepach, Martin Weichselbaumer
"""

from time import sleep
import RPi.GPIO as GPIO

class GpioMotor(object):
	"""Motor - GPIO out"""
	GPIO.setmode(GPIO.BOARD)

	name = 'motor'
	currentPosition = 0
	endStop = False
	endstopbutton = 0

	waitDelay = .0208 / 32
	#waitDelay = .0208 / 16

	sendMessage = None

	# init. name of the motor, a,b,c,d are the contoling gpio ports
	def __init__(self, name, directionPin, stepPin, sleepPin):
		self.name = name
		# init step position
		self.directionPin = directionPin
		self.stepPin = stepPin
		self.endStop=False
		self.sleepPin=sleepPin
		print (" *****channels = " + str(self.directionPin) + "/" + str(self.stepPin) + "/" +str(self.sleepPin))

		# define out pins
		GPIO.setup(directionPin, GPIO.OUT)
		GPIO.setup(stepPin, GPIO.OUT)
		GPIO.setup(sleepPin, GPIO.OUT)
		# allways set to off
		GPIO.output(self.sleepPin, GPIO.LOW)

	# set SendMessage method
	def SetSendMessage(self, SendMessage):
		self.sendMessage = SendMessage

	# info
	def Info(self):
		print ('\n--- motor info --- ')
		print (" channels = " + str(self.directionPin) + "/" + str(self.stepPin) + "/" +str(self.sleepPin))
		print (" currentPosition = " + str(self.currentPosition))
		print (" self = " + self.__class__.__name__)
		info = { "name": self.name, "channels": str(self.directionPin) + "/" + str(self.stepPin) +"/"+str(self.sleepPin), "currentPosition": self.currentPosition }
		if self.sendMessage:
			self.sendMessage("statusinfo", info)
		return info

	# set powerOn
	def PowerOn(self):
		print ("GPIO.powerOn() ", GPIO.input(self.stepPin))
		if not GPIO.input(self.stepPin):
			GPIO.output(self.sleepPin, GPIO.HIGH)			

	# set powerOff
	def PowerOff(self):
		print ("GPIO.powerOff()")
		GPIO.output(self.directionPin, GPIO.LOW)
		GPIO.output(self.stepPin, GPIO.LOW)
		GPIO.output(self.sleepPin, GPIO.LOW)

	# dispose
	def Dispose(self):
		print ("GPIO.cleanup()")
		GPIO.output(self.directionPin, GPIO.LOW)
		GPIO.output(self.stepPin, GPIO.LOW)
		GPIO.output(self.sleepPin, GPIO.LOW)

	# set endstop gpio port
	def SetEndstop(self, endstopport):
		self.endstopbutton = endstopport
		GPIO.setup(self.endstopbutton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		# change to PULL-UP
		#GPIO.setup(self.endstopbutton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		print ("set Endstop", self.endstopbutton)
		#if not GPIO.input(self.endstopbutton):
		if GPIO.input(self.endstopbutton):
			self.endStop = True
		print ("Endstop", self.endStop)

		#xi = 0
		#while 1:
		#	if not GPIO.input(self.endstopbutton):
		#		print ("Pressed " + str(xi) )
		#		xi = xi + 1
		# call when Button Released
		#GPIO.add_event_detect(self.endstopbutton, GPIO.FALLING, callback=self.EndstopCallback)  
		# call when Button Pressed
		GPIO.add_event_detect(self.endstopbutton, GPIO.RISING, callback=self.EndstopCallback)  
		
	# set endstop gpio port
	def TestEndStop(self):
		print ("Test End Stop", self.endstopbutton)
		xx1 = 0
		for xi in range (2000):
			sleep (1)
			print ("    status: ", GPIO.input(self.endstopbutton))
		print ("Test End Stop", self.endstopbutton)


	# do step
	def DoStep(self, count):
		direction=1
		if count < 0:
			direction= (-1)
		if direction == -1 and self.endStop:
			print ("break init endStop")
			return
		# TODO:
		#if GPIO.input(self.endstopbutton)==1 and direction>0:
		#	return self.info()

		print(self.directionPin)
		if direction>0: # Clockwise Rotation
			print("Clockwise")
			GPIO.output(self.directionPin, GPIO.HIGH)
		else: # Counterclockwise Rotation
			print("Counterclockwise")
			GPIO.output(self.directionPin, GPIO.LOW)
		print ("direction", direction, self.endStop)
		for xi in range (abs(count)):
			# down until button pressed
			if direction == -1 and self.endStop:
				self.endStop = False
				print ("break loop")
				break
			self.currentPosition += direction
			GPIO.output(self.stepPin, GPIO.HIGH)
			sleep (self.waitDelay * 10)
			GPIO.output(self.stepPin, GPIO.LOW)
			sleep (self.waitDelay * 10)

		print ("after loop")

		return self.Info()
		
	#do while endstop button pressed
	def DoCalibrate(self):
		self.DoStep(1000)
		self.currentPosition=0
		return self.Info()
	
	# reset
	def DoReset(self):
		self.currentPosition=0
		self.PowerOff()
		return self.Info()
	#emulate gpio.output with arrays
	def GpioOutput(self, channelArray, valueArray):
		for channelCount in range(len(channelArray)):
			GPIO.output(channelArray[channelCount], valueArray[channelCount])

	#callback button pressed
	def EndstopCallback(self,port):
		print("     -----> GPIO.input() - Button pressed - stop loop")
		self.endStop = True
		self.currentPosition = 0

	#callback button released
	def EndstopCallbackReleased(self,port):
		print("     -----> GPIO.input() - Button released - stop loop")
