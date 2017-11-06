#!/usr/bin/python
import RPi.GPIO as GPIO
import GpioMotor 

import sys

def getch():   # define non-Windows version
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch
 
def keypress():
    global char
    char = getch()

print("Test 2 Motoren")

stepsPerRound = 4096
#motor1 = GpioMotor.gpioMotor(4,17,27,22)
motor1 = GpioMotor.gpioMotor(18,23,24,25)


motor1.setSpeed(100)	
motor1.doStep(-8500)
motor1.doStep(8500)
#motor1.doStep(-3000)


#motor2.doStepForward(4096)
#motor2.info()
#motor2.dispose()

GPIO.cleanup()	
