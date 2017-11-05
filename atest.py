#!/usr/bin/python
import RPi.GPIO as GPIO
import GpioMotor 
print("Test 2 Motoren")

stepsPerRound = 4096
motor1 = GpioMotor.gpioMotor(18,23,24,25)
motor2 = GpioMotor.gpioMotor(2,3,4,17)
	
	
motor1.doStepForward(1000)
motor1.info()
motor2.doStepForward(1000)
motor2.info()
	
motor1.dispose()
motor2.dispose()
GPIO.cleanup()	
