#!/usr/bin/python
# coding: utf8

"""
GpoiMotor.py

version: 2020-01-19-2
date: 19.01.2020
author: oliver Klepach, Martin Weichselbaumer
"""

from time import sleep
import RPi.GPIO as GPIO

class GpioMotor(object):
	"""Motor - GPIO out"""
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)

	name = 'motor'
	currentPosition = 0
	endStop = False

	waitDelay = .0208 / 32
	#waitDelay = .0208 / 16

	sendMessage = None

	# init. name of the motor, a,b,c,d are the contoling gpio ports
	# if powerOffAfterCommand == True allways Power Off after the command is thru
	def __init__(self, name, directionPin, stepPin, sleepPin, powerOffAfterCommand):
		self.name = name
		# init step position
		self.directionPin = directionPin
		self.stepPin = stepPin
		self.sleepPin=sleepPin
		self.endStopButtonPin = 0
		self.powerOffAfterCommand = powerOffAfterCommand
		self.endStop=False
		print (" *****channels = " + str(self.directionPin) + "/" + str(self.stepPin) + "/" +str(self.sleepPin))

		# define out pins
		GPIO.setup(directionPin, GPIO.OUT)
		GPIO.setup(stepPin, GPIO.OUT)
		GPIO.setup(sleepPin, GPIO.OUT)
		# allways set to off - NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
		#GPIO.output(self.sleepPin, GPIO.LOW)

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
		#if not GPIO.input(self.stepPin):
		#	GPIO.output(self.sleepPin, GPIO.HIGH)			
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
		self.endStopButtonPin = endstopport
		GPIO.setup(self.endStopButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
				# change to PULL-UP
				#GPIO.setup(self.endstopbutton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		print ("set Endstop", self.endStopButtonPin)
			#if not GPIO.input(self.endstopbutton):
		if GPIO.input(self.endStopButtonPin):
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
		GPIO.add_event_detect(self.endStopButtonPin, GPIO.RISING, callback=self.EndstopCallback)  
		
	# set endstop gpio port
	def TestEndStop(self):
		print ("Test End Stop", self.endStopButtonPin)
		xx1 = 0
		for xi in range (2000):
			sleep (1)
			print ("    status: ", GPIO.input(self.endStopButtonPin))
		print ("Test End Stop", self.endStopButtonPin)


	# do step
	def DoStep(self, count):
		self.PowerOn()
		direction=1
		if count < 0:
			direction = (-1)
		print("DoStep count, direction, endStop", count, direction, self.endStop)

		# if endStop and direction down, exit
		if direction == -1 and self.endStop:
			print ("break init endStop")
			return

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
		
		# set endStop to False when direction is up
		if direction == 1:
			self.endStop = False

		if self.powerOffAfterCommand:
			self.PowerOff()

		return self.Info()
		
	#do while endstop button pressed
	def DoCalibrate(self):
		self.DoStep(-1000)
		self.PowerOff()
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
