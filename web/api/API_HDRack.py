#!/usr/bin/python
# coding: utf8
from tornado import websocket, web, ioloop

from Common import BaseHandler


#
# HDRack worker class
#        
class HDRackWorker():
    # init
    def __init__(self, socketHandler):
        # check if gpio exists
        self.gpioExists = True
        self.ElevatorMotor = None
        self.ConnectorMotor = None
        try:
            import RPi.GPIO as GPIO
        except ImportError:
            self.gpioExists = False
        self.socketHandler = socketHandler
        print("HDRackWorker: init gpioExists:", self.gpioExists)

        # init motors
        if self.gpioExists:
            print ("init motors")
            # load GpioMotor
            import GpioMotor
        
            #Elevator
            #Elevator Slot
            self.stepsPerSlot = 400
            #Elevator Motor
            self.stepsPerRound = 4096

            self.stepsPerKey = 100
            self.stepsToConnect = 1830

            self.ElevatorMotor = GpioMotor.GpioMotor("Elevator", 21, 23, 19)
            #ElevatorMotor1.SetEndstop(18)
            self.ElevatorMotor.SetSendMessage(socketHandler.SendMessage)

            self.ConnectorMotor = GpioMotor.GpioMotor("Connector", 3, 5, 7)
            #ConnectorMotor1.SetEndstop(26) 
            self.ConnectorMotor.SetSendMessage(socketHandler.SendMessage)

    # info motor
    def InfoMotor(self, motorName):
        if motorName == "Connector":
            return self.ConnectorMotor.Info()
        else:
            return self.ElevatorMotor.Info()

    # reset motor
    def ResetMotor(self, motorName):
        if motorName == "Connector":
            return self.ConnectorMotor.DoReset()
        else:
            return self.ElevatorMotor.DoReset()

    # power off
    def PowerOffMotor(self, motorName):
        retJson = {}
        if motorName == "Connector":
            self.ConnectorMotor.PowerOff()
            retJson = self.ConnectorMotor.Info()
        else:
            self.ElevatorMotor.PowerOff()
            retJson = self.ElevatorMotor.Info()
        return retJson

    # move Elevator, up and down
    def MoveElevator(self, direction, steps):
        retJson = {}
        self.ElevatorMotor.PowerOn()
        #Im Uhrzeiger, hoch
        if direction == "up":
            print ("HDRackWorker: move up", retJson)
       	    retJson = self.ElevatorMotor.DoStep(steps)
        #gegen den Uhrzeiger, runter
        if direction == "down":
            print ("HDRackWorker: move down", retJson)
            retJson = self.ElevatorMotor.DoStep(steps * -1)
        #self.ElevatorMotor.PowerOff()
        return retJson

    # move Connector, in and out
    def MoveConnector(self, direction, steps):
        retJson = {}
        self.ConnectorMotor.PowerOn()
        #Im Uhrzeiger, rein
        if direction == "in":
            print ("HDRackWorker: move in", retJson)
       	    retJson = self.ConnectorMotor.DoStep(steps)
        #gegen den Uhrzeiger, raus
        if direction == "out":
            print ("HDRackWorker: move out", retJson)
            retJson = self.ConnectorMotor.DoStep(steps * -1)
        self.ConnectorMotor.PowerOff()
        return retJson


