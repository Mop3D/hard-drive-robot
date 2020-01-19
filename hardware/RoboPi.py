#!/usr/bin/python
# coding: utf8

"""
RoboPi.py

date: 18.01.2020
author: oliver Klepach, Martin Weichselbaumer
"""

import json
import os
import signal
import sys, getopt
cl = []

import RPi.GPIO as GPIO
import GpioMotor 

opts,args = getopt.getopt(sys.argv[1:], "hd:s:t:", ["direction=", "steps=", "slot="])

direction = "up"
steps = 0
slot = 0
poweroff = False
for opt, arg in opts:
	if opt == "-h":
		print "RoboPy.py -d --direction <up|down|in|out|slot|calibrate|poweroff> -s --steps <steps>"
	elif opt in ("-d", "--direction"):
		direction = arg
	elif opt in ("-s", "--steps"):
		steps = int(arg)
	elif opt in ("-t", "--slot"):
		slot = int(arg)

if direction == "slot" and (slot < 0 or slot > 6):
	print ("slot missing on not 1-6 or 0, use -t")
	sys.exit(1)

# 1 step = 0,4675 mm
# 112 Steps to Slot one
# 67 to next slots
# 75 in and out
#


#Elevator
#Elevator Slot
stepsToFirstSlot = 100
stepsPerSlot = 67
#Connector
stepsToConnect = 75



#Elevator Motor
stepsPerRound = 4096

stepsPerKey = 10

if direction == "up" or direction == "down" or direction == "slot":
	# name, direction, step
	# init activate power - motor becomes hot
	ElevatorMotor1 = GpioMotor.GpioMotor("Elevator", 21, 23, 19)
	ElevatorMotor1.SetEndstop(13)
	##not yet -> handling of sleepPin missing - ElevatorMotor1.powerOff()
	motorName = "Elevator"
	motor = ElevatorMotor1
if direction == "in" or direction == "out":
	# name, direction, step
	# init activate power - motor becomes hot
	ConnectorMotor1 = GpioMotor.GpioMotor("Connector", 3, 5, 7)
	#ConnectorMotor1.setEndstop(11)
	#ConnectorMotor1.powerOff()
	motorName = "Connector"
	motor = ConnectorMotor1

if direction == "poweroff":
	motorName = "PowerOff"
	print("PowerOff")
	ElevatorMotor1 = GpioMotor.GpioMotor("Elevator", 21, 23, 19)
	ElevatorMotor1.PowerOff()
	ConnectorMotor1 = GpioMotor.GpioMotor("Connector", 3, 5, 7)
	ConnectorMotor1.PowerOff()


command = "dostep"
if steps == 0:
	steps = stepsPerKey

print("MotorHandler, motorName, command, direction, steps", motorName, command, direction, steps)

# zu einem bestimmten Slot fahren 
if direction == "slot" and slot != 0:
	steps = 500
	retJson = motor.DoStep(steps * -1)
	# goto slot
	steps = stepsToFirstSlot + ((slot -1) * stepsPerSlot)
	print("steps to slot", steps)
	retJson = motor.DoStep(steps)
# auf init position fahren
if direction == "slot" and slot == 0:
	steps = 500
	print("steps to slot", steps)
	retJson = motor.DoStep(steps * -1)

# Elevator: rauf und runter
#Im Uhrzeiger, rauf
if direction == "up":
	motor.PowerOn()
	retJson = motor.DoStep(steps)
	print ("retJson ", retJson)
#gegen den Uhrzeiger, runter
if direction == "down":
	motor.PowerOn()
	retJson = motor.DoStep(steps * -1)
	print ("retJson ", retJson)

# Connector, rein und raus
#Im Uhrzeiger, rein
if direction == "in":
	motor.PowerOn()
	retJson = motor.DoStep(steps)
	motor.PowerOff()
	print ("retJson ", retJson)
#gegen den Uhrzeiger, raus
if direction == "out":
	motor.PowerOn()
	retJson = motor.DoStep(steps * -1)
	motor.PowerOff()
	print ("retJson ", retJson)

if direction == "calibrate":
	motor.PowerOn()
	retJson = motor.DoCalibrate()
	print ("retJson ", retJson)

if direction == "testendstop":
	motor.PowerOn()
	retJson = motor.TestEndStop()
	print ("retJson ", retJson)
	motor.PowerOff()


#class MotorHandler():
#
#	def get(self, motorName, command):
#		motor = ElevatorMotor1
#
#		print("MotorHandler, motorName, command", motorName, command)
#
#		if command == "info":
#			retJson = motor.info()
#		elif command == "slot":
#			slotNo = self.get_argument('slotno', None, True)
#			stepsToSlot = ((stepsPerSlot * int(slotNo)) - int(motor.currentPosition)) * -1
#			print("slot, stepsToSlot, currentPosition", slotNo, stepsToSlot, motor.currentPosition)
#			retJson = motor.doStep(stepsToSlot)
#		elif command == "forward":
#			retJson = motor.doStep(stepsPerKey)
#		elif command == "backward":
#			retJson = motor.doStep(stepsPerKey * -1)
#		elif command == "calibrate":
#			retJson = motor.doCalibrate()
#		else:
#			retJson = { "Motor": command }
#
#		print ("retJson ", retJson)
#		self.write(retJson)
#		self.finish()

