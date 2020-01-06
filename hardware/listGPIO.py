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

def main(stdscr):
	try:
	
		print "in func"
		curses.noecho()
		curses.cbreak()
		global screen 
		screen = curses.initscr()
		screen.keypad(True)

		GPIO.setmode(GPIO.BCM)  
		ports = [2,3,4,17,27,22,10,9,11,5,6,13,19,26,14,15,18,23,24,25,8,7,12,16,20,21]  
		pin_type = "Port"  
		
		# Using a dictionary as a lookup table to give a name to gpio_function() return code  
		port_use = {0:"GPIO.OUT", 1:"GPIO.IN",40:"GPIO.SERIAL",41:"GPIO.SPI",42:"GPIO.I2C",43:"GPIO.HARD_PWM", -1:"GPIO.UNKNOWN"} 

		
		# loop through the list of ports/pins querying and displaying the status of each  
		for port in ports:  
			usage = GPIO.gpio_function(port)  
			if usage==1 :
				GPIO.setup(port, GPIO.IN)
				value = GPIO.input(port)
				s = "%s %d status: %s value: %d" % (pin_type, port, port_use[usage], value) 
			else:
				s = "%s %d status: %s " % (pin_type, port, port_use[usage]) 
				
			screen.addstr(port, 4, s)
			
			screen.refresh()
			sleep(0.1)
		screen.getch()	
		
	except KeyboardInterrupt:
		pass
	finally:
		GPIO.cleanup()
		curses.endwin()
def showPort( port ):
	try:
		
		screen.addstr(port, 4, "Port "+str(port)+":"+ str(GPIO.input(port)) )
	except:
		#print "Port :"+str(port)
		a=11

def mycallback( port ):
	try:
		screen.addstr(20,4, "asdfasdfasdf" )
	except:
		#print "Port :"+str(port)
		a=10
	
	
curses.wrapper( main) 		


