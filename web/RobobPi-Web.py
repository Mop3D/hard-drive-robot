#!/usr/bin/python
# coding: utf8
from tornado import websocket, web, ioloop
import tornado.autoreload
import json
import os
import signal

cl = []

static_path_dir = '/static'
settings = {
	'debug': True,
	'autoreload': True,
	'static_path': '/home/pi/web/static'
}

import RPi.GPIO as GPIO
import GpioMotor 

#Elevator
#Elevator Slot
stepsPerSlot = 400
#Elevator Motor
stepsPerRound = 4096
# motor1 11,16,18,22 Motor alleine
# motor1 11, 13, 15, 16 Endstop 18 Robot
# motor2 19, 21, 23, 24 Endstop 26 Robot
ElevatorMotor1 = GpioMotor.gpioMotor("Elevator", 11, 13, 15, 16)
ElevatorMotor1.setSpeed(50)	
ElevatorMotor1.setEndstop(18)

ConnectorMotor1 = GpioMotor.gpioMotor("Connector", 19, 21, 23, 24)
ConnectorMotor1.setSpeed(50)	
#ConnectorMotor1.setEndstop(26)
ConnectorMotor1.powerOff()

stepsPerKey = 100
stepsToConnect = 1830

class IndexHandler(web.RequestHandler):
	def get(self):
		self.render("templates/index.html")

class ApiHandler(web.RequestHandler):

	@web.asynchronous
	def get(self, *args):
		self.finish()
		retJson = { }
		return json.dumps(retJson)

		
		value = self.get_argument("value")
		data = {"id": id, "value" : value}
		data = json.dumps(data)
		for c in cl:
			c.write_message(data)

	@web.asynchronous
	def post(self):
		pass

class MotorHandler(web.RequestHandler):

	@web.asynchronous
	def get(self, motorName, command):
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

class SocketHandler(websocket.WebSocketHandler):
	def check_origin(self, origin):
		return True

	def open(self):
		print ("open socket")
		if self not in cl:
			cl.append(self)
		ElevatorMotor1.setSendMessage(SocketHandler.SendMessage)
		ConnectorMotor1.setSendMessage(SocketHandler.SendMessage)
		
	def on_close(self):
		print ("open closed")
		if self in cl:
			cl.remove(self)
		ElevatorMotor1.setSendMessage(None)
		ConnectorMotor1.setSendMessage(None)

	@staticmethod
	def SendMessage(command, data):
		retJson = { "command": command, "data": data }
		for webSocket in cl:
			webSocket.write_message(retJson)


def signalHandler(signum, frame):
	SocketHandler.SendMessage("signalhandler", {})
	print ("send signal")
	signal.setitimer(signal.ITIMER_REAL, 5)

signal.signal(signal.SIGALRM, signalHandler)
#signal.setitimer(signal.ITIMER_REAL, 5)

			
app = web.Application(
	[
	(r'/', IndexHandler),
	(r'/ws', SocketHandler),
	(r'/api', ApiHandler),
	#(r'/motor/([0-9]+)', MotorHandler),
	(r'/motor/(.*)/(.*)', MotorHandler), #/motor/motorName/Command
	#(r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
	#(r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
	(r'/static/(.*)', web.StaticFileHandler, {'path': static_path_dir})
	],
	**settings
)

if __name__ == '__main__':
	print ("start app on 8888")
	app.listen(8888)
	#auto reload after file change
	#TODO remove in prod
	#tornado.autoreload.start()
	#for dir, _, files in os.walk('static'):
	#	 print (dir)
	#	 [tornado.autoreload.watch(dir + '/' + f) for f in files if not f.startswith('.')]
	#
	ioloop.IOLoop.instance().start()
