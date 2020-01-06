#!/usr/bin/python
# coding: utf8
from time import sleep
import RPi.GPIO as GPIO
import sys, tty, termios
import GpioMotor 
import sys
import curses
import random
import time
import locale


def main(stdscr):
	locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')
	
	# motor1 17, 27, 22, 23 Endstop 24
	# motor2 10, 9, 11, 8 Endstop 7
	
	motor1 = GpioMotor.gpioMotor(17,27,22,23)
	motor1.setSpeed(50)	
	motor1.setEndstop( 24 ) 
	
	motor3 = GpioMotor.gpioMotor(10,9,11,8)
	motor3.setSpeed(20)	
	motor3.setEndstop(7)
	
	stepsize  = 100
	screen = curses.initscr()
	screen.keypad(True)
	curses.noecho()
	curses.cbreak() 
	a = u'\2503'.encode('utf-8')
	
	screen.border( 0x2500,'-',chr(126),'+','+','+')
	screen.nodelay(True)
	try:
		(h, w) = screen.getmaxyx()
		key=''
		while True:

			screen.move(0,0)
			screen.addstr(1, 2, str(time.time()))  
			screen.addstr(2, 2, "commands are:")
			screen.addstr(4, 4, "arrow up = up")
			screen.addstr(5, 4, "arrow dw = down")
			screen.addstr(6, 4, "arrow left = in")
			screen.addstr(7, 4, "arrow right = out")
			screen.addstr(8, 4, "+- to change step size")
			screen.addstr(9, 4, "c = calibrate")
			screen.addstr(10, 4, "q = quit")


			screen.addstr(15, 4, u'\u2513'.encode('utf-8'))
			screen.addstr(16, 4, "q = quit")
			
			key = screen.getch()
						
			# window.move(y, x)
			# window.addch("*")
			
			time.sleep(0.05)
			
			#quit
			if key == ord('q'):
				GPIO.cleanup()	
				break
			#calibrate elevator
			if key == ord('c'):
				motor1.calibrate()
				

			#up
			if key == curses.KEY_UP:
				motor1.doStep(-stepsize)
			#down
			if key == curses.KEY_DOWN:
				motor1.doStep(stepsize)
			#in
			if key == curses.KEY_LEFT:
				motor3.doStep(stepsize)
			#out
			if key == curses.KEY_RIGHT:
				motor3.doStep(-stepsize)
			#steps plus
			if key ==  ord('+'):
				stepsize = stepsize + 10
			#steps plus
			if key == ord('-'):
				stepsize = stepsize - 10
			
			#### show info section
			motorpos1 = 	"Pos Elevator: " + str(motor1.currentPosition) +"     "
			screen.addstr(4, 30, motorpos1 +"     ")
			screen.addstr(4, 55, "Loopstop: " + str(motor1.loopStop)+"    ")
			screen.addstr(5, 55, "Endstop: " + str(motor1.endStop)+"    ")
			
			motorpos3 = 	"Pos Slider  : " + str(motor3.currentPosition)+"     "
			screen.addstr(5, 30, motorpos3)
			tstepssize = "Steps size: "+ str(stepsize)+"       "
			screen.addstr(6, 30, tstepssize )
			screen.refresh()	
			
	except KeyboardInterrupt:
		pass
	finally:
		curses.endwin()

curses.wrapper( main) 		





