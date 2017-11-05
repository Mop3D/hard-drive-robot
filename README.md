# hard-drive-robot
Sample project to access hard drives in a rack by motorized cage.
Like the (old) tape roboters.

Code is running on a raspberry pi 3.

Used hardware:

- Elegoo 5 sets 5V Stepper Motor + ULN2003 Driver Board (available at Amazon)
- 3D printed hard drive rack
- raspberry pi 3

Functions for controlling stepper motors
GpioMotor.py - Basis class for controlling stepper via raspberry gpio ports
test.py - just a test program for the basis functionallity. 
atest.py - test with two instances of motor 
DiskRobot.py - main test program
Elevator.py - main class to control all needed motors (3)

