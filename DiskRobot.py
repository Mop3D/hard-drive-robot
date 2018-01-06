#!/usr/bin/python
import getch
import Elevator as Elevator
print("DiskRobot")

diskElevator = Elevator.Steuerung()

diskElevator.info()

while True:
    print("\ncommands are:")
    print("   f = stepForward")
    print("   b = stepBackward")
    print("   c = calibrate")
    print("   i = info")
    print("   q = quit")
    command = raw_input("command:")
    
    #quit
    if command == "q":
        diskElevator.dispose()
        break
    
    #info
    if command == "i":
        diskElevator.info()

    #calibrate
    if command == "c":
        diskElevator.calibrate()
    #stepForward
    if command == "f":
        steps = input("steps forward:")
        diskElevator.stepForward(int(steps))
    #stepBackward
    if command == "b":
        steps = input("steps backward:")
        diskElevator.stepBackward(int(steps))


