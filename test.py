#!/usr/bin/python
# coding: utf8
from time import sleep
import RPi.GPIO as GPIO

# GPIO Ports
motorA1=18
motorA2=23
motorA3=24
motorA4=25

stepsDefined = 8
currStep = 0
loopStop = False
GPIO.setmode(GPIO.BCM) # gpio numbers NOT pin numbers

chan_A = [motorA1,motorA2,motorA3,motorA4]

# define out pins
GPIO.setup(chan_A, GPIO.OUT)
GPIO.output(chan_A,(0,0,0,0))

minsleeptime = 0.0006
speed = 100 # in percent 110% möglich
sleeptime= minsleeptime*100/speed

matrix= [
	[1,0,0,0],
	[1,1,0,0],
	[0,1,0,0],
	[0,1,1,0],
	[0,0,1,0],
	[0,0,1,1],
	[0,0,0,1],
	[1,0,0,1]]

for i in range(4096):
	GPIO.output(chan_A, matrix[i%8])  
	sleep (sleeptime)
for i in range(4096):
	GPIO.output(chan_A, matrix[7-(i%8)])  
	sleep (sleeptime)

GPIO.cleanup()
