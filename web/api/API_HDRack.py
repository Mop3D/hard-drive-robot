#!/usr/bin/python
# coding: utf8

"""
API_HDRack.py

date: 19.01.2020
author: oliver Klepach, Martin Weichselbaumer
"""

from tornado import websocket, web, ioloop

from Common import hdRoboCfg, BaseHandler


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
            # removes message: RuntimeWarning: This channel is already in use, continuing anyway.
            GPIO.setwarnings(False)

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

            elevatorRackCfg = hdRoboCfg["Rack"]["Elevator"]
            print("HDRackWorker: config Rack", elevatorRackCfg)

            #self.ElevatorMotor = GpioMotor.GpioMotor("Elevator", 21, 23, 19)
            self.ElevatorMotor = GpioMotor.GpioMotor("Elevator", int(elevatorRackCfg["DirectionPin"]), int(elevatorRackCfg["StepPin"]), int(elevatorRackCfg["SleepPin"]), False)
            #ElevatorMotor1.SetEndstop(13)
            if "StopPin" in elevatorRackCfg:
                self.ElevatorMotor.SetEndstop(int(elevatorRackCfg["StopPin"]))
            self.ElevatorMotor.SetSendMessage(socketHandler.SendMessage)

            self.ConnectorMotor = GpioMotor.GpioMotor("Connector", 3, 5, 7, True)
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

    # calibrate motor
    def CalibrateMotor(self, motorName):
        if motorName == "Connector":
            return self.ConnectorMotor.DoCalibrate()
        else:
            return self.ElevatorMotor.DoCalibrate()

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
        #Im Uhrzeiger, hoch
        if direction == "up":
            print ("HDRackWorker: move up", retJson)
       	    retJson = self.ElevatorMotor.DoStep(steps)
        #gegen den Uhrzeiger, runter
        if direction == "down":
            print ("HDRackWorker: move down", retJson)
            retJson = self.ElevatorMotor.DoStep(steps * -1)
        return retJson

    # move Connector, in and out
    def MoveConnector(self, direction, steps):
        retJson = {}
        #Im Uhrzeiger, rein
        if direction == "in":
            print ("HDRackWorker: move in", retJson)
       	    retJson = self.ConnectorMotor.DoStep(steps)
        #gegen den Uhrzeiger, raus
        if direction == "out":
            print ("HDRackWorker: move out", retJson)
            retJson = self.ConnectorMotor.DoStep(steps * -1)
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
        # move to Slot
        elif command == "slot":
            slotNo = int(self.get_argument('slotno', None, True))
            if slotNo == 1:
                stepsToSlot = 107
            if slotNo == 2:
                stepsToSlot = 169
            if slotNo == 3:
                stepsToSlot = 237
            if slotNo == 4:
                stepsToSlot = 305
            if slotNo == 5:
                stepsToSlot = 373
            steps = stepsToSlot
            retJson = self.hdrackWork.MoveElevator("up", steps)
            print("slot, stepsToSlot, steps, currentPosition ", slotNo, stepsToSlot, steps)
        # connect HD
        elif command == "connect":
            steps = 75
            retJson = self.hdrackWork.MoveConnector("in", steps)
        # release HD
        elif command == "release":
            steps = 75
            retJson = self.hdrackWork.MoveConnector("out", steps)
        #power off
        elif command == "poweroff":
            retJson = self.hdrackWork.PowerOffMotor(motorName)
        # calibrate
        elif command == "calibrate":
            retJson = self.hdrackWork.CalibrateMotor(motorName)
        #reset
        elif command == "reset":
            retJson = self.hdrackWork.ResetMotor(motorName)
        else:
            retJson = { "Motor": command }

        self.hdrackWork.socketHandler.SendMessage("motorinfo", retJson)
        print ("retJson ", retJson)
        if retJson is not None:
            self.write(retJson)
        self.finish()
