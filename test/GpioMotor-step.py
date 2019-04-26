#!/usr/bin/python
# coding: utf8
from time import sleep
import RPi.GPIO as GPIO

MODE = (11, 13, 15) # Microstep Resolution GPIO Pins
#Elevator
DIRM1 = 16 # Direction GPIO Pin
STEPM1 = 18 # Step GPIO Pin
#Connector
#DIR = 22 # Direction GPIO Pin
#STEP = 24 # Step GPIO Pin

CW = 1 # Clockwise Rotation
CCW = 0 # Counterclockwise Rotation
SPR = 510 # Steps per Revolution (360 / 7.5)

# Bananapi settings
# define by GPIO Board, not numbers / Bananpi
GPIO.setmode(GPIO.BOARD)
#GPIO.setmode(GPIO.BCM)

GPIO.setup(DIRM1, GPIO.OUT)
GPIO.setup(STEPM1, GPIO.OUT)
GPIO.output(DIRM1, CW)

# Bananapi settings
# define out pins
for mChannel in MODE:
	GPIO.setup(mChannel, GPIO.OUT)
#GPIO.setup(MODE, GPIO.OUT)

RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}

GPIO.output(11, GPIO.HIGH)
GPIO.output(13, GPIO.LOW)
GPIO.output(15, GPIO.HIGH)
#GPIO.output(MODE, RESOLUTION['1/32'])
step_count = SPR * 32
delay = .0208 / 32

GPIO.output(DIRM1, CCW)

#step_count = SPR delay = .0208
for x in range(step_count):
    print(x)
    GPIO.output(STEPM1, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEPM1, GPIO.LOW)
    sleep(delay)

sleep(.5)
GPIO.output(DIRM1, CW)

for x in range(step_count):
    print(x)
    GPIO.output(STEPM1, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEPM1, GPIO.LOW)
    sleep(delay)



GPIO.output(STEPM1, GPIO.LOW)

GPIO.cleanup()
