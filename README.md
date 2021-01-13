# hard-drive-robot
Sample project to access hard drives in a rack by motorized cage.
Like the (old) tape roboters.

Used hardware:

- Elegoo 5 sets 5V Stepper Motor + ULN2003 Driver Board (available at Amazon)
- 3D printed hard drive rack
- raspberry pi 3 or Banana Pi BPI-M1

Functions for controlling stepper motors
GpioMotor.py - Basis class for controlling stepper via raspberry gpio ports
test.py - just a test program for the basis functionallity. 
atest.py - test with two instances of motor 
DiskRobot.py - main test program
Elevator.py - main class to control all needed motors (3)

Web Url
```
http://hdrobo:8888
```


Code is running on a raspberry pi 3
-----------------------------------
```
Install pyudev
$ sudo apt-get install python-pip
$ sudo pip install pyudev
---- psutil ---
$ pip install psutil
(on ImportError: No module named psutil
$ sudo pip install --upgrade psutil
)
```

```
Install ntfs-3g
$ sudo apt-get install ntfs-3g
```

```
Install tornado
get the last version of tornado
$ sudo python -m pip install tornado
```

```
Install yaml
$ sudo python -m pip install pyyaml
```

```
Run HD Robo Desk
$ cd ~/hard-drive-robot/web
$ sudo ./HDRobo-Desk.py
```

```
Install Events
$ sudo pip install events
```





Code running on Banana Pi BPI-M1
--------------------------------
```
Install gpio
$ sudo apt-get install python-dev
$ sudo apt-get install git
$ git clone https://github.com/LeMaker/RPi.GPIO_BP -b bananapro
$ cd ./RPi.GPIO_BP
$ sudo python setup.py install

Install pyudev
$ sudo apt-get install python-pip
$ sudo pip install pyudev

Install tornado
get the last version of tornado
$ sudo python -m pip install tornado
```
