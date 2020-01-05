#!/usr/bin/python
# coding: utf8
from tornado import websocket, web, ioloop

class MotorHandlerB(web.RequestHandler):
    def initialize(self, gpioExists):
        self.gpioExists = gpioExists
        print("MotorHandler init gpioExists:", gpioExists)

    @web.asynchronous
    def get(self, motorName, command):
        if self.gpioExists == False:
            return

        print("MotorHandler get gpioExists:", self.gpioExists)
        pass

class MotorHandler(web.RequestHandler):
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