class MotorHandler(BaseHandler):
    def initialize(self, hdrackWork):
        self.hdrackWork = hdrackWork
        print("MotorHandler init gpioExists:", self.hdrackWork.gpioExists)

    @web.asynchronous
    def get(self, motorName, command):
        if self.hdrackWork.gpioExists == False:
            retJson = { "name": motorName, "error": "no device" }
            self.hdrackWork.socketHandler.SendMessage("motorinfo", retJson)
            self.write(retJson)
            self.finish()
            return

        print("  ---  MotorHandler, motorName, command", motorName, command)

        retJson = { "name": motorName, "command": command }

        # info
        if command == "info":
            retJson = self.hdrackWork.InfoMotor(motorName)

        # elevator up
        elif command.startswith("up"):
            steps = int(command.replace("up", ""))
            if command == "up":
                steps = self.hdrackWork.stepsPerKey
            retJson = self.hdrackWork.MoveElevator("up", steps)
        #elevator down
        elif command.startswith("down"):
            steps = int(command.replace("down", ""))
            print("down steps", steps)
            if command == "down":
                steps = self.hdrackWork.stepsPerKey
            retJson = self.hdrackWork.MoveElevator("down", steps)

        #connector forward
        elif command.startswith("forward"):
            steps = int(command.replace("forward", ""))
            if command == "forward":
                steps = self.hdrackWork.stepsPerKey
            retJson = self.hdrackWork.MoveConnector("in", steps)
        #connector backward
        elif command.startswith("backward"):
            steps = int(command.replace("backward", ""))
            if command == "forward":
                steps = self.hdrackWork.stepsPerKey
            retJson = self.hdrackWork.MoveConnector("out", steps)

        elif command == "slot":
            #if ConnectorMotor1.currentPosition > 0:
            #	ConnectorMotor1.doStep(stepsToConnect);
            slotNo = int(self.get_argument('slotno', None, True))
            if slotNo == 1:
                stepsToSlot = 115
            if slotNo == 2:
                stepsToSlot = 180
            if slotNo == 3:
                stepsToSlot = 247
            if slotNo == 4:
                stepsToSlot = 314
            if slotNo == 5:
                stepsToSlot = 376
            steps = stepsToSlot - int(motor.currentPosition)
            print("slot, stepsPerSlot, stepsToSlot, steps, currentPosition ", slotNo, stepsPerSlot, stepsToSlot, steps, motor.currentPosition)
            robotWork.ConnectToSlot(slotNo)
            retJson = motor.doStep(steps)

        #power off
        elif command == "poweroff":
            retJson = self.hdrackWork.PowerOffMotor(motorName)
        #reset
        elif command == "reset":
            retJson = self.hdrackWork.ResetMotor(motorName)
        else:
            retJson = { "Motor": command }

        self.hdrackWork.socketHandler.SendMessage("motorinfo", retJson)
        print ("retJson ", retJson)
        self.write(retJson)
        self.finish()

class MotorHandlerB(web.RequestHandler):
    def initialize(self, gpioExists, socketHandler):
        self.gpioExists = gpioExists
        self.socketHandler = socketHandler
        print("MotorHandler init gpioExists:", gpioExists)

    @web.asynchronous
    def get(self, motorName, command):
        if self.gpioExists == False:
            retJson = { "name": motorName, "error": "no device" }
            self.socketHandler.SendMessage("motorinfo", retJson)
            self.write(retJson)
            self.finish()
            return

        motor = ElevatorMotor1
        if motorName == "Connector":
            motor = ConnectorMotor1

        print("  ---  MotorHandler, motorName, command", motorName, command)

        if command == "info":
            retJson = motor.info()
        elif command == "slot":
            #if ConnectorMotor1.currentPosition > 0:
            #	ConnectorMotor1.doStep(stepsToConnect);
            slotNo = int(self.get_argument('slotno', None, True))
            stepsToSlot = stepsPerSlot * slotNo * -1
            if slotNo == 1:
                stepsToSlot = -200
            if slotNo == 2:
                stepsToSlot = -1470
            if slotNo == 3:
                stepsToSlot = -2840
            if slotNo == 4:
                stepsToSlot = -4440
            if slotNo == 5:
                stepsToSlot = -5700
            steps = stepsToSlot - int(motor.currentPosition)
            print("slot, stepsPerSlot, stepsToSlot, steps, currentPosition ", slotNo, stepsPerSlot, stepsToSlot, steps, motor.currentPosition)
            robotWork.ConnectToSlot(slotNo)
            retJson = motor.doStep(steps)
        #connect
        elif command == "connect":
            steps = stepsToConnect
            retJson = motor.doStep(steps * -1)
        #release
        elif command == "release":
            steps = stepsToConnect
            retJson = motor.doStep(steps)
        #forward
        elif command.startswith("forward"):
            steps = int(command.replace("forward", ""))
            if command == "forward":
                steps = stepsPerKey
            retJson = motor.doStep(steps * -1)
        #backward
        elif command.startswith("backward"):
            steps = int(command.replace("backward", ""))
            if command == "backward":
                steps = stepsPerKey
            retJson = motor.doStep(steps)
        #up
        elif command.startswith("up"):
            steps = int(command.replace("up", ""))
            if command == "up":
                steps = stepsPerKey
            retJson = motor.doStep(steps * -1)
        #down
        elif command.startswith("down"):
            steps = int(command.replace("down", ""))
            print("down steps", steps)
            if command == "down":
                steps = stepsPerKey
            retJson = motor.doStep(steps)
        #calibrate
        elif command == "calibrate":
            retJson = motor.doCalibrate()
        #reset
        elif command == "reset":
            retJson = motor.doReset()
        else:
            retJson = { "Motor": command }

        SocketHandler.SendMessage("motorinfo", retJson)
        print ("retJson ", retJson)
        self.write(retJson)
        self.finish()

    @web.asynchronous
    def post(self):
        pass
