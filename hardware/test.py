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
	try:
		locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')
		locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
		
		curses.noecho()
		curses.cbreak()
		screen = curses.initscr()
		screen.keypad(True)
		screen.border( '└','-',chr(126),'+','+','+')


		screen.addstr(4, 4, "#test text#")
		screen.addstr(5, 4, "#äöüß@²³#")
		screen.addstr(6, 4, "#─┓	└	┕	┖	╣	╤#")
		#screen.addstr(6, 4, unichr(40960))
		c = curses.ACS_ULCORNER

		screen.refresh()
		sleep(0.1)
		screen.getch()	
		
	except KeyboardInterrupt:
		pass
	finally:
		GPIO.cleanup()
		curses.endwin()
	
curses.wrapper( main) 		


