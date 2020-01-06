#!/usr/bin/python
#modul Elevator
import GpioMotor 

class Steuerung(object):
    """Motorsteuerung"""
    minPos = 0
    maxPos = 1000
    stepsPerRound = 4096
    motor1 = GpioMotor.gpioMotor(4,17,27,22)
	
	#init
    def __init__(self):
        currPos = 0

    # dispose object
    def dispose(self):
        self.motor1.dispose()

    # info
    def info(self):
        print ('\n--- info --- ')
        print (" motor 1 = " + str(self.motor1.info))


    # calibrate
    def calibrate(self):
        print ('calibrate currPos = %s' % (self.currPos))
        self.motor1.doStepBackward(10000)
        print (" after calibrate currPos = " + str(self.info))

    # stepForward
    def stepForward(self, units):
        print ('stepForward %s' % (units))
        self.motor1.doStepForward(units)
        print (" after stepForward currPos = " + str(self.motor1.info))

    #stepBackward
    def stepBackward(self, units):
        print ('stepBackward %s' % (units))
        self.motor1.doStepBackward(units)
        print (" after stepBackward currPos = " + str(self.motor1.info))

